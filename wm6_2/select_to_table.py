import pprint

from db_connection import connection


simple_select = """
    SELECT * FROM users WHERE id=%s;
"""
select = """
    SELECT id, name, email, age
    FROM users
    WHERE age > 15
    ORDER BY name, age DESC
    LIMIT 10;
"""
select_regex = """
    SELECT id, name, email, age
    FROM users
    WHERE name SIMILAR TO '%(рій|ко)%'
    ORDER BY name, age DESC
    LIMIT 10;
"""

        
if __name__ == '__main__':
    with connection() as conn:
        if conn is not None:
            c = conn.cursor()
            # c.execute(simple_select, (10,))
            # print(c.fetchone())
            c.execute(select_regex)
            print(c.fetchall())
            # pprint.pprint(c.fetchall())
            c.close()
