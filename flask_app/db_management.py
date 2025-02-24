import psycopg2
from auth_func import * 

def main():
    table_name = "classes"
    data = [
        ("CS222", 1001, 39, "2025-02-23", "2026-02-24"),
        ("CS222", 1002, 39, "2025-02-23", "2026-02-24"),
        ("CS135", 1001, 40, "2025-02-21", "2026-02-24"),
        ("CS302", 1001, 40, "2025-02-20", "2026-02-24")
    ]

    connection = psycopg2.connect(
        dbname="test",
        user="testuser",
        password="testPassword",
        host="localhost"
    )

    #insert_admin_user(connection)
    insert_data_into_table(connection, table_name, data)

    connection.close()

def insert_data_into_table(connection, table_name, data):
    insert_query = f"""
    INSERT INTO {table_name} (class_course_code, class_section_number, user_id, created_at, expired_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    cursor.executemany(insert_query, data)
    connection.commit()
    print(f"Inserted {len(data)} rows into {table_name}.")
    cursor.close()

def insert_admin_user(connection):
    cursor = connection.cursor()

    username = "admin"
    first_name = "Admin"
    last_name = "One"
    email = "admin@example.com"
    password = "testPassword!1"
    role_id = 3 

    password = hash_password(password)

    insert_query = """
        INSERT INTO users (username, first_name, last_name, email, password, role_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (username, first_name, last_name, email, password, role_id))
    
    connection.commit()
    cursor.close()
    

if __name__ == "__main__":
    main()