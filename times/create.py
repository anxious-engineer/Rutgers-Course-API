import sqlite3


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# END METHOD DEFINITIONS


# Create Table Statement
sql_create_index_table = """ CREATE TABLE IF NOT EXISTS times (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                subject TEXT NOT NULL,
                                course_title TEXT NOT NULL,
                                campus_name TEXT,
                                building_code TEXT,
                                room_number TEXT,
                                meeting_day TEXT,
                                begin_time TEXT,
                                end_time TEXT
                            );"""

# Creates Connection to Database
connection = sqlite3.connect('times.db')

if connection is not None:
    # Create Table
    create_table(connection, sql_create_index_table)

else:
    print("Error Connecting to times Database.")

connection.close()

