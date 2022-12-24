# File Name: make_and_cancel_reservations_front.py
# File Description: Contains the functions that make and cancel reservations 
#
# Date: May 5, 2022


# Importing Libraries
import datetime
import pandas as pd
pd.options.display.width=None
import requests
import main_front


# Base URL
URL = 'http://127.0.0.1:8000/v2_0/'


def resource_name(book):
    '''
    This function converts the user's choice of resource into the resource 
    name as stored in the database.

    Inputs:
        book (string): user's choice of resource.

    Returns:
        (string) the name of the resource.
    '''

    if book == "W" or book == "w":
        return 'workshop'

    if book == "M" or book == "m":
        return 'microvac'

    if book == "I" or book == "i":
        return 'irradiator'

    if book == "P" or book == "p":
        return 'extruder'

    if book == "C" or book == "c":
        return 'hvc'

    if book == "H" or book == "h":
        return 'harvester'


def confirm(conf):
    '''
    This function checks if the user wants to go ahead with the prompt

    Inputs:
        conf (string): user response to prompt.

    Returns: 
        (string) "Yes" or "No" based on user input.
    '''

    if conf == 'Y' or conf == 'y':
        return "Yes"
    elif conf =='N' or conf == 'n':
        return "No"


def check_space(value):
    '''
    This function checks if the string passed into it has spaces.

    Inputs:
        value (string): string to be checked.

    Returns: 
        (bool) True or False.
    '''

    split_length = len(value.split())
    if split_length > 1:
        return True
    else:
        return False


def print_details(json_object):
    '''
    This function prints the reservation details of a user on the console.

    Inputs:
        json_object (JSON): json object of user inputs in the reservation function.

    Returns:
        None.
    '''
    
    # Posting the request
    response = requests.post(URL + "reservations", json = json_object)
    response_info = response.json()

    if response.status_code == 201:
        print("\nYour reservation has been booked")
        print("Reservation details:-")
        print("Reservation ID  : {}".format(response_info["detail"]["reservation_id"]))
        print("Discount Percent: {}".format(response_info["detail"]["discount"]))
        print("Total Cost  ($) : {}".format(response_info["detail"]["total_cost"]))
        print("Downpayment ($) : {}".format(response_info["detail"]["down_payment"]))
    else: 
        print(response_info["detail"])


def check_date(user_entered_date):
    '''
    This function checks if the date entered is in a valid format.

    Inputs:
        user_entered_date (string): date to be checked.

    Returns: 
        (bool) True or False.
    '''

    try:
        entered_date = list(map(int, user_entered_date.split("-")))
        obj = datetime.date(int(entered_date[2]), int(entered_date[0]), int(entered_date[1]))
    except ValueError:
        return False
    except IndexError:
        return False
    return True
    

def check_time(user_entered_time):
    '''
    This function checks if the time entered is in a valid format.

    Inputs:
        user_entered_time (string): time to be checked.

    Returns: 
        (bool) True or False.
    '''
    
    try:
        entered_time = list(map(int, user_entered_time.split(":")))
        obj = datetime.time(int(entered_time[0]), int(entered_time[1]))
    except ValueError:
        return False
    except IndexError:
        return False
    return True


def reservation(staff_id):
    '''
    This function displays the reservation menu for all resources, and lets 
    the user input the necessary information in order to make the reservation.

    Inputs:
        staff_id (string): staff ID inputted by the user at the start of the session.

    Returns:
        None.
    '''

    # Reservation Menu
    print("\nEquipment in facility:")
    print("Press W for workshop")
    print("Press M for mini microvacs")
    print("Press I for irradiators")
    print("Press P for polymer extruders")
    print("Press C for high velocity crusher")
    print("Press H for 1.21 gigawatt lightning harvester")
    print("Press E for exit")

    # User Inputs
    book = input("\nPick item for reserving: ") 
    while book not in ['W', 'M', 'I', 'P', 'C', 'H', 'E', 'w', 'm', 'i', 'p', 'c', 'h', 'e']:
        print("\nPlease enter valid input")
        book = input("\nPick item for reserving: ")

    if book == "E" or book == "e":
        main_front.menu(staff_id) 

    name = input("\nEnter your name: ")  
    while check_space(name):
        print("\nName cannot have a space!")
        name = input("Enter your name: ")

    resource = resource_name(book) 

    startdate = input("Enter reservation start date (mm-dd-yyyy): ")
    check = check_date(startdate)
    while not check:
        print("Please enter valid date (format: mm-dd-yyyy)!")
        startdate = input("Enter reservation start date (mm-dd-yyyy): ")
        check = check_date(startdate)

    starttime = input("Enter reservation start time (24 hr format - hh:mm): ")
    check = check_time(starttime)
    while not check:
        print("Please enter valid time (format: hh:mm)!")
        starttime = input("Enter reservation start time (24 hr format - hh:mm): ")
        check = check_time(starttime)

    print("\nStart date and time entered: ")
    print("Date: {} || Time: {}".format(startdate, starttime))

    print("\nEntering an end time is optional.")
    print("By default, we will book a 30 minute slot for you.")
    conf = input("Do you still want to enter the end time? [y/n]: ")
    while conf not in ['Y', 'y', 'N', 'n']:
        print("Please enter valid input: y or n")
        conf = input("Do you still want to enter the end time? [y/n]: ")
    check = confirm(conf) 
    
    if check == "Yes":
        endtime = input("\nEnter reservation end time (24 hr format - hh:mm) for the same day: ")
        check = check_time(endtime)
        while not check:
            print("Please enter valid time (format: hh:mm)!")
            endtime = input("\nEnter reservation end time (24 hr format - hh:mm) for the same day: ")
            check = check_time(endtime)

        print("\nEnd time entered: ")
        print("Time: {}".format(endtime))
          
    else:
        endtime = None
        
    json_object = {
        "customer_id": name, 
        "resource": resource, 
        "start_date": startdate,
        "start_time": starttime, 
        "end_time": endtime,
        "staff_id": staff_id
    }

    print_details(json_object)


def recurring_reservations(staff_id):
    '''
    This function displays the reservation menu for all resources, and lets the
    user input the necessary information in order to make a recurring reservation.

    Inputs:
        staff_id (string): staff ID inputted by the user at the start of the session.

    Returns:
        None.
    '''

    # Reservation Menu
    print("\nEquipment in facility:")
    print("Press W for workshop")
    print("Press M for mini microvacs")
    print("Press I for irradiators")
    print("Press P for polymer extruders")
    print("Press C for high velocity crusher")
    print("Press H for 1.21 gigawatt lightning harvester")
    print("Press E for exit")

    # User Inputs
    book = input("\nPick item for reserving: ")
    while book not in ['W', 'M', 'I', 'P', 'C', 'H', 'E', 'w', 'm', 'i', 'p', 'c', 'h', 'e']:
        print("\nPlease enter valid input")
        book = input("\nPick item for reserving: ")

    if book == "E" or book == "e":
        main_front.menu(staff_id)

    name = input("\nEnter your name: ") 
    while check_space(name):
        print("\nName cannot have a space!")
        name = input("Enter your name: ")

    resource = resource_name(book) 

    startdate = input("Enter recurring reservation start date (mm-dd-yyyy): ")
    check = check_date(startdate)
    while not check:
        print("Please enter valid date (format: mm-dd-yyyy)!")
        startdate = input("Enter recurring reservation start date (mm-dd-yyyy): ")
        check = check_date(startdate)

    starttime = input("Enter recurring reservation start time (24 hr format - hh:mm): ")
    check = check_time(starttime)
    while not check:
        print("Please enter valid time (format: hh:mm)!")
        starttime = input("Enter recurring reservation start time (24 hr format - hh:mm): ")
        check = check_time(starttime)

    print("\nStart date and time entered: ")
    print("Date: {} || Time: {}".format(startdate, starttime))

    enddate = input("Enter recurring reservation end date (mm-dd-yyyy): ")
    check = check_date(enddate)
    while not check:
        print("Please enter valid date (format: mm-dd-yyyy)!")
        enddate = input("Enter recurring reservation end date (mm-dd-yyyy): ")
        check = check_date(enddate)

    endtime = input("Enter recurring reservation end time (24 hr format - hh:mm): ")
    check = check_time(endtime)
    while not check:
        print("Please enter valid time (format: hh:mm)!")
        endtime = input("\nEnter recurring reservation end time (24 hr format - hh:mm): ")
        check = check_time(endtime)

    print("\nEnd date and time entered: ")
    print("Date: {} || Time: {}".format(enddate, endtime))

    json_object = {
        "customer_id": name,
        "resource": resource, 
        "start_date": startdate,
        "end_date": enddate,
        "start_time": starttime, 
        "end_time": endtime,
        "staff_id": staff_id
    }

    print_details(json_object)


def cancellation(staff_id):
    '''
    This function cancels a reservation based on the user's reservation ID.

    Inputs:
        staff_id (string): staff ID inputted by the user at the start of the session.

    Returns:
        None.
    '''

    # User Inputs
    res_id = input("\nEnter the Reservation ID you want to cancel: ") ### check error handle letter
    while check_space(res_id):
        print("\nReservation ID cannot have a space!")
        res_id = input("Enter the Reservation ID you want to cancel: ")
    
    conf = input("Do you want to confirm the cancellation? [y/n]: ")
    while conf not in ['Y', 'y', 'N', 'n']:
        print("Please enter valid input: y or n")
        conf = input("Do you want to confirm the cancellation? [y/n]: ")
    check = confirm(conf) 

    if check == "No":
        main_front.menu(staff_id)

    else:
        json_object = {
            "reservation_id": res_id,
            "staff_id": staff_id
        }
        
        # Deleting the request
        response = requests.delete(URL + 'reservations', json = json_object)
        response_info = response.json()

        if response.status_code == 200:
            print("\nYour reservation has been canceled")
            print("Cancellation details:-")
            print("Refund Percent  : {}".format(response_info["detail"]["percent_returned"]))
            print("Refund Amount($): {}".format(response_info["detail"]["refund"]))
        else: 
            print(response_info["detail"])