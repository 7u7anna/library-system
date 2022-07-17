# sql connector

import random
from random import choice
from argparse import _MutuallyExclusiveGroup
from multiprocessing.sharedctypes import Value
from random import random
from sre_compile import isstring
from sys import excepthook
import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='sqluser',
    password='password',
    database='library'
)
mycursor = mydb.cursor(buffered=True)

# python code 
class Member:
    def __init__(self, card_id, numb_of_books):
        self.card_id = card_id
        self.numb_of_books = numb_of_books

class System(Member):
    def __init__(self, card_id, numb_of_books):
        super().__init__(card_id, numb_of_books)

    def showAvailability(self):
        print(f"Enter title of the book you want to find")
        enter_title = input(f"Title: ")
        mycursor.execute(
            "SELECT status FROM books WHERE EXISTS (SELECT title FROM books WHERE title = %s);", (enter_title, )
        )
        status = mycursor.fetchone()[0]
        if mycursor.fetchone() != None:
            if status == 'avl':
                status = 'available'
            else:
                status = 'borrowed'
            print(f"Book '{enter_title}' is now {status}")
        elif mycursor.fetchone() == None:
            print(f"There is no book with such title.Try something else")

    def borrowBook(self):
        print(f"Enter book title you are searching for")
        print(f"(remember not to use uppercase letters otherwise book will not be found!)")
        enter_title = input(f"Book title: ")
        mycursor.execute(
            'SELECT author, status FROM books WHERE EXISTS (SELECT title FROM books WHERE title = %s);', (enter_title, )
        )
        if mycursor.fetchone() != None:
            author = mycursor.fetchone()[0]
            status = mycursor.fetchone()[1]
            print(f"Did you searched for book '{enter_title}' by {author} ?")
            confirm_search = int(input("1) Yes 2)No\n"))
            while confirm_search != 1 and confirm_search != 2:
                confirm_search = int(input('Please choose option 1 or 2\n'))
            if confirm_search == 1:
                if status == 'avl':
                    print(f"Book available")
                    print(f"Are you sure to borrow '{enter_title}' book by {author}?")
                    confirm_option = int(input(f"1) Yes 2) No\n"))
                    while confirm_option != 1 and confirm_option != 2:
                        confirm_option = int(input('invalid option please choose 1 or 2\n'))
                    if confirm_option == 1:
                        mycursor.execute(
                            "UPDATE books SET status = 'brw' WHERE title = %s;", (enter_title, )
                        )
                        mycursor.execute(
                            "UPDATE books SET user = %s WHERE title = %s;", (active_member, enter_title, )
                        )
                        print(f"Book '{enter_title}' have been successfully borrowed by user {active_member.card_id} ")
                        print(f"Thank you for choosing our library")
                    elif confirm_option == 2:
                        print(f"Thank you for choosing our library")
                        search_or_exit = int(input(f"1) Search again 2) Exit\n"))
                        while search_or_exit != 1 and search_or_exit != 2:
                            search_or_exit = int(
                                input(f"Please choose option 1 or 2'\n"))
                        if search_or_exit == 1:
                            print(self.borrowBook())
                        elif search_or_exit == 2:
                            print(f"Thank you for choosing our library")
                elif status == 'brw':
                    print(f"We are sorry but this book is now borrowed")
            elif confirm_search == 2:
                print(f"If this is not what are you looking for check if you enter title correctly or try another phrase.There is also possibility we do not have book you are looking for.")
                print(self.borrowBook())
        elif mycursor.fetchone() == None:
            print(f"No records match given title.Try different one")

    def bringBackBook(self):
        print(f"To return book please enter book title below")
        returned_book = str(input(f"Book title: "))
        mycursor.execute(
            "SELECT user FROM books WHERE title = %s;", (returned_book, )
        )
        if mycursor.fetchone() != None:
            if mycursor.fetchone()[0] == active_member:
                print(f"Place book on the bookcase below screen")
                mycursor.execute(
                    "UPDATE books SET user = NULL WHERE title = %s;", (returned_book, )
                )
                mycursor.execute(
                    "UPDATE books SET status = 'avl' WHERE title = %s;", (returned_book, )
                )
                print(f"Book {returned_book} have been successfully returned.Thank you for choosing our library")
            else:
                print(f"This book is borrowed by somebody else you cannot return it")
        elif mycursor.fetchone() == None:
            print(f"No book with such title registered on user {active_member} account")

    def showBorrowedBooks(self):
        print(f"Holded books amount")
        return self.numb_of_books
                    
while True:
    print(f"Please choose option")
    login_or_register = int(input(f"1) I am registered user 2) I want to become member\n"))
    while login_or_register != 1 and login_or_register != 2:
        login_or_register = int(input(f"Please choose option 1 or 2 "))
    if login_or_register == 1:
        verify_card = str(input(f"Enter card number: "))
        mycursor.execute(
            "SELECT books_amount FROM users WHERE EXISTS (SELECT card_id FROM users WHERE card_id = %s);", (verify_card, )
        )
        if mycursor.fetchone() == None:
            print(f"No such member.Please try again")
        else:
            card_id = verify_card
            numb_of_books = mycursor.fetchone()[0]
            active_member = System(card_id, numb_of_books)

        option = int(input(f"1) Show book availability\n2) Borrow book\n3) Return book\n4) See borrowed books amount\n"))
        while option != 1 and option != 2 and option != 3 and option != 4:
            option = int(input(f"Invalid number. Please choose option from 1-4\n"))
        if option == 1:
            print(active_member.showAvailability())
        elif option == 2:
            print(active_member.borrowBook())
        elif option == 3:
            print(active_member.bringBackBook())
        elif option == 4:
            print(active_member.showBorrowedBooks())
    
    elif login_or_register == 2:
        print(f"Please fill personal data to become library member and got unique identifier")
        name = str(input(f'Name: '))
        print(f"Please note that you have to be minimum 13 years old to become member")
        age = int(input(f'Age: '))
        if age < 13:
            print(f"You cannot become library member.Age does not meet our requirements")
        else:
            code = name[0]
            numbers = age
            current_books = 0
            numbs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            last_numb = choice(numbs)
            identifier = str(code) + str(numbers) + str(last_numb)
            identifier = str(identifier)
            mycursor.execute(
                "INSERT INTO users(card_id, books_amount) VALUES (%s, %s)",
                (identifier, current_books)
            )
            print(f"Membership was successfully created your id number is {identifier} if you want to order card please go to the reception and ask for card generation")
            print(f"Thank you for choosing our library")



