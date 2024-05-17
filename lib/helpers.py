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
    data = [False, ""]
    data[1] = input("\n" "Enter your username: ")
    if current_user := User.find_by_name(data[1]):
        cprint("Initializing...", "dark_grey")
        time.sleep(.5)
        print("\n"f'Welcome back, {data[1]}.'"\n")
        time.sleep(1)
        data[0] = True
        return data
    else:
        try:
            User.create(data[1])
            cprint("Initializing...", "dark_grey")
            time.sleep(.5)
            print(f'New profile created, welcome {data[1]}.')
            data[0] = True
            return data
        except Exception as exc:
            print("Error creating new profile:", exc)
            data[0] = False
            return data

# List all current sentence instances
def show_sentences():
    cprint("\n"f"{page_break_tl}SENTENCES{page_break_tr}""\n", "light_magenta")
    for sentence in Sentence.get_all():
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

# Countdown and call test
def begin_test(username):
    cprint("\n""3...", "red")
    time.sleep(1)
    cprint("\n""2...", "yellow")
    time.sleep(1)
    cprint("\n""1...", "white")
    time.sleep(1)
    cprint("\n""GO""\n", "green")
    test(username)
    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    input("> ")
    
# Select a random test sentence, start a timer, prompt input, end timer 
# Calculate time, accuracy, and wpm; create a new test with data
def test(username):
    # Intitialize variables for test
    user = User.find_by_name(username)
    sentences = Sentence.get_all()
    test_sentence = sentences[random.randint(0, (len(sentences)-1))]
    test_string = test_sentence.string

    # Administer test
    cprint(f"{test_string}""\n", "yellow", attrs=["bold", "underline"])
    time.sleep(.2)
    start = time.time()
    user_input = input()
    end = time.time()
    test_time = round((end - start), 1)
    
    # Calculate statistics
    # Split by word, compare words length and add # for each missing/extra letter
    test_string_length = len(test_string)
    test_words = test_string.split(" ")
    user_words = user_input.split(" ")
    for i in range(len(test_words)):
        if len(test_words[i]) > len(user_words[i]):
            user_words[i] += "#"*(len(test_words[i]) - len(user_words[i]))
        elif len(test_words[i]) < len(user_words[i]):
            test_words[i] += "#"*(len(user_words[i]) - len(test_words[i]))
    test_string = " ".join(test_words)
    user_input = " ".join(user_words)
    misses = sum(1 for a, b in zip(test_string, user_input) if a != b)
    # percent difference in sentences
    accuracy = round((((test_string_length-misses)/test_string_length)*100), 1)
    wpm = round((((test_string_length/5)/(test_time/60))*(accuracy/100)), 1)
    Test.create(user_input, test_time, accuracy, wpm, user.id, test_sentence.id)
    
    # Display test results
    cprint("\n""      Test Results:      ""\n", attrs=["underline"])
    if wpm > user.record_wpm():
        cprint(f"       WPM: {wpm} WPM (PB)", "light_yellow")
    else:
        cprint(f"       WPM: {wpm} WPM")
    print(f"      time: {test_time}s")
    print(f"  accuracy: {accuracy}%")

# Display average wpm of all users sorted best first
def leaderboard():
    cprint("\n"f"{page_break_tl}LEADERBOARD{page_break_tr}""\n", "light_magenta")
    leaderboard_data = []
    users = User.get_all()
    for user in users:
        if all_tests := user.tests():
            leaderboard_data.append(calculate_stats(user.name))
        else:
            leaderboard_data.append({
                "username": user.name,
                "total_tests": 0,
                "avg_time": 999,
                "avg_accuracy": 999,
                "avg_wpm": 0,
            })

    sorted_data = sorted(leaderboard_data, key=lambda x: x['avg_wpm'], reverse = True)   
    index = 1 
    for user in sorted_data:
        cprint(f"                        [{index}]. {user['username']}: Average WPM: {round(user['avg_wpm'], 1)}", attrs=["bold"])
        index+=1
    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    cprint("\n"f"{page_break_bottom}", "light_magenta")
    input("> ")

# Display the average stats and number of tests taken of the current user
def profile(username):
    cprint("\n"f"{page_break_tl}{username}{page_break_tr}""\n", "light_magenta")
    user = User.find_by_name(username)
    if all_tests := user.tests():
        temp_stats = calculate_stats(username)
        cprint(f"                                 Tests taken: {temp_stats['total_tests']}"
        '\n' f"                                 Average WPM: {round(temp_stats['avg_wpm'], 1)}"
        '\n' f"                                Average time: {round(temp_stats['avg_time'], 1)}"
        '\n' f"                            Average accuracy: {round(temp_stats['avg_accuracy'], 1)}""\n"
        ,attrs=["bold"])
    else:
        cprint(f"No stats found.", "red")

# Prompt the user for a new username and update
def change_name(username):
    current_user = User.find_by_name(username)
    cprint("Enter a new unique username (enter nothing to cancel): ", "light_blue")
    new_name = input("> ")
    if new_name == "":
        return username
    for user in User.get_all():
        if user.name == new_name:
            cprint(f"Username {new_name} already taken", "red")
            return username
    current_user.name = new_name
    current_user.update()
    cprint(f"Username has been changed to: {current_user.name}", "light_green")
    return new_name

def history(username):
    current_user = User.find_by_name(username)
    tests = current_user.tests()
    for test in tests:
        print(test.id)

    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    input("> ")

# Delete all previous tests of user.id
def reset_stats(username):
    current_user = User.find_by_name(username)
    if tests := current_user.tests():
        for test in tests:
            test.delete()
        cprint("Statistics reset", "red")
    
# Prompt for confirmation and delete user 
def delete_user(username):
    user = User.find_by_name(username)
    confirm = input("\n" "Type Y/N to confirm deletion: ")
    if confirm == "Y":
        user.delete()
        cprint("User account terminated", "red")
    else:
        cprint("Action cancelled", "dark_grey")

def exit_program():
    cprint("\n" "Shutting down...", "red")
    exit()

# Calculate average time, accuracy, and wpm for stats page: return a dict
def calculate_stats(username):
    stats = {
        "username": username,
        "total_tests": 0,
        "avg_time": 0,
        "avg_accuracy": 0,
        "avg_wpm": 0,
    }
 
    current_user = User.find_by_name(username)
    stats["total_tests"] = len(current_user.tests())
    stats["avg_time"] = current_user.avg_time()
    stats["avg_accuracy"] = current_user.avg_accuracy()
    stats["avg_wpm"] = current_user.avg_wpm()
    return stats