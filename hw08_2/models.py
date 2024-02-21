from mongoengine import *

connect(host="mongodb+srv://userweb9:567234@cluster0.oaw543f.mongodb.net/hw08", ssl=True)


class Contact(Document):
    fullname = StringField(required=True)    
    email = StringField(required=True)
    sent_email = BooleanField(default=False)
