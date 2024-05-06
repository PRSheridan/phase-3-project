# lib/cli.py

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

def main():
    logged_in = False
    username = None
    while True:

#LOGIN SCREEN -------------------------------------------------------------------------
        if (logged_in == False):
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
        print("Please login to continue:")
        print("1. Login")
        print("0. Quit")
    else:
        print("--------------------------------| Placeholder Name |--------------------------------")
        print("Please select an option:")
        print("1. Begin test")
        print("2. Leaderboard")
        print("3. Statistics")
        print("00. Logout")
        print("0. Quit")
        print("-------------------------------------------------------------------------------------")

#STATS MENU ----------------------------------------------------------------------------------
def stats_menu():
    print("Please select an option:")
    print("1. Change username")
    print("2. Reset stats")
    print("3. Delete User")
    print("0. Back")

if __name__ == "__main__":
    main()
