import json
import os
from re import split
import sys


from mongoengine import *


from models import Authors, Quotes
    
    
class ExceptValidation(Exception):
    pass

def load_authors_json_to_mongodb(json_file_path):
    # open json
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # json load
    for item in data:
        author = Authors(
            fullname=item['fullname'],
            born_date=item.get('born_date', ''),
            born_location=item.get('born_location', ''),
            description=item.get('description', '')
        )
        author.save()

def load_quotes_json_to_mongodb(json_file_path):
    # open json
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # json load
    for item in data:
        author_name = item.get('author', '')
        author = Authors.objects(fullname=author_name).first()
        quotes = Quotes(
            tags=item['tags'],
            author=author.id,
            quote=item.get('quote', '')
        )
        quotes.save()


def find_quotes_by_author(name):
    author = Authors.objects(fullname=name).first()
    if author:
        quotes = Quotes.objects(author=author)
        return list(quotes)
    else:
        return []

def find_quotes_by_tag(tag):
    quotes = Quotes.objects(tags=tag)
    return list(quotes)

def find_quotes_by_tags(tags):
    quotes = Quotes.objects(tags__in=tags)
    return list(quotes)

def main():
    while True:
        commands = input('Enter command:value from list (load_authors:file_name, load_quotes:file_name, name:name, tag:tag, tags:tag1,tag2, exit)? -->')
        aim = commands.split(':')
        action = aim[0]
        parameter = aim[1] if len(aim) > 1 else None
        print(action,parameter)
        try:
            match action:
                case 'load_authors':
                    if not os.path.isabs(parameter):
                        parameter = os.path.join(current_directory, parameter)
                    load_authors_json_to_mongodb(parameter)
                case 'load_quotes':
                    if not os.path.isabs(parameter):
                        parameter = os.path.join(current_directory, parameter)
                    load_quotes_json_to_mongodb(parameter)
                case 'name':
                    name = parameter
                    quotes = find_quotes_by_author(name)
                    if quotes:
                        print(f"Цитати автора '{name}':")
                        for quote in quotes:
                            print(quote.quote)
                    else:
                        print(f"Автор '{name}' не знайдений або у нього немає цитат.")            
                case 'tag':
                    tag = parameter
                    quotes = find_quotes_by_tag(tag)
                    if quotes:
                        print(f"Цитати з тегом '{tag}':")
                        for quote in quotes:
                            print(quote.quote)
                    else:
                        print(f"Цитат з тегом '{tag}' не існує.")  
                case 'tags':
                    tags = parameter.split(',')
                    quotes = find_quotes_by_tags(tags)
                    if quotes:
                        print(f"Цитати з тегами '{tags}':")
                        for quote in quotes:
                            print(quote.quote)
                    else:
                        print(f"Цитат з тегами '{tags}' не існує.")                                
                case 'exit':
                    sys.exit()  
                case _:
                    print(f'Unknown command')                           
        except ExceptValidation as err:
            print(err)


if __name__ == "__main__":
    print('Wait for starting ...')
    client = connect(host="mongodb+srv://userweb9:567234@Cluster0.oaw543f.mongodb.net/hw08", ssl=True)
    current_directory = os.getcwd()
    main()

