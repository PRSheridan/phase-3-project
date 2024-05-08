# lib/cli.py
#python3 -m pip install --upgrade termcolor
import time
from termcolor import colored, cprint

from helpers import (
    exit_program,
    login,
    begin_test,
    leaderboard,
    stats,
    change_name,
    reset_stats,
    delete_user
)

page_break_bottom = "---------------------------------------------------------------------------------"
page_break_tl = "----------------------------------| "
page_break_tr = " |----------------------------------"

def main():
    logged_in = False
    username = None
    while True:

#LOGIN SCREEN -------------------------------------------------------------------------
        if (logged_in == False):
            print("Initializing...")
            time.sleep(1)
            cprint("\n"f"{page_break_tl}GAMENAME{page_break_tr}""\n", "light_magenta")
            cprint(
                '            GAMENAME is designed to test a subjects typing ability.'
                '\n' '          Each test measures speed, and accuracy and provides the subject'
                '\n' '          with a final score to be compared with others in the leaderboard.'
                )
            cprint("\n" f"{page_break_bottom}", "light_magenta")
            menu(logged_in)
            choice = input("> ")
            if choice == "0":
                exit_program()
            elif choice == "1":
                username = login()
                logged_in = True

#MAIN MENU -----------------------------------------------------------------------------
        else:
            menu(logged_in)
            choice = input("> ")
            if choice == "0":
                exit_program()
            elif choice == "00":
                logged_in = False
                username = None

##BEGIN GAME -----------------------------------------------------------------------------
            elif choice == "1":
                begin_test(username)

##LEADERBOARD ----------------------------------------------------------------------------
            elif choice == "2":
                leaderboard()

#STATISTICS MENU ------------------------------------------------------------------------
            elif choice == "3":
                stats(username)
                stats_menu()
                choice = input("> ")

##CHANGE USERNAME ------------------------------------------------------------------------
                if(choice == "1"):
                    username = change_name(username)
                    print(f"Username has been changed to: {username}")

##RESET STATS ----------------------------------------------------------------------------
                elif(choice == "2"):
                    reset_stats(username)
                    print("Statistics reset")

##DELETE USER ----------------------------------------------------------------------------
                elif(choice == "3"):
                    delete_user(username)
                    logged_in = False
                    username = None
                elif(choice == "0"):
                    print("Navigating...")
                else:
                    print("Invalid choice")
            else:
                print("Invalid choice")
#CLI MENU ----------------------------------------------------------------------------------
def menu(logged_in):
    if (logged_in == False):
        cprint("\n" "Login to continue:" "\n", "light_blue")
        print("1. Login")
        print("0. Quit")
    else:
        cprint("Select an option below:" "\n", "light_blue")
        cprint("1. Test")
        cprint("2. Leaderboard")
        cprint("3. Statistics")
        cprint("00. Logout")
        cprint("0. Quit")
        cprint("\n"f"{page_break_bottom}", "light_magenta")

#STATS MENU ----------------------------------------------------------------------------------
def stats_menu():
    cprint("Select an option below:" "\n", "light_blue")
    cprint("1. Change username")
    cprint("2. Reset stats")
    cprint("3. Delete User")
    cprint("0. Back")

if __name__ == "__main__":
    main()
