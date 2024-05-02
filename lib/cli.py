# lib/cli.py

from helpers import (
    exit_program,
    login,
    begin_test,
    user_info
)

def main():
    logged_in = False
    while True:
        if (logged_in == False):
            menu(logged_in)
            choice = input("> ")
            if choice == "0":
                exit_program()
            elif choice == "1":
                login()
                logged_in = True
        else:
            menu(logged_in)
            choice = input("> ")
            if choice == "0":
                exit_program()
            elif choice == "00":
                logged_in = False
            elif choice == "1":
                begin_test()
            elif choice == "2":
                leaderboard()
            elif choice == "3":
                user_info()
            else:
                print("Invalid choice")

def menu(logged_in):
    print("Please select an option:")
    if (logged_in == False):
        print("1. Login")
        print("0. Quit")
    else:
        print("1. Begin test")
        print("2. Scoreboard")
        print("3. User information")
        print("00. Logout")
        print("0. Quit")

if __name__ == "__main__":
    main()
