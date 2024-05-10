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
    reset_stats,
    delete_user
)

import time
from termcolor import colored, cprint

page_break_bottom = "---------------------------------------------------------------------------------"
page_break_tl = "----------------------------------| "
page_break_tr = " |----------------------------------"

def main():
    logged_in = False
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
            menu(logged_in)
            choice = input("> ")
            if choice == "00":
                exit_program()
            elif choice == "1":
                data = login()
                logged_in = data[0]
                username = data[1]

#MAIN MENU -----------------------------------------------------------------------------
        else:
            menu(logged_in)
            choice = input("> ")
            if choice == "00":
                exit_program()
            elif choice == "0":
                logged_in = False
                username = None
###TEST MENU ------------------------------------
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

###STATS MENU ------------------------------------
            elif choice == "3":
                profile(username)
                profile_menu()
                choice = input("> ")
                if(choice == "1"):
                    username = change_name(username)
                elif(choice == "2"):
                    reset_stats(username)
                elif(choice == "3"):
                    delete_user(username)
                    logged_in = False
                    username = None
                elif(choice == ""):
                    cprint("Navigating...""\n", "dark_grey")                    
                else:
                    cprint("Invalid choice""\n", "red")
            else:
                cprint("Invalid choice""\n", "red")

#CLI MENU ----------------------------------------------------------------------------------
def menu(logged_in):
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
        cprint("\n"f"{page_break_bottom}", "light_magenta")

#STATS MENU ----------------------------------------------------------------------------------
def profile_menu():
    cprint("Select an option below:" "\n", "light_blue")
    print("1. Change username")
    print("2. Reset statistics")
    print("3. Delete profile")
    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    cprint("\n"f"{page_break_bottom}""\n", "light_magenta")

#TEST MENU ------------------------------------------------------------------------------------
def test_menu():
    cprint("\n"f"{page_break_tl}Typewell{page_break_tr}""\n", "light_magenta")
    print("TASK: Type the presented sentence as quickly, and as accurately as possible.""\n")
    cprint("Select an option below:" "\n", "light_blue")
    print("1. Begin test")
    print("2. View sentences")
    print("3. Add a sentence")
    cprint("\n""Press ENTER to return to the menu...", "light_blue")
    cprint("\n"f"{page_break_bottom}""\n", "light_magenta")

if __name__ == "__main__":
    main()
