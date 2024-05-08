# lib/helpers.py
from models.sentence import Sentence
from models.test import Test
from models.user import User

import time
import random
from termcolor import colored, cprint

page_break_bottom = "-------------------------------------------------------------------------------"
page_break_tl = "----------------------------------| "
page_break_tr = " |----------------------------------"

# Prompt the user for a username: if not registered, create a new user: return username
def login():
    username = input("\n" "Enter your username: ")
    if current_user := User.find_by_name(username):
        print("Initializing...")
        time.sleep(1)
        cprint(f"{page_break_tl}Placeholder{page_break_tr}""\n", "light_magenta")
        print(f'Welcome back, {username}.')
    else:
        try:
            User.create(username)
            print("Initializing...")
            time.sleep(1)
            print(f'New profile created, welcome {username}.')
        except Exception as exc:
            print("Error creating new profile:", exc)
    login = True
    return username

# Confirmation and countdown to testing
def begin_test(username):
    cprint("\n"f"{page_break_tl}INITIALIZING{page_break_tr}""\n", "light_magenta")
    print("TASK: Type the presented sentence as quickly, and as accurately as possible.""\n")
    print("1. Begin test")
    print("0. Back")
    confirmation = input("> ")
    if confirmation == "1":
        cprint("\n""3...", "red")
        time.sleep(1)
        cprint("\n""2...", "yellow")
        time.sleep(1)
        cprint("\n""1...", "white")
        time.sleep(1)
        cprint("\n""GO""\n", "green")
        test(username)
    elif confirmation == "0":
        print("Returning to menu...")

# Select a random test sentence, start a timer, prompt input, end timer 
# Calculate final_time, accuracy, and final_score; create a new test with data
def test(username):
    user = User.find_by_name(username)
    sentences = Sentence.get_all()
    test_sentence = sentences[random.randint(0, (len(sentences)-1))]

    cprint(f"{test_sentence.string}""\n", "yellow", attrs=["bold", "underline"])
    time.sleep(.2)
    start = time.time()
    test_answer = input()
    end = time.time()
    final_time = round((end - start), 1)

    misses = sum(1 for a, b in zip(test_sentence.string, test_answer) if a != b)
    accuracy = round((((len(test_sentence.string)-misses)/(len(test_sentence.string)))*100), 1)
    final_score = round((accuracy/final_time), 1)
    
    cprint("\n""      Test Results:      ""\n", attrs=["underline"])
    print(f"     score: {final_score} points")
    print(f"      time: {final_time}s")
    print(f"  accuracy: {accuracy}%")
    Test.create(test_answer, final_time, accuracy, final_score, user.id, test_sentence.id)
    input("\n""Press ENTER to return to the menu...")
    cprint("\n"f"{page_break_tl}GAMENAME{page_break_tr}""\n", "light_magenta")

# Display average scores of all users sorted best first
def leaderboard():
    cprint("\n"f"{page_break_tl}LEADERBOARD{page_break_tr}""\n", "light_magenta")
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
                "avg_score": 0
            })

    sorted_data = sorted(leaderboard_data, key=lambda x: x['avg_score'], reverse = True)   
    index = 1 
    for user in sorted_data:
        cprint(f"                        [{index}]. {user['username']}: Average Score: {round(user['avg_score'], 1)}", attrs=["bold"])
        index+=1
    cprint("\n"f"{page_break_bottom}""\n", "light_magenta")
    print("\n" "Press ENTER to return to the menu...")
    input("> ")

# Display the average stats and number of tests taken of the current user
def stats(username):
    cprint("\n"f"{page_break_tl}{username.upper()}{page_break_tr}""\n", "light_magenta")
    user = User.find_by_name(username)
    if all_tests := Test.find_by_user_id(user.id):
        temp_stats = calculate_stats(username)
        cprint(f"                                 Tests taken: {temp_stats['total_tests']}"
        '\n' f"                                Average time: {round(temp_stats['avg_time'], 1)}"
        '\n' f"                            Average accuracy: {round(temp_stats['avg_accuracy'], 1)}"
        ,attrs=["bold"])
    else:
        print(f"No stats found.")
    cprint("\n"f"{page_break_bottom}""\n", "light_magenta")

# Prompt the user for a new username and update
def change_name(username):
    user = User.find_by_name(username)
    user.name = input("\n" "Enter a new unique username: ")
    user.update()
    return user.name

# Delete all previous tests of user.id
def reset_stats(username):
    user = User.find_by_name(username)
    if all_tests := Test.find_by_user_id(user.id):
        for test in all_tests:
            test.delete()
    
# Prompt for confirmation and delete user 
def delete_user(username):
    user = User.find_by_name(username)
    confirm = input("\n" "Type Y/N to confirm deletion: ")
    if confirm == "Y":
        user.delete()
        print("User Account Terminated")
    else:
        print("Action Cancelled")

def exit_program():
    print("\n" "Shutting down testing chamber...")
    exit()

# Calculate average time, accuracy, and score for stats page: return a dict
def calculate_stats(username):
    stats = {
        "username": username,
        "total_tests": 0,
        "avg_time": 0,
        "avg_accuracy": 0,
        "avg_score": 0
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
        stats["avg_score"] = stats["avg_accuracy"]/stats["avg_time"]
        return stats