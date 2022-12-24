# File Name: main_front.py
# File Description: Contains the main function to run the frontend.
# It also has the menu that will be printed on the console. 
#
# Date: May 5, 2022


# Importing Libraries
import pandas as pd
pd.options.display.width=None
import requests
import sys
import make_and_cancel_reservations_front as make_cancel
import staff_management_front as staff
import reports_front as report


# Base URL
URL = 'http://127.0.0.1:8000/v2_0/'


def menu(staff_id):
    '''
    This function displays the Main Menu for MPCS Inc. Reservation System.

    Inputs:
        staff_id (string): staff ID inputted by the user at the start of the session.

    Returns:
        None.
    '''
    
    choice = "100"

    while (choice != "7"):
        
        print("\nSelect task you want to perform:")
        print("Enter 1 to make a reservation")
        print("Enter 2 to make a recurring reservation")
        print("Enter 3 to cancel a reservation")
        print("Enter 4 to generate report of the current reservations over a particular time period")
        print("Enter 5 to get financial transactions over a particular time period")
        print("Enter 6 to manage staff")
        print("Enter 7 to logout")

        choice = input("\nEnter your option: ")

        if choice == "1":
            make_cancel.reservation(staff_id)

        elif choice == "2":
            make_cancel.recurring_reservations(staff_id)

        elif choice == "3":
            make_cancel.cancellation(staff_id)

        elif choice == "4":
            report.all_reservations_for_user()

        elif choice == "5":
            report.financial_transactions()

        elif choice == "6":
            staff.staff_management(staff_id)

    return


def main():
    '''
    This invokes the program execution

    Inputs:
        None.

    Returns:
        None.
    '''

    run_again = True

    while(run_again):
        staff_id = input("\nEnter your staff id: ")

        while make_cancel.check_space(staff_id):
            print("\nStaff ID cannot have a space!")
            staff_id = input("Enter your staff id: ")

        json_object = {
            "staff_id": staff_id
        }
    
        response = requests.get(URL + 'login', json = json_object)

        if response.status_code == 200:   
            menu(staff_id)

            conf = input("Do you want to login again? [y/n]: ")
            choice = make_cancel.confirm(conf)
            if choice == "Yes":
                run_again = True
            else:
                run_again = False
        
        else:
            print("Please enter a valid staff id!")

    sys.exit("\nThank you for using the MPCS Inc. Reservation System")


if __name__ == "__main__":
    # Calling the main execution
    print("##########################################################################################")
    print("\nWelcome to the MPCS Inc. Reservation System")
    print("Note: Please run the terminal on full screen\n")
    main()