import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param _dbFile: database file
    :return: Connection object or None
    """
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn


def closeConnection(conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def loggedIn(conn):




def auth(conn, input1, input2):
    cursor = conn.cursor()
    try:
        # input1 = input('print username: ')
        # input2 = input('print password: ')
        cursor.execute('''SELECT * FROM User where u_username = ? and u_password = ?''', (input1, input2))

        user = cursor.fetchone()  # attempt to fetch a single user with matching username and password
        if user:
            print("Authentication successful. User exists in the database.")
            # print(user)
            return True
        else:
            print("Authentication failed. User does not exist or provided credentials are incorrect.")
            return False
    except Error as e:
        print("Error in SQL query:", e)
        # return False


def delAcct(conn):

    input1 = input('print username: ')
    input2 = input('print password: ')

    exists = auth(conn, input1, input2)
    cursor = conn.cursor()
    # print(exists)
    if exists:
        cursor.execute('''DELETE FROM User where u_username = ? and u_password = ?''', (input1, input2))
        print("User account deletion successful.")
    else:
        print("User account deletion failed.")

    #     try:
    #         cursor.execute('''DELETE FROM User where u_username = ? and u_password = ?''', (input1, input2))
    #         print("User account deletion successful.")
    #     except Error as e:
    #         print("User account deletion failed.")
    #         print("Error in SQL query:", e)


def createAcct(conn):
    cursor = conn.cursor()

    input1 = input('print username: ')
    input2 = input('print password: ')

    cursor.execute('''SELECT u_username FROM User WHERE u_username = ?''', (input1,))
    exists = cursor.fetchone()
    # print(type(exists))
    # print(tuple(input1))
    if exists != (input1,):
        cursor.execute('''INSERT INTO User (u_username, u_password) values(?,?)''', (input1, input2))
        print("User account creation successful.")
    else:
        print("User account creation failed because {} is already in use. Please try again with a new username.".format(input1))
    # # try:

    # except Error as e:
    #     print("User account creation failed.")
    #     print("Error in SQL query:", e)


def createList(conn):
    cursor = conn.cursor()

    input1 = input('Enter list name: ')

    cursor.execute('''SELECT u_username, lis FROM User WHERE u_username = ?''', (input1,))
    exists = cursor.fetchone()
    # print(type(exists))
    # print(tuple(input1))
    if exists != (input1,):
        cursor.execute('''INSERT INTO User (u_username, u_password) values(?,?)''', (input1, input2))
        print("User account creation successful.")
    else:
        print("User account creation failed because {} is already in use. Please try again with a new username.".format(input1))


def main():
    # database = r"data.sqlite"
    database = r"bookworms_db.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        #auth(conn)
        delAcct(conn)
        #createAcct(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
