# File Name: staff_management_front.py
# File Description: Contains the functions that adds, deletes or updates a staff
#
# Date: May 5, 2022


# Importing Libraries
import pandas as pd
pd.options.display.width=None
import requests
import make_and_cancel_reservations_front as make_cancel


# Base URL
URL = 'http://127.0.0.1:8000/v2_0/'

def add_staff(staff_id):
    '''
    This function adds a staff member.

    Inputs:
        staff_id (string): staff ID inputted by the user at the start of the session.

    Returns:
        None.
    '''

    # User inputs
    new_staff_id = input("\nEnter the ID of the staff to be added: ")
    while make_cancel.check_space(staff_id):
        print("\nStaff ID cannot have a space!")
        new_staff_id = input("Enter the ID of the staff to be added: ")

    print("\nEntering a staff role is optional.")
    print("By default, the staff role is set to REGULAR.")
    
    conf = input("\nDo you want to enter a staff role? [y/n]: ")
    while conf not in ['Y', 'y', 'N', 'n']:
        print("Please enter valid input: y or n")
        conf = input("Do you want to enter a staff role? [y/n]: ")
    check = make_cancel.confirm(conf) 
    
    if check == "Yes":
        staff_role = input("\nEnter the staff role [ADMIN/REGULAR]: ")
        while staff_role not in ["ADMIN", "REGULAR"]:
            print("\nPlease enter valid input: ADMIN or REGULAR")
            staff_role = input("Enter the staff role [ADMIN/REGULAR]: ")

        print("\nStaff role entered: ")
        print("Staff role: {}".format(staff_role))
    
    else:
        staff_role = "REGULAR"

    conf = input("\nDo you want to confirm the task of adding a staff? [y/n]: ")
    while conf not in ['Y', 'y', 'N', 'n']:
        print("\nPlease enter valid input: y or n")
        conf = input("Do you want to confirm the task of adding a staff? [y/n]: ")
    check = make_cancel.confirm(conf) 

    if check == "No":
        return

    else:
        json_object = {
        "new_staff_id": new_staff_id,
        "staff_role": staff_role, 
        "staff_id": staff_id
        }
        
        # Posting the request
        response = requests.post(URL + 'staffs', json = json_object)
        print(get_response_message(response))
        '''
        if response.status_code == 201:
            print("\nStaff has been added")
        elif response.status_code == 403:
            print(f"\n{}")
            print("Current operating staff is not an admin")
        elif response.status_code == 409:
            print("Staff ID to be added is already in use") 
        elif response.status_code == 400:
            print("\nInvalid input")
        '''


def delete_staff(staff_id):
    '''
    This function deletes a staff member.

    Inputs:
        staff_id (string): staff ID inputted by the user at the start of the session.

    Returns:
        None.
    '''

    # User inputs
    staff_to_delete_id = input("\nEnter the ID of the staff to be deleted: ")
    while make_cancel.check_space(staff_to_delete_id):
        print("\nStaff ID cannot have a space!")
        staff_to_delete_id = input("Enter the ID of the staff to be deleted: ")

    conf = input("\nDo you want to confirm the task of deleting a staff? [y/n]: ")
    while conf not in ['Y', 'y', 'N', 'n']:
        print("\nPlease enter valid input: y or n")
        conf = input("Do you want to confirm the task of deleting a staff? [y/n]: ")
    check = make_cancel.confirm(conf) 

    if check == "No":
        return

    else:
        json_object = {
        "staff_to_delete_id": staff_to_delete_id,
        "staff_id": staff_id
        }
        
        # Deleting the request
        response = requests.delete(URL + 'staffs', json = json_object)
        print(get_response_message(response))
        '''
        if response.status_code == 200:
            print("\nStaff has been deleted")
        elif response.status_code == 403:
            print("\nNot authorized to delete a user")
            print("Current operating staff is not an admin")
        elif response.status_code == 404:
            print("\nStaff to be deleted not found")
        '''


def modify_staff(staff_id):
    '''
    This function modifies a staff member.

    Inputs:
        staff_id (string): staff ID inputted by the user at the start of the session.

    Returns:
        None.
    '''

    # User inputs
    staff_to_update_id = input("\nEnter the ID of the staff to be updated: ")
    while make_cancel.check_space(staff_to_update_id):
        print("\nStaff ID cannot have a space!")
        staff_to_update_id = input("Enter the ID of the staff to be updated: ")
    
    staff_role = input("\nEnter the staff role [ADMIN/REGULAR]: ")
    while staff_role not in ["ADMIN", "REGULAR"]:
        print("\nPlease enter valid input: ADMIN or REGULAR")
        staff_role = input("Enter the staff role [ADMIN/REGULAR]: ")

    print("\nStaff role to be updated to: ")
    print("Staff role: {}".format(staff_role))

    conf = input("\nDo you want to confirm the task of updating a staff? [y/n]: ")
    while conf not in ['Y', 'y', 'N', 'n']:
        print("\nPlease enter valid input: y or n")
        conf = input("Do you want to confirm the task of updating a staff? [y/n]: ")
    check = make_cancel.confirm(conf) 

    if check == "No":
        return

    else:
        json_object = {
        "staff_to_update_id": staff_to_update_id,
        "staff_role": staff_role, 
        "staff_id": staff_id
        }
        
        # Putting the request
        response = requests.put(URL + 'staffs', json = json_object)
        print(get_response_message(response))
        '''
        if response.status_code == 200:
            print("\nStaff has been updated")
        elif response.status_code == 403:
            print("\nNot authorized to update a user")
            print("Current operating staff is not an admin")
        elif response.status_code == 404:
            print("Staff to be updated is not found")
        elif response.status_code == 400:
            print("\nInvalid input")
        '''


def staff_management(staff_id):
    '''
    This function displays the menu for Staff Management System.

    Inputs:
        staff_id (string): staff ID inputted by the user at the start of the session.

    Returns:
        None.
    '''

    option = "100"

    while (option != "E" and option != "e"):

        # Staff Management Menu
        print("\nSelect task you want to perform:")
        print("Press A for adding staff")
        print("Press D for deleting staff")
        print("Press U for updating staff")    
        print("Press E for exit")

        # User Input
        option = input("\nEnter your option: ")

        if option == "A" or option == "a":
            add_staff(staff_id)

        elif option == "D" or option == "d":
            delete_staff(staff_id)

        elif option == "U" or option == "u":
            modify_staff(staff_id)

    return

def get_response_message(response):
    return "\n{}".format(response.json()["detail"])