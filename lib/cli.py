#!/usr/bin/env python3
# lib/cli.py
#python3 -m pip install --upgrade termcolor

from helpers import (
    exit_program,
    login,
    begin_test,
    show_sentences,
    add_sentence,
    leaderboard,
    profile,
    change_name,
    history,
    reset_stats,
    delete_user,
    user_admin_menu,
    test_admin_menu
)

import time
from termcolor import colored, cprint

page_break_bottom = "---------------------------------------------------------------------------------"
page_break_tl = "----------------------------------| "
page_break_tr = " |----------------------------------"

def main():
    logged_in = False
    admin = False
    username = None
    while True:

#LOGIN SCREEN -------------------------------------------------------------------------
        if (logged_in == False):
            cprint("Initializing...", "dark_grey")
            time.sleep(.5)
            cprint("\n"f"{page_break_tl}Typewell{page_break_tr}""\n", "light_magenta")
            cprint(
                '            Typewell is designed to test a subjects typing ability.'
                '\n' '          Each test measures speed, and accuracy and provides the subject'
                '\n' '          with a final wpm to be compared with others in the leaderboard.'
                )
            cprint("\n" f"{page_break_bottom}", "light_magenta")
            menu(logged_in, admin)
            choice = input("> ")
            if choice == "00":
                exit_program()
            elif choice == "1":
                data = login()
                logged_in = data[0]
                admin = data[1]
                username = data[2]
            else:
                cprint("Invalid choice.", "red")

#MAIN MENU -----------------------------------------------------------------------------
        else:
            menu(logged_in, admin)
            choice = input("> ")
            if choice == "00":
                exit_program()
            elif choice == "0":
                logged_in = False
                admin = False
                username = None
###TEST MENU ------------------------------------
            elif choice == "admin" and admin == True:
                admin_menu()
                choice = input("> ")
                if choice == "1":
                    user_admin_menu()
                elif choice == "2":
                    test_admin_menu()
                elif choice == "":
                    cprint("Returning to menu...", "dark_grey")
                else:
                    cprint("Invalid choice.", "red")
            elif choice == "1":
                test_menu()
                choice = input("> ")
                if choice == "1":
                    begin_test(username)
                elif choice == "2":
                    show_sentences()
                elif choice == "3":
                    add_sentence()
                elif choice == "":
                    cprint("Returning to menu...", "dark_grey")
                else:
                    cprint("Invalid choice.", "red")
            elif choice == "2":
                leaderboard()

###PROFILE MENU ------------------------------------
            elif choice == "3":
                profile(username)
                profile_menu()
                choice = input("> ")
                if(choice == "1"):
                    username = change_name(username)
                elif(choice == "2"):
                    history(username)
                elif(choice == "3"):
                    reset_stats(username)
                elif(choice == "4"):
                    delete_user(username)
                    logged_in = False
                    admin = False
                    username = None
                elif(choice == ""):
                    cprint("Navigating...""\n", "dark_grey")                    
                else:
                    cprint("Invalid choice""\n", "red")
            else:
                cprint("Invalid choice""\n", "red")

#CLI MENU ----------------------------------------------------------------------------------
def menu(logged_in, admin):
    if (logged_in == False):
        cprint("\n" "Login to continue:" "\n", "light_blue")
        print("1. Login")
        print("00. Quit")
    else:
        cprint(f"{page_break_tl}Typewell{page_break_tr}""\n", "light_magenta")
        cprint("Select an option below:" "\n", "light_blue")
        print("1. Test")
        print("2. Leaderboard")
        print("3. Profile")
        print("0. Logout")
        print("00. Quit")
        if(admin == True):
            cprint("\n""admin. Admin Console", "light_green")
        cprint("\n"f"{page_break_bottom}", "light_magenta")

#PROFILE MENU ----------------------------------------------------------------------------------
def profile_menu():
    cprint("Select an option below:" "\n", "light_blue")
    print("1. Change username")
    print("2. View history")
    print("3. Reset statistics")
    print("4. Delete profile")
    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    cprint("\n"f"{page_break_bottom}", "light_magenta")

#TEST MENU ------------------------------------------------------------------------------------
def test_menu():
    cprint("\n"f"{page_break_tl}Typewell{page_break_tr}""\n", "light_magenta")
    print("TASK: Type the presented sentence as quickly, and as accurately as possible.""\n")
    cprint("Select an option below:" "\n", "light_blue")
    print("1. Begin test")
    print("2. View sentences")
    print("3. Add a sentence")
    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    cprint("\n"f"{page_break_bottom}", "light_magenta")

def admin_menu():
    cprint("Select an option below:" "\n", "light_green")
    print("1. Users")
    print("2. Tests")
    cprint("\n""Press ENTER to return to the menu...", "light_green")
    cprint("\n"f"{page_break_bottom}", "light_magenta")
if __name__ == "__main__":
    main()
