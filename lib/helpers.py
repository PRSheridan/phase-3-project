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
        cprint("Initializing...", "dark_grey")
        time.sleep(.5)
        print("\n"f'Welcome back, {username}.'"\n")
        time.sleep(1)
    else:
        try:
            User.create(username)
            cprint("Initializing...", "dark_grey")
            time.sleep(.8)
            print(f'New profile created, welcome {username}.')
        except Exception as exc:
            print("Error creating new profile:", exc)
    login = True
    return username

# Countdown to test, and initialize test instance
def begin_test(username):
    cprint("\n""3...", "red")
    time.sleep(1)
    cprint("\n""2...", "yellow")
    time.sleep(1)
    cprint("\n""1...", "white")
    time.sleep(1)
    cprint("\n""GO""\n", "green")
    test(username)

# List all current sentence instances
def show_sentences():
    cprint("\n"f"{page_break_tl}SENTENCES{page_break_tr}""\n", "light_magenta")
    sentences = Sentence.get_all()
    for sentence in sentences:
        cprint(sentence.string)
    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    input("> ""\n")

# Create a new sentence instance
def add_sentence():
    cprint("\n""A new sentence cannot contain numbers, and should not contain any punctuation.")
    cprint("Enter a new sentence below (Enter nothing to cancel):", "light_blue")
    new_string = input("> ")
    if new_string == "":
        return new_string
    try:
        Sentence.create(new_string)
        cprint("Initializing...""\n", "dark_grey")
        time.sleep(.5)
        cprint(f"New sentence, \"{new_string}\" has been added.""\n", "light_green")
    except Exception as exc:
        print("\n""Error creating new sentence:", exc)

# Select a random test sentence, start a timer, prompt input, end timer 
# Calculate final_time, accuracy, and final_score; create a new test with data
def test(username):
    user = User.find_by_name(username)
    sentences = Sentence.get_all()
    test_sentence = sentences[random.randint(0, (len(sentences)-1))]
    word_count = len(test_sentence.string.split())
    cprint(f"{test_sentence.string}""\n", "yellow", attrs=["bold", "underline"])
    time.sleep(.2)
    start = time.time()
    test_answer = input()
    end = time.time()

    final_time = round((end - start), 1)
    misses = sum(1 for a, b in zip(test_sentence.string, test_answer) if a != b)
    accuracy = round((((len(test_sentence.string)-misses)/(len(test_sentence.string)))*100), 1)
    wpm = round(((word_count * 60)/final_time), 1)
    
    #final score weight adjusted for sentence length: midpoint ~25 characters
    final_score = accuracy/final_time
    final_score = round(((final_score * (100+(len(test_sentence.string)*1.5)))/100), 1)
    
    cprint("\n""      Test Results:      ""\n", attrs=["underline"])
    print(f"     score: {final_score} points")
    print(f"       WPM: {wpm} WPM")
    print(f"      time: {final_time}s")
    print(f"  accuracy: {accuracy}%")
    Test.create(test_answer, final_time, accuracy, wpm, final_score, user.id, test_sentence.id)
    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    input("> ")

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
                "avg_wpm": 0,
                "avg_score": 0
            })

    sorted_data = sorted(leaderboard_data, key=lambda x: x['avg_score'], reverse = True)   
    index = 1 
    for user in sorted_data:
        cprint(f"                        [{index}]. {user['username']}: Average Score: {round(user['avg_score'], 1)}", attrs=["bold"])
        index+=1
    cprint("\n"f"{page_break_bottom}""\n", "light_magenta")
    cprint("Press ENTER to return to the menu...", "light_blue")
    input("> ""\n")

# Display the average stats and number of tests taken of the current user
def profile(username):
    cprint("\n"f"{page_break_tl}{username.upper()}{page_break_tr}""\n", "light_magenta")
    user = User.find_by_name(username)
    if all_tests := Test.find_by_user_id(user.id):
        temp_stats = calculate_stats(username)
        cprint(f"                                 Tests taken: {temp_stats['total_tests']}"
        '\n' f"                               Average score: {round(temp_stats['avg_score'], 1)}"
        '\n' f"                                 Average WPM: {round(temp_stats['avg_wpm'], 1)}"
        '\n' f"                                Average time: {round(temp_stats['avg_time'], 1)}"
        '\n' f"                            Average accuracy: {round(temp_stats['avg_accuracy'], 1)}""\n"
        ,attrs=["bold"])
    else:
        cprint(f"No stats found.", "red")

# Prompt the user for a new username and update
def change_name(username):
    current_user = User.find_by_name(username)
    cprint("Enter a new unique username (Enter nothing to cancel): ", "light_blue")
    new_name = input("> ")
    if new_name == "":
        return username
    users = User.get_all()
    for this_user in users:
        if this_user.name == new_name:
            cprint(f"Username {new_name} already taken", "red")
            return username
    user.name = new_name
    current_user.update()
    cprint(f"Username has been changed to: {user.name}", "light_green")
    return user.name
    #cancelling breaks profile page...

# Delete all previous tests of user.id
def reset_stats(username):
    user = User.find_by_name(username)
    if all_tests := Test.find_by_user_id(user.id):
        for test in all_tests:
            test.delete()
        cprint("Statistics reset", "red")
    
# Prompt for confirmation and delete user 
def delete_user(username):
    user = User.find_by_name(username)
    confirm = input("\n" "Type Y/N to confirm deletion: ")
    if confirm == "Y":
        user.delete()
        cprint("User Account Terminated", "red")
    else:
        cprint("Action Cancelled", "dark_grey")

def exit_program():
    cprint("\n" "Shutting down testing chamber...", "red")
    exit()

# Calculate average time, accuracy, and score for stats page: return a dict
def calculate_stats(username):
    stats = {
        "username": username,
        "total_tests": 0,
        "avg_time": 0,
        "avg_accuracy": 0,
        "avg_wpm": 0,
        "avg_score": 0
    }
 
    current_user = User.find_by_name(username)
    stats["total_tests"] = len(current_user.tests())
    stats["avg_time"] = current_user.avg_time()
    stats["avg_accuracy"] = current_user.avg_accuracy()
    stats["avg_wpm"] = current_user.avg_wpm()
    stats["avg_score"] = current_user.avg_score()
    return stats