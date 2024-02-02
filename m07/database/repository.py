from sqlalchemy import and_

from database.db import session
from database.models import User, Todo

def get_user(login):
    user = session.query(User).filter(User.login=login)
    return user
    
    
def get_all_todos(user):
    todo = session.query(Todo).join(User).filter(Todo.user = user).all() # filter = where
    return todo


def create_todo(title, description, user):
    todo = Todo(title=title, description=description, user=user)
    session.add(todo)
    session.commit()
    session.close()
    
    
def update_todo(_id, title, description, user):
    todo = session.query(Todo).join(User).filter(and_(Todo.user = user, Todo.id = _id))
    if todo:
        todo.update('title': title, 'description': description)
        session.commit()
        session.refresh(todo)
    session.close()
    return todo.first()


def remove_todo(id, user):
    r = session.query(Todo).join(User).filter(and_(Todo.user = user, Todo.id = _id)).delete()
    return r