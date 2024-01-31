from psycopg2 import Error

from db_connection import connection


create_table_users = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  email VARCHAR(50),
  password VARCHAR(50),
  age NUMERIC CHECK (age > 1 AND age < 150)
);
"""

        
if __name__ == '__main__':
    with connection() as conn:
        if conn is not None:
            c = conn.cursor()
            c.execute(create_table_users)
            c.close()