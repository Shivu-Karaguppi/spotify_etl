import mysql.connector
import pandas as pd
# Replace these values with your own database credentials
db_config = {
    'host': 'database-analytics.c3y0yk8mqy0g.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'admin1234',
    'database': 'mydb'
}

def conn_closed(connection):
    # Close the connection in the finally block to ensure it's always closed
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print('Connection closed')

def create_table():
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            cursor=connection.cursor()
            cursor.execute("""CREATE TABLE artist2 (
        artist_id VARCHAR(50) ,
        name VARCHAR(50),
        followers INT,
        popularity INT,
        genere VARCHAR(50),
        fetched_on VARCHAR(50),
        week_day VARCHAR(50) );""")
        print('Query executed...& table creted')

            # Perform database operations here

    except mysql.connector.Error as e:
        print(f'Error connecting to MySQL database: {e}')

    finally:
        conn_closed(connection)

# def insert_records(value1, value2, value3,value4, value5, value6):
def insert_records(id,name,followers,popularity,genere,fetched_on,week_day):  #(id,name,followers,popularity,genre,dateTime,week_day)
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            cursor=connection.cursor()
            ins_qry=f"""INSERT INTO mydb.artist2 VALUES ('{id}','{name}',{followers},{popularity},'{genere}','{fetched_on}','{week_day}');""" #(id,name,followers,popularity,genre,dateTime,week_day)
            print(ins_qry)
            cursor.execute(ins_qry)
            connection.commit()
            print('records inserted...')

            # Perform database operations here

    except mysql.connector.Error as e:
        print(f'Error connecting to MySQL database: {e}')

    finally:
        conn_closed(connection)

# insert_records()
def query_executor():
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**db_config)
        query = "SELECT * FROM mydb.artist2"
        df = pd.read_sql_query(query, connection)
        print(df)

    except mysql.connector.Error as e:
        print(f'Error connecting to MySQL database: {e}')

    finally:
        conn_closed(connection)

# insert_records()
# query_executor()
# create_table()