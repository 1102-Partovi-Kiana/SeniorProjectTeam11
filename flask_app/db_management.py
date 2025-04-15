import psycopg2
from auth_func import * 

def main():
    data = [
    ]
    
    connection = psycopg2.connect(
        dbname="test",
        user="testuser",
        password="testPassword",
        host="localhost"
    )

    #insert_admin_user(connection)
    #insert_student_user(connection, data)
    #insert_classes(connection, data)
    #insert_course_subsection(connection, data)
    enroll_students_in_class(connection, start_user_id=94, number_of_students=29, class_id=44)

    connection.close()

def insert_classes(connection, data):
    insert_query = f"""
    INSERT INTO classes (class_course_code, class_section_number, user_id, created_at, expired_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    cursor.executemany(insert_query, data)
    connection.commit()
    print(f"Inserted {len(data)} rows into classes table.")
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

def insert_student_user(connection, student_data):
    cursor = connection.cursor()

    hashed_data = []
    for student in student_data:
        username, first_name, last_name, email, password, role_id = student
        hashed_password = hash_password(password)
        hashed_data.append((username, first_name, last_name, email, hashed_password, role_id))

    insert_query = """
        INSERT INTO users (username, first_name, last_name, email, password, role_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(insert_query, hashed_data)
    connection.commit()
    print(f"Inserted {len(student_data)} rows into users table.")
    cursor.close()

def insert_course_subsection(connection, course_subsections_data):
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO course_subsections (course_subsection_number, course_subsection_name)
    VALUES (%s, %s)
    """
    
    cursor.executemany(insert_query, course_subsections_data)
    connection.commit()
    print(f"Inserted {len(course_subsections_data)} rows into course_subsection table.")
    cursor.close()

def enroll_students_in_class(connection, start_user_id, number_of_students, class_id):
    cursor = connection.cursor()

    enrollments = []
    for i in range(number_of_students):
        user_id = start_user_id + i
        enrollments.append((user_id, class_id))

    insert_query = """
        INSERT INTO enrollment (user_id, class_id)
        VALUES (%s, %s)
    """

    cursor.executemany(insert_query, enrollments)
    connection.commit()
    print(f"Enrolled {number_of_students} students in class_id {class_id}.")
    cursor.close()

if __name__ == "__main__":
    main()



'''
        ("DemoOne", "Demo", "One", "demoone@gmail.com", "testPassword!1", 2),
        ("DemoTwo", "Demo", "Two", "demotwo@gmail.com", "testPassword!1", 2),
        ("DemoThree", "Demo", "Three", "demothree@gmail.com", "testPassword!1", 2),
        ("DemoFour", "Demo", "Four", "demofour@gmail.com", "testPassword!1", 2),
        ("DemoFive", "Demo", "Five", "demofive@gmail.com", "testPassword!1", 2),
        ("DemoSix", "Demo", "Six", "demosix@gmail.com", "testPassword!1", 2),
        ("DemoSeven", "Demo", "Seven", "demoseven@gmail.com", "testPassword!1", 2),
        ("DemoEight", "Demo", "Eight", "demoeight@gmail.com", "testPassword!1", 2),
        ("DemoNine", "Demo", "Nine", "demonine@gmail.com", "testPassword!1", 2),
        ("DemoTen", "Demo", "Ten", "demoten@gmail.com", "testPassword!1", 2),
        ("DemoEleven", "Demo", "Eleven", "demoeleven@gmail.com", "testPassword!1", 2),
        ("DemoTwelve", "Demo", "Twelve", "demotwelve@gmail.com", "testPassword!1", 2),
        ("DemoThirteen", "Demo", "Thirteen", "demothirteen@gmail.com", "testPassword!1", 2),
        ("DemoFourteen", "Demo", "Fourteen", "demofourteen@gmail.com", "testPassword!1", 2),
        ("DemoFifteen", "Demo", "Fifteen", "demofifteen@gmail.com", "testPassword!1", 2),
        ("DemoSixteen", "Demo", "Sixteen", "demosixteen@gmail.com", "testPassword!1", 2),
        ("DemoSeventeen", "Demo", "Seventeen", "demoseventeen@gmail.com", "testPassword!1", 2),
        ("DemoEighteen", "Demo", "Eighteen", "demoeighteen@gmail.com", "testPassword!1", 2),
        ("DemoNineteen", "Demo", "Nineteen", "demonineteen@gmail.com", "testPassword!1", 2),
        ("DemoTwenty", "Demo", "Twenty", "demotwenty@gmail.com", "testPassword!1", 2),
        ("DemoTwentyOne", "Demo", "TwentyOne", "demotwentyone@gmail.com", "testPassword!1", 2),
        ("DemoTwentyTwo", "Demo", "TwentyTwo", "demotwentytwo@gmail.com", "testPassword!1", 2),
        ("DemoTwentyThree", "Demo", "TwentyThree", "demotwentythree@gmail.com", "testPassword!1", 2),
        ("DemoTwentyFour", "Demo", "TwentyFour", "demotwentyfour@gmail.com", "testPassword!1", 2),
        ("DemoTwentyFive", "Demo", "TwentyFive", "demotwentyfive@gmail.com", "testPassword!1", 2),
        ("DemoTwentySix", "Demo", "TwentySix", "demotwentysix@gmail.com", "testPassword!1", 2),
        ("DemoTwentySeven", "Demo", "TwentySeven", "demotwentyseven@gmail.com", "testPassword!1", 2),
        ("DemoTwentyEight", "Demo", "TwentyEight", "demotwentyeight@gmail.com", "testPassword!1", 2),
        ("DemoTwentyNine", "Demo", "TwentyNine", "demotwentynine@gmail.com", "testPassword!1", 2),
        ("DemoThirty", "Demo", "Thirty", "demothirty@gmail.com", "testPassword!1", 2)
'''