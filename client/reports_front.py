# File Name: reports_front.py
# File Description: Contains the functions that display the reservation and transaction reports 
#
# Date: May 5, 2022


# Importing Libraries
import pandas as pd
pd.options.display.width=None
import requests
import make_and_cancel_reservations_front as make_cancel


# Base URL
URL = 'http://127.0.0.1:8000/v2_0/'


def get_daterange():
    '''
    This function gets a date range from the user.

    Inputs:
        None.

    Returns:
        (string) the start date.
        (string) the end date. 
    '''

    print("\nEntering a start date and end date is optional.")
    print("By default, the start date is set to today and the end date is set to 7 days from the start date.")
    
    # User Inputs
    conf = input("\nDo you want to enter a start date? [y/n]: ")
    while conf not in ['Y', 'y', 'N', 'n']:
        print("Please enter valid input: y or n")
        conf = input("Do you want to enter a start date? [y/n]: ")
    check = make_cancel.confirm(conf) 
    
    if check == "Yes":
        startdate = input("Enter the start date (mm-dd-yyyy): ")
        check = make_cancel.check_date(startdate)
        while not check:
            print("Please enter valid date (format: mm-dd-yyyy)!")
            startdate = input("Enter the start date (mm-dd-yyyy): ")
            check = make_cancel.check_date(startdate)

        print("\nStart date: ")
        print("Date: {}".format(startdate))
    
    else:
        startdate = None

    conf = input("Do you want to enter an end date? [y/n]: ")
    while conf not in ['Y', 'y', 'N', 'n']:
        print("Please enter valid input: y or n")
        conf = input("Do you want to enter an end date? [y/n]: ")
    check = make_cancel.confirm(conf) 
    
    if check == "Yes":
        enddate = input("Enter the end date (mm-dd-yyyy): ")
        check = make_cancel.check_date(enddate)
        while not check:
            print("Please enter valid date (format: mm-dd-yyyy)!")
            enddate = input("Enter the end date (mm-dd-yyyy): ")
            check = make_cancel.check_date(enddate)

        print("\nEnd date: ")
        print("Date: {}".format(enddate))
    
    else:
        enddate = None
    
    return startdate, enddate


def all_reservations_for_user():
    '''
    This function lets the user input the necessary information 
    to display all the reservations within a date range.

    Inputs:
        None.

    Returns:
        None.
    '''

    # User Inputs
    name = input("\nEnter your name (Leave blank and press enter for all users): ")
    if name != "":
        while make_cancel.check_space(name):
            print("\nName cannot have a space!")
            name = input("Enter your name: ")

    startdate, enddate = get_daterange()
    json_object = {
        "start_date": startdate,
        "end_date": enddate,
        "customer_id": name 
    }

    response = requests.get(URL + 'reservations', params = json_object)
    response_info = response.json()
    results_per_page = 10
    
    if response.status_code == 200 and len(response_info["detail"]["reservations"]) > 0:
        print("\nReport of current reservations for "+ name +":-")

        n = len(response_info["detail"]["reservations"])
        more = True
        i = 0

        while (more and n > 0):
            if n < results_per_page:
                reservation_list = []
                for j in range(i, i + n):
                    row = []
                    reservation = response_info["detail"]["reservations"][j]
                    row.append(reservation["reservation_id"])
                    row.append(reservation["customer_id"])
                    row.append(reservation["resource"])
                    row.append(reservation["start_date"])
                    row.append(reservation["end_date"])
                    row.append(reservation["start_time"])
                    row.append(reservation["end_time"])
                    row.append(reservation["total_cost"])
                    row.append(reservation["down_payment"])
                    more = False
                    reservation_list.append(row)
                
                reservation_df = pd.DataFrame(reservation_list, columns = ['Reservation ID','Customer ID','Resource','Start date','End date','Start time','End time','Total Cost ($)','Downpayment ($)'])
                print(reservation_df.to_string(index=False))

            else:
                reservation_list = []
                for j in range(i, i + results_per_page):
                    row = []
                    reservation = response_info["detail"]["reservations"][j]
                    row.append(reservation["reservation_id"])
                    row.append(reservation["customer_id"])
                    row.append(reservation["resource"])
                    row.append(reservation["start_date"])
                    row.append(reservation["end_date"])
                    row.append(reservation["start_time"])
                    row.append(reservation["end_time"])
                    row.append(reservation["total_cost"])
                    row.append(reservation["down_payment"])
                    reservation_list.append(row)

                reservation_df = pd.DataFrame(reservation_list, columns = ['Reservation ID','Customer ID','Resource','Start date','End date','Start time','End time','Total Cost ($)','Downpayment ($)'])
                print(reservation_df.to_string(index=False))
                
                i = i + results_per_page
                n = n - results_per_page
                        
                if (n > 0):
                    conf = input("Do you want to view the next 10 reservations? [y/n]: ")
                    while conf not in ['Y', 'y', 'N', 'n']:
                        print("Please enter valid input: y or n")
                        conf = input("Do you want to view the next 10 reservations? [y/n]: ")
                    check = make_cancel.confirm(conf)

                    if check == "Yes":
                        continue

                    else:
                        more = False
                else:
                    more = False
        
    elif response.status_code == 200 and len(response_info["detail"]["reservations"]) == 0:
        print("Currently, there aren't any reservations in the system.")

    else: 
        print(response_info["detail"])


def financial_transactions():
    '''
    This function lets the user input the necessary information 
    to display all the financial transactions within a date range.

    Inputs:
        None.

    Returns:
        None.
    '''

    startdate, enddate = get_daterange()
    json_object = {
        "start_date": startdate,
        "end_date": enddate
    }

    response = requests.get(URL + 'transactions', params = json_object)
    response_info = response.json()
    results_per_page = 10
    
    if response.status_code == 200 and len(response_info["detail"]["transactions"]) > 0:
        print("\nReport of all the financial transactions:-")
        n = len(response_info["detail"]["transactions"])
        more = True
        i = 0

        while (more and n > 0):
            if n < results_per_page:
                transaction_list = []
                for j in range(i, i + n):
                    transaction = response_info["detail"]["transactions"][j]
                    row = []
                    row.append(transaction["transaction_id"])
                    row.append(transaction["transaction_type"])
                    row.append(transaction["transaction_date"])
                    row.append(transaction["reservation_id"])
                    row.append(transaction["customer_id"])
                    row.append(transaction["resource"])
                    row.append(transaction["total_cost"])
                    row.append(transaction["transaction_amount"])
                    transaction_list.append(row)
                    more = False

                transaction_df = pd.DataFrame(transaction_list, columns = ['Transaction ID','Transaction Type','Transaction date','Reservation ID','Customer ID','Resource','Total Cost ($)','Transaction Amount ($)'])
                print(transaction_df.to_string(index=False))

            else:
                transaction_list = []
                for j in range(i, i + results_per_page):
                    transaction = response_info["detail"]["transactions"][j]
                    row = []
                    row.append(transaction["transaction_id"])
                    row.append(transaction["transaction_type"])
                    row.append(transaction["transaction_date"])
                    row.append(transaction["reservation_id"])
                    row.append(transaction["customer_id"])
                    row.append(transaction["resource"])
                    row.append(transaction["total_cost"])
                    row.append(transaction["transaction_amount"])
                    transaction_list.append(row)

                transaction_df = pd.DataFrame(transaction_list, columns = ['Transaction ID','Transaction Type','Transaction date','Reservation ID','Customer ID','Resource','Total Cost ($)','Transaction Amount ($)'])
                print(transaction_df.to_string(index=False))

                i = i + results_per_page
                n = n - results_per_page
                        
                if (n > 0):
                    conf = input("Do you want to view the next 10 financial transactions? [y/n]: ")
                    while conf not in ['Y', 'y', 'N', 'n']:
                        print("Please enter valid input: y or n")
                        conf = input("Do you want to view the next 10 financial transactions? [y/n]: ")
                    check = make_cancel.confirm(conf)

                    if check == "Yes":
                        continue

                    else:
                        more = False
                else:
                    more = False
                    
    elif response.status_code == 200 and len(response_info["detail"]["transactions"]) == 0:
        print("Currently, there aren't any financial transactions in the system.")
    else: 
        print(response_info["detail"])