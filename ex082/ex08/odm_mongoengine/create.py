from models import Post, LinkPost, ImagePost, TextPost, User

if __name__ == '__main__':
    ross = User(email = 'ross@example.com', first_name = 'Ross', last_name = 'Lawley').save()

    post1 = TextPost(title='Fun with MongoEngine', author=ross)
    post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
    post1.tags = ['mongodb', 'mongoengine']
    post1.save()

    post2 = LinkPost(title='MongoEngine Documentation', author=ross)
    post2.link_url = 'http://docs.mongoengine.com/'
    post2.tags = ['mongoengine']
    post2.save()
    
    steve = User(email = 'steve@example.com', first_name = 'Steve', last_name = 'Buscemi').save()
    post3 = ImagePost(title='Foto', author=steve)
    post3.image_path = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.simplilearn.com%2Fimage-processing-article&psig=AOvVaw0eu4lQjgDkieNL2OJ1JgcP&ust=1708343385746000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLCIkpjptIQDFQAAAAAdAAAAABAE'
    post3.tags = ['actor']
    post3.save()