from db_connection import connection


change_table_users = """
    ALTER TABLE users ADD COLUMN phone_number varchar(15);
"""

        
if __name__ == '__main__':
    with connection() as conn:
        c = conn.cursor()
        c.execute(change_table_users)            
        c.close()
