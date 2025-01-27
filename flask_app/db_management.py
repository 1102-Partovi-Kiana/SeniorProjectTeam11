import psycopg2

def main():
    table_name = "course_subsections"
    data = [
        (1.9, "C1 Quiz One")
    ]

    connection = psycopg2.connect(
        dbname="test",
        user="testuser",
        password="testPassword",
        host="localhost"
    )

    insert_data_into_table(connection, table_name, data)

    connection.close()

def insert_data_into_table(connection, table_name, data):
    insert_query = f"""
    INSERT INTO {table_name} (course_subsection_number, course_subsection_name) VALUES (%s, %s)
    """
    cursor = connection.cursor()
    cursor.executemany(insert_query, data)
    connection.commit()
    print(f"Inserted {len(data)} rows into {table_name}.")
    cursor.close()

if __name__ == "__main__":
    main()