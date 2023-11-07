import sqlite3
from sqlite3 import Error

# global var; bool val represents login status
loggedIn = False

global userKey


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


def logOut(conn):
    global loggedIn
    loggedIn = False


def auth(conn):
    cursor = conn.cursor()
    try:
        # if loggedIn == True no need to authenticate
        global loggedIn
        if loggedIn:
            return loggedIn
        else:
            # get username and password from user to authenticate
            username = input('print username: ')
            password = input('print password: ')

            # check if username + password combination exists in User table
            cursor.execute('''SELECT * FROM User where u_username = ? and u_password = ?''', (username, password))

            # attempt to fetch a single user with matching username and password
            user = cursor.fetchone()

            # if username + password combination exists in User table
            if user:
                print("Authentication successful. User exists in the database.")

               # grab u_userkey using the username + password combination
                cursor.execute('''select u_userkey from User where u_username = ? and u_password = ?''', (username, password))

                # stores u_userkey in userKey var to access the user's lists in createList()
                global userKey
                userKey = cursor.fetchone()

                loggedIn = True
                return True

            # username + password combination does not exist in User table
            else:
                print("Authentication failed. User does not exist or provided credentials are incorrect.")
                return False

    except Error as e:
        print("Error in SQL query:", e)
        # return False


def delAcct(conn):
    # retrieve account info to delete an account
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
    # checks to see if already logged in
    if loggedIn:
        print("User is already logged in")

    # if not logged in, proceeds to make a new account
    else:

        input1 = input('print username: ')
        input2 = input('print password: ')
        cursor = conn.cursor()

    # checks to see if username does not previously exist before creating account
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

    listName = input('Enter list name: ')

    cursor.execute('''SELECT l_name, l_userkey FROM List WHERE l_name = ?''', (listName,))
    exists = cursor.fetchone()

    if exists != (listName,):
        cursor.execute('''INSERT INTO List (l_name, l_userkey) values(?,?)''', (listName, userKey[0]))
        print("{} was successfully created.".format(listName))
    else:
        print("{} was not successfully created.".format(listName))


def main():
    # database = r"data.sqlite"
    database = r"bookworms_db.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        auth(conn)
        #delAcct(conn)
        #createAcct(conn)
        createList(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
