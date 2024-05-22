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
    # 0LOGGED_IN, 1ADMIN, 2USERNAME
    data = [False, "", ""]
    data[2] = input("\n" "Enter your username: ")
    if current_user := User.find_by_name(data[2]):
        cprint("Initializing...", "dark_grey")
        time.sleep(.5)
        print("\n"f'Welcome back, {data[2]}.'"\n")
        time.sleep(1)
        if current_user.role == 'admin':
            data[1] = True
        else:
            data[1] = False
        data[0] = True
        return data
    else:
        try:
            if "adm_" in data[2]:
                User.create(data[2], "admin")
                cprint("Initializing...", "dark_grey")
                time.sleep(.5)
                print(f'New ADMIN profile created, welcome {data[2]}.')
                data[0] = True
                data[1] = True
                return data
            else:
                User.create(data[2], "basic")
                cprint("Initializing...", "dark_grey")
                time.sleep(.5)
                print(f'New profile created, welcome {data[2]}.')
                data[0] = True
                return data
            cprint("Initializing...", "dark_grey")
            time.sleep(.5)
        except Exception as exc:
            print("Error creating new profile:", exc)
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
    # Split by word, add placeholder for missing words,
    # compare words length and add # for each missing/extra letter.
    test_string_length = len(test_string)
    test_words = test_string.split(" ")
    user_words = user_input.split(" ")
    if len(test_words) > len(user_words):
        for i in range((len(test_words)-len(user_words))):
            user_words.append("#")
    elif len(test_words) < len(user_words):
        for i in range((len(user_words)-len(test_words))):
            user_words.append("#")
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

# Prompt for test index and display test stats
def history(username):
    current_user = User.find_by_name(username)
    if tests := current_user.tests():
        print(f"You have {len(tests)} tests on record."
        '\n' f"Input a number between 1 and {len(tests)} to view test results: ")
        choice = input("> ")
        if 1 <= int(choice) <= len(tests):
            test = Test.find_by_id(int(choice))
            sentence = Sentence.find_by_id(test.sentence_id)
            cprint('\n'f"Test {choice}",attrs=["underline"])
            cprint(f"Sentence:   {sentence.string}"
            '\n' f"User Input: {test.user_input}"
            '\n''\n' f"WPM: ------ {test.wpm}"
            '\n' f"Time: ----- {test.time}"
            '\n' f"Accuracy: - {test.accuracy}",attrs=["bold"])
        else:
            cprint(f"Test index out of range.", "red")
    else:
        cprint(f"No stats found.", "red")

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

#ADMIN CONSOLE ------------------------------------------------------------------------------------------
# Display options for admin > users
def user_admin_menu():
    cprint("Select an option below:" "\n", "light_green")
    print("1. View users")
    print("2. Edit user")
    print("3. Create user")
    print("4. Delete user")
    cprint("\n""Press ENTER to return to the menu...", "light_green")
    cprint("\n"f"{page_break_bottom}", "light_magenta")
    choice = input("> ")

# View all User instances
    if choice == "1":
        cprint("\n"f"{page_break_tl}USERS{page_break_tr}""\n", "light_magenta")
        for user in User.get_all():
            cprint(f"{user.id}. {user.name} ({user.role})")
        cprint("\n""Press ENTER to return to the menu...", "light_green")
        input("> ""\n")

# Edit an existing User instance's username and role
    elif choice == "2":
        cprint("Enter the username below: ", "light_green")
        if current_user := User.find_by_name(input("> ")):
            cprint(f"Select an option for {current_user.name} below:" "\n", "light_green")
            print("1. Change username")
            print("2. Change role")
            cprint("\n""Press ENTER to return to the menu...", "light_green")
            temp = input("> ")
            if temp == "1":
                change_name(current_user.name)
            elif temp == "2":
                cprint(f"Select a role for {current_user.name} below:" "\n", "light_green")
                print("1. basic")
                print("2. admin")
                cprint("\n""Press ENTER to return to the menu...", "light_green")
                temp = input("> ")
                if temp == "1":
                    current_user.role = "basic"
                    current_user.update()
                elif temp == "2":
                    current_user.role = "admin"
                    current_user.update()
                elif choice == "":
                    cprint("Returning to menu...", "dark_grey")
                else:
                    cprint("Invalid choice.", "red")
        else:
            cprint("User does not exist.", "red")

# Create a new User instance by entering a username and chosing role
    elif choice == "3":
        data = ["", ""]
        cprint(f"Enter a unique username below:" "\n", "light_green")
        data[0] = input("> ")
        if current_user := User.find_by_name(data[0]):
            cprint(f"{current_user.name} already exists. Returning to menu...", "dark_grey")
        else:
            cprint(f"Select a role for {data[0]} below:" "\n", "light_green")
            print("1. basic")
            print("2. admin")
            temp = input("> ")
            if temp == "1":
                data[1] = "basic"
                User.create(data[0], data[1])
                print(f'New profile created: {data[0]} ({data[1]}).'"\n", "light_green")
            elif temp == "2":
                data[1] = "admin"
                User.create(data[0], data[1])
                print(f'New ADMIN profile created: {data[0]} ({data[1]}).'"\n", "light_green")
            elif choice == "":
                cprint("Returning to menu...", "dark_grey")
            else:
                cprint("Invalid choice.", "red")

# Delete a User instance
    elif choice == "4":
        cprint("Enter the username below: ", "light_green")
        if current_user := User.find_by_name(input("> ")):
            confirm = input("\n" "Type Y/N to confirm deletion: ")
            if confirm == "Y":
                current_user.delete()
                cprint("User account terminated", "red")
            else:
                cprint("Action cancelled", "dark_grey")
        else:
            cprint("User does not exist. Returning to menu...", "red")

    elif choice == "":
        cprint("Returning to menu...", "dark_grey")
    else:
        cprint("Invalid choice.", "red")

# Display options for admin > tests
def test_admin_menu():
    cprint("Select an option below:" "\n", "light_green")
    print("1. View all tests")
    print("2. View tests by user")
    print("3. Edit test")
    print("4. Create test")
    print("5. Delete test")
    cprint("\n""Press ENTER to return to the menu...", "light_green")
    cprint("\n"f"{page_break_bottom}", "light_magenta")
    choice = input("> ")

# View all Test instances
    if choice == "1":
        for test in Test.get_all():
            sentence = Sentence.find_by_id(test.sentence_id)
            user = User.find_by_id(test.user_id)
            cprint('\n'f"Test {test.id}: {user.name}",attrs=["underline"])
            cprint(f"Sentence:   {sentence.string}"
            '\n' f"User Input: {test.user_input}"
            '\n''\n' f"WPM: ------ {test.wpm}"
            '\n' f"Time: ----- {test.time}"
            '\n' f"Accuracy: - {test.accuracy}",attrs=["bold"])
        cprint("\n""Press ENTER to return to the menu...", "light_green")
        input("> ")

# View all Test instances by a specified user
    elif choice == "2":
        cprint("Enter the username below: ", "light_green")
        if current_user := User.find_by_name(input("> ")):
            for test in current_user.tests():
                sentence = Sentence.find_by_id(test.sentence_id)
                cprint('\n'f"Test {test.id}: {current_user.name}",attrs=["underline"])
                cprint(f"Sentence:   {sentence.string}"
                '\n' f"User Input: {test.user_input}"
                '\n''\n' f"WPM: ------ {test.wpm}"
                '\n' f"Time: ----- {test.time}"
                '\n' f"Accuracy: - {test.accuracy}",attrs=["bold"])
            cprint("\n""Press ENTER to return to the menu...", "light_green")
            input("> ")

# Edit an existing Test instance's WPM, time, accuracy, or user
    elif choice == "3":
        cprint("Enter the test ID below: ", "light_green")
        if test := Test.find_by_id(input("> ")):
            cprint(f"Select an option for test {test.id} below:" "\n", "light_green")
            print("1. Change WPM")
            print("2. Change time")
            print("3. Change accuracy")
            print("4. Change user")
            cprint("\n""Press ENTER to return to the menu...", "light_green")
            cprint("\n"f"{page_break_bottom}", "light_magenta")
            choice = input("> ")
            if choice == "1":
                cprint("Enter the new wpm value below: ", "light_green")
                test.wpm = input("> ")
                test.update()
                cprint(f"Test {test.id} wpm set to {test.wpm}.", "light_green")
            if choice == "2":
                cprint("Enter the new time value below: ", "light_green")
                test.time = input("> ")
                test.update()
                cprint(f"Test {test.id} time set to {test.time}.", "light_green")
            if choice == "3":
                cprint("Enter the new accuracy value below: ", "light_green")
                test.accuracy = input("> ")
                test.update()
                cprint(f"Test {test.id} accuracy set to {test.accuracy}.", "light_green")
            if choice == "4":
                cprint("Enter the new user ID below: ", "light_green")
                test.user_id = input("> ")
                test.update()
                cprint(f"Test {test.id} user ID set to {test.user_id}.", "light_green")
        else:
            cprint(f"Test does not exist. Returning to menu...", "red")

# Create a new Test instance
    elif choice == "4":
        test_temp = ["", "", "", "", "", ""]
        cprint("Enter the time value below: ", "light_green")
        test_temp[0] = input("> ")
        cprint("Enter the accuracy value below: ", "light_green")
        test_temp[1] = input("> ")
        cprint("Enter the wpm value below: ", "light_green")
        test_temp[2] = input("> ")
        cprint("Enter the user ID value below: ", "light_green")
        test_temp[3] = input("> ")
        cprint("Enter the sentence ID value below: ", "light_green")
        test_temp[4] = input("> ")
        cprint(f"Sentence: {Sentence.find_by_id(test_temp[4]).string}", "light_green")
        cprint("Enter the user input value below: ", "light_green")
        test_temp[5] = input("> ")
        try:
            test = Test.create(test_temp[5], test_temp[0], test_temp[1], test_temp[2], test_temp[3], test_temp[4])
            sentence = Sentence.find_by_id(test.sentence_id)
            current_user = User.find_by_id(test.user_id)
            cprint('\n'f"Test created: ",attrs=["underline"])
            cprint(f"Sentence:   {sentence.string}"
            '\n' f"User Input: {test.user_input}"
            '\n''\n' f"WPM: ------ {test.wpm}"
            '\n' f"Time: ----- {test.time}"
            '\n' f"Accuracy: - {test.accuracy}",attrs=["bold"])
            cprint("\n""Press ENTER to return to the menu...", "light_green")
            input("> ")
        except Exception as exc:
            print("Error creating new test:", exc)

# Delete a Test instance
    elif choice == "5":
        cprint("Enter the test ID below: ", "light_green")
        if test := Test.find_by_id(input("> ")):
            test.delete()
            cprint("Test Deleted", "light_green")
        else:
            cprint(f"Test does not exist. Returning to menu...", "red")
    elif choice == "":
        cprint("Returning to menu...", "dark_grey")
    else:
        cprint("Invalid choice.", "red")
