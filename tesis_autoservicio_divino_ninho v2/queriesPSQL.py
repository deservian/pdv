import psycopg2
from psycopg2 import Error

class QueriesPostgres:
    @staticmethod
    def create_connection():
        connection = None
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="jvgoLMSYRUWBaXgHTfHbUdBEzkgSkHMC",
                host="postgres.railway.internal",
                port="5432",
                database="railway"
            )
            print("Connection to PostgreSQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    @staticmethod
    def execute_query(connection, query, data_tuple):
        cursor = connection.cursor()
        try:
            cursor.execute(query, data_tuple)
            connection.commit()
            print("Query executed successfully")
            return cursor.lastrowid
        except Error as e:
            print(f"The error '{e}' occurred")

    @staticmethod
    def execute_read_query(connection, query, data_tuple=()):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query, data_tuple)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

