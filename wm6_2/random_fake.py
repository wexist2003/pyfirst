# pip install Faker
from random import randint

from psycopg2 import Error
from faker import Faker

from db_connection import connection

fake = Faker('uk-UA')

insert_user = """
INSERT INTO users (name, email, password, age) VALUES (%s, %s, %s, %s);
"""

        
if __name__ == '__main__':
    with connection() as conn:
        if conn is not None:
            c = conn.cursor()
            for _ in range(10000):
                c.execute(insert_user, (fake.name(), fake.email(), fake.password(), randint(2, 120)))
            c.close()
