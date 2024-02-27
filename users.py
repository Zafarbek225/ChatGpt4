import psycopg2 
from psycopg2 import Error

def USERS(id, ism, familiya, phone):
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="postgresql",
                                  host="127.0.0.1",
                                  port= "5432",
                                  database="chatgpt")
        cursor = connection.cursor()
        create_table_querty='''CREATE TABLE USERS
            (ID TEXT PRIMARY KEY NOT NULL,
            FIRST_NAME TEXT NOT NULL,
            LAST_NAME TEXT ,
            NUMBER TEXT 
            );'''

        insert_querty='''INSERT INTO USERS (ID, FIRST_NAME, LAST_NAME, NUMBER) VALUES (%s, %s, %s, %s)'''
        cursor.execute(insert_querty, (id, ism, familiya, phone))
        connection.commit()
        print("Qo'shildi")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
