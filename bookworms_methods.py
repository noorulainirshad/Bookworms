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
    print('You have successfully logged out. Have a nice day!')


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
            cursor.execute('''SELECT * FROM User 
                            WHERE u_username = ? 
                            AND u_password = ?''', (username, password))

            # attempt to fetch a single user with matching username and password
            user = cursor.fetchone()

            # if username + password combination exists in User table
            if user:
                print("Authentication successful. User exists in the database.")

               # grab u_userkey using the username + password combination
                cursor.execute('''SELECT u_userkey FROM User 
                                WHERE u_username = ? AND u_password = ?''', (username, password))

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
        cursor.execute('''DELETE FROM User 
                    WHERE u_username = ? 
                    AND u_password = ?''', (username, password))
        print("User account deletion successful.")
    else:
        print("User account deletion failed.")

    conn.commit()
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
        cursor.execute('''SELECT u_username FROM User 
                        WHERE u_username = ?''', (username,))
        exists = cursor.fetchone()
        # print(type(exists))
        # print(tuple(input1))
        if exists != (username,):
            cursor.execute('''INSERT INTO User (u_username, u_password) values(?,?)''', (username, password))
            print("User account creation successful.")
        else:
            print("User account creation failed because {} is already in use. Please try again with a new username.".format(username))

    conn.commit()
        # # try:

        # except Error as e:
        #     print("User account creation failed.")
        #     print("Error in SQL query:", e)


#
def createList(conn):
    # still need to implement authentification**
    cursor = conn.cursor()

    listName = input('Enter list name: ')

    # checks if user has created a list using listName as l_name
    cursor.execute('''SELECT l_name, l_userkey 
                    FROM List 
                    WHERE l_name = ?''', (listName,))

    exists = cursor.fetchone()

    # user has not created a list using listName as l_name
    if exists != (str(listName), userKey[0]):
        cursor.execute('''INSERT INTO List (l_name, l_userkey) 
                        values(?,?)''', (listName, userKey[0]))
        print("{} was successfully created.".format(listName))
    # user already created a list using listName as l_name
    else:
        print("{} was not successfully created because you already created a list named {}.".format(listName, listName))

    conn.commit()

def delList(conn):
    # retrieve account info to delete an account
    listName = input('Enter the list you want to delete: ')
    cursor = conn.cursor()

    # checks if user has created a list using listName as l_name
    cursor.execute('''SELECT l_name, l_userkey 
                    FROM List 
                    WHERE l_name = ?''', (listName,))

    exists = cursor.fetchone()
    # print(exists)
    if exists == (str(listName), userKey[0]):
        cursor.execute('''DELETE FROM List 
                        WHERE l_name = ? 
                        AND l_userkey = ?''', (listName, userKey[0]))

        print("List deletion successful.")
    else:
        print("List deletion failed.")

    conn.commit()

def addBookToList(conn):
    cursor = conn.cursor()

    listName = input("What list do you want to add a book to? ")

    # checks if user has created a list using listName as l_name
    # duplicate
    cursor.execute('''SELECT l_name, l_userkey 
                    FROM List 
                    WHERE l_name = ?''', (listName,))

    listExists = cursor.fetchone()

    # if list exists
    if listExists is not None:
        bookName = input("What book do you want to add? ")

        # check if book exists
        # duplicate
        cursor.execute('''SELECT b_bookkey FROM Book 
                            WHERE LOWER(title) = LOWER(?)''', (bookName,))
        # store tuple containing book key
        bookKey = cursor.fetchone()

        # if book exists
        if bookKey is not None:
            # check if book already exists in list
            cursor.execute('''SELECT lb_bookkey FROM ListBook 
                                WHERE lb_bookkey = ? 
                                AND lb_listkey = ?''', (bookKey[0], listExists[0]))
            # store tuple containing book title in title var
            bookInListBook = cursor.fetchone()
            # print(exists)
            if listExists == (str(listName), userKey[0]) and bookInListBook is None:
                cursor.execute('''INSERT INTO ListBook 
                                (lb_listkey, lb_bookkey, lb_userkey) values(?,?,?)''',
                               (listExists[1], bookKey[0],  userKey[0]))
                print("Book addition to list was successful.")
            else:
                print("Book addition to list was not successful.")
        else:
            print("Book does not exist.")
    # list does not exist
    else:
        print("Sorry, your list does not exist.")

    conn.commit()

def displayList(conn):
    cursor = conn.cursor()
    bookName = input("What book list do you want to view? Please enter list name: ")


    # check if list exists
    # duplicate
    cursor.execute('''SELECT b_bookkey FROM Book
                        WHERE LOWER(title) = LOWER(?)''', (bookName,))
    bookKey = cursor.fetchone()

    # if book key exists
    if bookKey is not None:
        cursor.execute('''SELECT u_username, stars, comment
                        FROM User, Rating, Book
                        WHERE u_userkey = r_userkey
                        AND r_bookkey = b_bookkey
                        AND b_bookkey = ?
                        ''', (bookKey[0],))
        ratings = cursor.fetchall()
        print(ratings)
    # book does not exist in database
    else:
        print("Unfortunately, that book is not in our database")
def createRating(conn):
    # implement auth
    cursor = conn.cursor()
    bookName = input("What book do you want to rate? ")

    # check if book exists
    cursor.execute('''SELECT title FROM Book 
                        WHERE LOWER(title) = LOWER(?)''', (bookName,))
    # store tuple containing book title in title var
    title = cursor.fetchone()

    # if title exists
    if title is not None:

        # check if rating exists (same user and bookName)
        cursor.execute('''SELECT * FROM Rating, Book, User 
                        WHERE r_bookkey = b_bookkey 
                        AND LOWER(title) = LOWER(?) 
                        AND r_userkey = u_userkey
                        AND r_userkey = ?''', (bookName, userKey[0]))

        ratingExists = cursor.fetchone()
        # print(type(exists))

        # if there is no previous rating from user on the book
        if ratingExists is None:

            # grabs book key to use for insert statement below
            cursor.execute('''SELECT b_bookkey from Book 
                            WHERE LOWER(title) = LOWER(?)''', (bookName,))
            bookKey = cursor.fetchone()
            # eg output for print(bookKey): (10,)
            # declare star var
            stars = 0
            # GUI: create a textbox that only accepts int vals
            try:
                stars = int(input("How many stars would you give this book? (Please enter an integer.) "))
            except Error as e:
                print("Rating failed. Please enter an integer.")
            # GUI: comments are optional
            comment = input("Comments (optional): ")

            cursor.execute('''INSERT INTO Rating (stars, r_userkey, r_bookkey, comment) values(?,?,?,?)''', (stars, userKey[0], bookKey[0], comment))

            print("Your rating was successfully created.")

        # user already rated that book
        else:
            print("Your rating was not successfully created because you already wrote a rating for {}.".format(title[0]))
    # book does not exist in our database
    else:
        print("Unfortunately, that book is not in our database :((((")

    conn.commit()

def editRating(conn):
    cursor = conn.cursor()
    bookName = input("What book rating do you want to edit? Please enter book name: ")

    # check if book exists
    # duplicate
    cursor.execute('''SELECT title FROM Book 
                        WHERE LOWER(title) = LOWER(?)''', (bookName,))
    title = cursor.fetchone

    # if title exists
    if title is not None:
        # check if rating exists (same user and bookName)
        cursor.execute('''SELECT r_ratingkey FROM Rating, Book, User 
                        WHERE r_bookkey = b_bookkey 
                        AND LOWER(title) = LOWER(?) 
                        AND r_userkey = u_userkey
                        AND r_userkey = ?''', (bookName, userKey[0]))

        ratingKey = cursor.fetchone()

        # if ratingKey exists
        if ratingKey is not None:
            stars = 0
            # GUI: create a textbox that only accepts int vals
            try:
                stars = int(input("How many stars would you give this book? (Please enter an integer.) "))
            except Error as e:
                print("Rating failed. Please enter an integer.")

            # GUI: comments are optional
            comment = input("Comments (optional): ")

            cursor.execute('''UPDATE Rating 
                            SET stars = ?, comment = ? 
                            WHERE r_ratingkey = ?''', (stars, comment, ratingKey[0]))
            print("Rating was successfully updated.")
        # rating does not exist
        else:
            print("Sorry, you did not write a rating for {}".format(title[0]))
    # title does not exist in database
    else:
        print("Sorry, there is no rating because this book is not in our database.")

    conn.commit()

def deleteRating(conn):
    cursor = conn.cursor()
    bookName = input("What book rating do you want to edit? Please enter book name: ")

    # check if book exists
    # duplicate
    cursor.execute('''SELECT title FROM Book 
                        WHERE LOWER(title) = LOWER(?)''', (bookName,))
    title = cursor.fetchone()

    # if title exists
    if title is not None:
        # check if rating exists (same user and bookName)
        cursor.execute('''SELECT r_ratingkey, r_bookkey 
                        FROM Rating, Book, User 
                        WHERE r_bookkey = b_bookkey 
                        AND LOWER(title) = LOWER(?) 
                        AND r_userkey = u_userkey
                        AND r_userkey = ?''', (bookName, userKey[0]))
        ratingKey_and_bookKey = cursor.fetchone()
        # if ratingKey_and_bookKey exists
        if ratingKey_and_bookKey is not None:
            cursor.execute('''DELETE FROM Rating 
                            WHERE r_ratingkey = ?
                            AND r_bookkey = ? 
                            AND r_userkey = ?''', (ratingKey_and_bookKey[0], ratingKey_and_bookKey[1], userKey[0]))
        # rating does not exist
        else:
            print("There was no rating previously written by you for this book.")
    # title does not exist in database
    else:
        print("Sorry, there is no rating because this book is not in our database.")

    conn.commit()

def displayRatings(conn):
    cursor = conn.cursor()
    bookName = input("What book ratings do you want to view? Please enter book name: ")

    # check if book exists
    # duplicate
    cursor.execute('''SELECT b_bookkey FROM Book
                        WHERE LOWER(title) = LOWER(?)''', (bookName,))
    bookKey = cursor.fetchone()

    # if book key exists
    if bookKey is not None:
        cursor.execute('''SELECT u_username, stars, comment
                        FROM User, Rating, Book
                        WHERE u_userkey = r_userkey
                        AND r_bookkey = b_bookkey
                        AND b_bookkey = ?
                        ''', (bookKey[0],))
        ratings = cursor.fetchall()
        print(ratings)
    # book does not exist in database
    else:
        print("Unfortunately, that book is not in our database")

    conn.commit()

def main():
    # database = r"data.sqlite"
    database = r"bookworms_db.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        while True:
            acctExists = input('Do you have an account with Bookworms? Y/N: ')
            if acctExists.upper() == 'Y':
                auth(conn)
                break
            elif acctExists.upper() == 'N':
                makeAcct = input('Would you like to make an account? Y/N: ')
                if makeAcct.upper() == 'Y':
                    createAcct(conn)
                    print('Please login with your new account!\n')
                    auth(conn)
                else:
                    print('Understandable, have a nice day!')
                break
            else:
                print('Please input a valid response.\n')

        print('\nWelcome to Bookworms!')
        while loggedIn:
            print('''
These are the available commands:
1: create a new list 
2: add a book to a list
3: delete a book from a list
4: delete a list
5: create a new book review
6: edit a review 
7: display a book's reviews 
8: delete an account
9: logout\n''')


            response = int(input('What action would you like to perform? '))

            if response == 1:
                createList(conn)
            if response == 2:
                addBookToList(conn)
            if response == 3:
                delList(conn)
            if response == 4:
                createRating(conn)
            if response == 5:
                editRating(conn)
            if response == 6:
                displayRatings(conn)
            if response == 7:
                delAcct(conn)
            if response == 8:
                logOut(conn)


    closeConnection(conn, database)


if __name__ == '__main__':
    main()
