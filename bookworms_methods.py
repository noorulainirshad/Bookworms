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


def auth(conn, input1, input2):
    cursor = conn.cursor()
    try:
        # input1 = input('print username: ')
        # input2 = input('print password: ')
        cursor.execute('''SELECT * FROM User where u_username = ? and u_password = ?''', (input1, input2))

        user = cursor.fetchone()  # attempt to fetch a single user with matching username and password
        if user:
            print("Authentication successful. User exists in the database.")
            print(user)
        else:
            print("Authentication failed. User does not exist or provided credentials are incorrect.")
        return True
    except Error as e:
        print("Error in SQL query:", e)
        return False


def delAcct(conn, input1, input2):
    exists = auth(conn, input1, input2)
    if exists:
        cursor = conn.cursor()
        try:
            cursor.execute('''DELETE FROM User where u_username = ? and u_password = ?''', (input1, input2))
            print("User account deletion successful.")
        except Error as e:
            print("User account deletion failed.")
            print("Error in SQL query:", e)


def createAcct(conn, input1, input2):
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO User (u_username, u_password) values(?,?)''', (input1, input2))
        print("User account creation successful.")
    except Error as e:
        print("User account deletion failed.")
        print("Error in SQL query:", e)

def main():
    # database = r"data.sqlite"
    database = r"bookworms_db.sqlite"

    input1 = input('print username: ')
    input2 = input('print password: ')

    # create a database connection
    conn = openConnection(database)
    with conn:
        #auth(conn, input1, input2)
        #delAcct(conn, input1, input2)
        createAcct(conn, input1, input2)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
