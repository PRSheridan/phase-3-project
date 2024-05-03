# lib/cli.py

from helpers import (
    exit_program,
    login,
    begin_test,
    stats,
    change_name
)

def main():
    logged_in = False
    username = None
    while True:
        if (logged_in == False):
            menu(logged_in)
            choice = input("> ")
            if choice == "0":
                exit_program()
            elif choice == "1":
                username = login()
                logged_in = True
        else:
            menu(logged_in)
            choice = input("> ")
            if choice == "0":
                exit_program()
            elif choice == "00":
                username = None
                logged_in = False
            elif choice == "1":
                begin_test()
            #game will live here:
            #take 3 random sentences
            #countdown
            #capture input
            #capture time
            #compare to sentence
            #evaluate accuracy
            #update test history
            #update user information

            elif choice == "2":
                leaderboard()
            elif choice == "3":
                stats(username)
                user_menu()
                choice = input("> ")
                if(choice == "1"):
                    username = change_name(username)
                elif(choice == "2"):
                    print("test")
                elif(choice == "0"):
                    print("test")
                else:
                    print("Invalid choice")

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
        print("3. Statistics")
        print("00. Logout")
        print("0. Quit")

def user_menu():
    print("Please select an option:")
    print("1. Change username")
    print("2. Reset stats")
    print("0. Back")

if __name__ == "__main__":
    main()
