# lib/helpers.py
from models.sentence import Sentence
from models.test import Test
from models.user import User

def login():
    login = True
    username = input("Please provide a unique username: ")
    if current_user := User.find_by_name(username):
        print(f'Welcome back, {username}.')
    else:
        try:
            User.create(username)
            print(f'New profile created, welcome {username}.')
        except Exception as exc:
            print("Error creating new profile:", exc)


def begin_test():
    print("Beginning test: ")
    print("")

def user_info():
    print(username)


def exit_program():
    print("Shutting down testing chamber...")
    exit()
