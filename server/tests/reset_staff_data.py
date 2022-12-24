# File Name: reset_staff_data.py
# File Description: Contains the tests for user_management functionality
#
# Date: May 5, 2022

import json

default = {
    "hanzeh": "ADMIN",
    "yusen": "REGULAR",
    "prajvalmohan": "REGULAR",
    "thanushrir": "REGULAR",
    "haydersaad": "REGULAR",
    "peter": "REGULAR",
    "kariyushi": "REGULAR",
    "spencer": "REGULAR",
    "staff1": "REGULAR",
    "staff2": "REGULAR"
}

def reset_staff_data():
    confirmation = input("Are you sure you want to reset the active staff data file? [y/n]: ").lower()
    if confirmation in ["y", "yes"]:
        with open("data/staff.json", "w") as FILE:
            json.dump(default, FILE, indent=4)
    else:
        print("The staff data file was not reset")