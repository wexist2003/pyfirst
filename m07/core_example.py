from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import MetaData

from sqlalchemy import create_engine
from sqlalchemy.sql import select


engine = create_engine('sqlite:///:memory:', echo=True)
metadata = MetaData()


users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)


addresses = Table('addresses', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('email_address', String, nullable=False))
    

metadata.create_all(engine)

if __name__ == '__main__':
    with engine.connect() as conn:
        ins = users.insert().values(name='jack', fullname='Jack Jones')
        print(str(ins))     # INSERT INTO users (name, fullname) VALUES (:name, :fullname)
        conn = engine.connect()
        result = conn.execute(ins)
        s = select(users)
        result = conn.execute(s)
        for row in result:
            print(row)  # (1, u'jack', u'Jack Jones')        
        conn.close()