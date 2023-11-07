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
            username = input('Enter username: ')
            password = input('Enter password: ')

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
    username = input('Enter username: ')
    password = input('Enter password: ')

    exists = auth(conn)
    cursor = conn.cursor()
    # print(exists)
    if exists:
        cursor.execute('''DELETE FROM User where u_username = ? and u_password = ?''', (username, password))
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

        username = input('Enter username: ')
        password = input('Enter password: ')
        cursor = conn.cursor()

    # checks to see if username does not previously exist before creating account
        cursor.execute('''SELECT u_username FROM User WHERE u_username = ?''', (username,))
        exists = cursor.fetchone()
        # print(type(exists))
        # print(tuple(input1))
        if exists != (username,):
            cursor.execute('''INSERT INTO User (u_username, u_password) values(?,?)''', (username, password))
            print("User account creation successful.")
        else:
            print("User account creation failed because {} is already in use. Please try again with a new username.".format(username))
        # # try:

        # except Error as e:
        #     print("User account creation failed.")
        #     print("Error in SQL query:", e)


def createList(conn):
    # still need to implement authentification**
    cursor = conn.cursor()

    listName = input('Enter list name: ')

    # checks if user has created a list using listName as l_name
    cursor.execute('''SELECT l_name, l_userkey FROM List WHERE l_name = ?''', (listName,))
    exists = cursor.fetchone()

    # user has not created a list using listName as l_name
    if exists != (str(listName), userKey[0]):
        cursor.execute('''INSERT INTO List (l_name, l_userkey) values(?,?)''', (listName, userKey[0]))
        print("{} was successfully created.".format(listName))
    # user already created a list using listName as l_name
    else:
        print("{} was not successfully created because you already created a list named {}.".format(listName, listName))


def delList(conn):
    # retrieve account info to delete an account
    listName = input('Enter the list you want to delete: ')
    cursor = conn.cursor()

    # checks if user has created a list using listName as l_name
    cursor.execute('''SELECT l_name, l_userkey FROM List WHERE l_name = ?''', (listName,))
    exists = cursor.fetchone()
    # print(exists)
    if exists == (str(listName), userKey[0]):
        cursor.execute('''DELETE FROM List where l_name = ? and l_userkey = ?''', (listName, userKey[0]))
        print("List deletion successful.")
    else:
        print("List deletion failed.")


def main():
    # database = r"data.sqlite"
    database = r"bookworms_db.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        auth(conn)
        #delAcct(conn)
        #createAcct(conn)
        #createList(conn)
        delList(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
