# lib/helpers.py
from models.sentence import Sentence
from models.test import Test
from models.user import User

import time
import random

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

def begin_test(username):
    print("--------------------------------| INITIALIZING |--------------------------------")
    print("")
    print("TASK: Type the presented sentence as quickly, and as accurately as possible.")
    print("")
    input("Press enter to begin: ")
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("GO")
    test(username)

def test(username):
    user = User.find_by_name(username)
    sentences = Sentence.get_all()
    test_sentence = sentences[random.randint(0, (len(sentences)-1))]

    print(test_sentence.string)
    time.sleep(.2)
    start = time.time()
    test_answer = input()
    end = time.time()
    final_time = round((end - start), 1)

    misses = sum(1 for a, b in zip(test_sentence.string, test_answer) if a != b)
    accuracy = round((((len(test_sentence.string)-misses)/(len(test_sentence.string)))*100), 1)

    print(f"time: {final_time}s")
    print(f"accuracy: {accuracy}%")
    Test.create(test_answer, final_time, accuracy, user.id, test_sentence.id)


def leaderboard():
    print("--------------------------------| LEADERBOARD |--------------------------------")
    leaderboard_data = []
    users = User.get_all()
    for user in users:
        if all_tests := Test.find_by_user_id(user.id):
            leaderboard_data.append(calculate_stats(user.name))
        else:
            leaderboard_data.append({
                "username": user.name,
                "total_tests": 0,
                "avg_time": 999,
                "avg_accuracy": 999,
            })

    sorted_data = sorted(leaderboard_data, key=lambda x: x['avg_time'])   
    index = 1 
    for user in sorted_data:
        print(f"{index}. {user['username']}: Average Time: {round(user['avg_time'], 1)}")
        index+=1
    print("-------------------------------------------------------------------------------")


def stats(username):
    print(f"--------------------------------| {username} Statistics |--------------------------------")
    user = User.find_by_name(username)
    if all_tests := Test.find_by_user_id(user.id):
        temp_stats = calculate_stats(username)
        print(f"Tests taken: {temp_stats['total_tests']}")
        print(f"Average time: {round(temp_stats['avg_time'], 1)}")
        print(f"Average accuracy: {round(temp_stats['avg_accuracy'], 1)}")
    else:
        print(f"No stats found.")
    print("----------------------------------------------------------------------------------------")

def change_name(username):
    user = User.find_by_name(username)
    user.name = input("Please enter a new unique username: ")
    user.update()
    return user.name

def reset_stats(username):
    user = User.find_by_name(username)
    if all_tests := Test.find_by_user_id(user.id):
        for test in all_tests:
            test.delete()
    

def delete_user(username):
    user = User.find_by_name(username)
    confirm = input("Type Y/N to confirm deletion: ")
    if confirm == "Y":
        user.delete()
        print("User Account Terminated")
    else:
        print("Action Cancelled")

def exit_program():
    print("Shutting down testing chamber...")
    exit()

#Helpers Helpers
def calculate_stats(username):
    stats = {
        "username": username,
        "total_tests": 0,
        "avg_time": 0,
        "avg_accuracy": 0,
    }

    user = User.find_by_name(username)
    if all_tests := Test.find_by_user_id(user.id):
        stats["total_tests"] = len(all_tests)
        total_time = 0
        total_accuracy = 0
        for test in all_tests:
            total_time += test.time
            total_accuracy += test.accuracy

        stats["avg_time"] = total_time / stats["total_tests"]
        stats["avg_accuracy"] = total_accuracy / stats["total_tests"]
        return stats

#work on scoring system?