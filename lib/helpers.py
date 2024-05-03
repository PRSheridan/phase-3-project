# lib/helpers.py
from models.sentence import Sentence
from models.test import Test
from models.user import User

def login():
    login = True
    username = input("Please enter a unique username: ")
    if current_user := User.find_by_name(username):
        print(f'Welcome back, {username}.')
    else:
        try:
            User.create(username)
            print(f'New profile created, welcome {username}.')
        except Exception as exc:
            print("Error creating new profile:", exc)
    return username

def begin_test():
    print("Beginning test: ")


def stats(username):
    user = User.find_by_name(username)
    if all_tests := Test.find_by_user_id(user.id):
        total_tests = len(all_tests)
        total_time = 0
        total_accuracy = 0
        for test in all_tests:
            total_time += test.time
            total_accuracy += test.accuracy

        print(f"STATS: {username}")
        print(f"Tests taken: {total_tests}")
        print(f"Average time: {total_time/total_tests}")
        print(f"Average accuracy: {total_accuracy/total_tests}")
    else:
        print("User has no statistics")

def change_name(username):
    user = User.find_by_name(username)
    user.name = input("Please enter a new unique username: ")
    user.update()
    return user.name


def exit_program():
    print("Shutting down testing chamber...")
    exit()
