from mongoengine import *

connect(host="mongodb+srv://userweb9:567234@Cluster0.oaw543f.mongodb.net/hw08", ssl=True)


class Authors(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=50)
    description = StringField(max_length=10000)


class Quotes(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField(max_length=500)