# File Name: user_management.py
# File Description: Contains the functions that adds, deletes or updates a staff
# As well as the functions to interact with the staff json datafile
#
# Date: May 5, 2022

import json, user_management_persist
from user_management_models import *

## --------------------- CONFIG FUNCTIONS --------------------- ##

def parse_data_file():
    """
    Returns the data file path for staffs based on the config.json file

    Returns:
        File path for the json file containing staff data
    """
    config_file = "config.json"
    with open(config_file, "r") as cf:
        config = json.load(cf)
        return config["staff_data_file"]

## --------------------- HANDLER FUNCTIONS --------------------- ##

def handle_user_management_request(request_type, request_model: StaffRequest, datafile=None):
    """
    Main handler function for the user management requests, refer to
    user_management_models.py for details.
    Loads data from a given datafile and then save it after changes are made

    Args:
        request_type (str): The request method (POST, PUT, DELETE)
        request_model (BaseModel): The parsed model of input data

    Returns:
        response (dict): A JSON formatted dictionary API response
    """
    if not datafile:
        datafile = parse_data_file()

    user_data_manager = user_management_persist.UserDataManager(datafile)
    staff_data = user_data_manager.load()
    
    if request_type != "LOGIN" and not check_request_auth(request_model.staff_id, staff_data):
        return generate_response(403, f"{request_model.staff_id} does not have permission to manage staffs")
    
    if request_type == "LOGIN":
        response = handle_login_user(request_model, staff_data)
    elif request_type == "POST":
        response = handle_post_user(request_model, staff_data)
    elif request_type == "PUT":
        response = handle_put_user(request_model, staff_data)
    elif request_type == "DELETE":
        response = handle_delete_user(request_model, staff_data)
    else:
        response = generate_response(400, f"{request_type} is not a valid request type")
    user_data_manager.save(staff_data)
    return response


def handle_login_user(request, staff_data):
    """
    Handler function for users to login

    Args:
        request (PostStaffsRequest): The model that contains all data for 
            a post request
        staff_data (dict): The staff_data preloaded from staff.json

    Returns:
        response (dict): A JSON formatted dictionary API response
    """
    if request.staff_id in staff_data:
        return generate_response(200, "")
    return generate_response(404, "")


def handle_post_user(request: PostStaffsRequest, staff_data):
    """
    Handler function for post requests, responsible for creating users

    Args:
        request (PostStaffsRequest): The model that contains all data for 
            a post request
        staff_data (dict): The staff_data preloaded from staff.json

    Returns:
        response (dict): A JSON formatted dictionary API response
    """
    new_staff = request.new_staff_id
    staff_role = request.staff_role

    if new_staff in staff_data:
        return generate_response(409, f"{new_staff} already exists in the system")

    if staff_role not in ["ADMIN", "REGULAR"]:
        return generate_response(400, f"{staff_role} is not a valid user role")
    
    staff_data[new_staff] = staff_role

    return generate_response(201, f"{new_staff} has been created with role {staff_role}")

def handle_put_user(request: PutStaffsRequest, staff_data):
    """
    Handler function for post requests, responsible for updating user roles

    Args:
        request (PutStaffsRequest): The model that contains all data for 
            a put request
        staff_data (dict): The staff_data preloaded from staff.json

    Returns:
        response (dict): A JSON formatted dictionary API response
    """
    update_staff = request.staff_to_update_id
    new_role = request.staff_role

    if update_staff not in staff_data:
        return generate_response(404, f"{update_staff} is not in the system")

    if staff_data[update_staff] == "ADMIN" and only_one_admin(staff_data):
        return generate_response(403, f"{update_staff} is the only remaining Admin in the system")

    if new_role not in ["ADMIN", "REGULAR"]:
        return generate_response(400, f"{new_role} is not a valid user role")

    staff_data[update_staff] = new_role

    return generate_response(200, f"{update_staff}'s role has been updated to {new_role}")

def handle_delete_user(request: DeleteStaffsRequest, staff_data):
    """
    Handler function for post requests, responsible for deleting users

    Args:
        request (PutStaffsRequest): The model that contains all data for 
            a delete request
        staff_data (dict): The staff_data preloaded from staff.json

    Returns:
        response (dict): A JSON formatted dictionary API response
    """
    delete_staff = request.staff_to_delete_id

    if delete_staff not in staff_data:
        return generate_response(404, f"{delete_staff} is not in the system")

    # If the staff to delete is the only admin left on the system
    if staff_data[delete_staff] == "ADMIN" and only_one_admin(staff_data):
        return generate_response(403, f"{delete_staff} is the only remaining Admin in the system")

    del staff_data[delete_staff]
    return generate_response(200, f"{delete_staff} has been removed from the system")

## --------------------- HELPER FUNCTIONS --------------------- ##

def generate_response(status_code, detail):
    """
    Construct a response that is JSON formatted and can be returned via API
    
    Args:
        status_code (str): status code of the response
        detail (str/dict): ditail of the response, either a string or a dict

    Returns:
        A dict object containing status_code and detail of the response
    """
    return {
        "status_code": status_code,
        "detail": detail
    }


def check_request_auth(requesting_staff: str, staff_data):
    """
    Checks that the staff sending the request to the system has permission to
    modify user data, i.e. they are recorded in the system as an ADMIN

    Args:
        requesting_staff (str): the id of the staff sending the request

    Returns:
        (bool): False if the staff does not have authorization, True if they do
    """
    if requesting_staff not in staff_data:
        return False
    if staff_data[requesting_staff] != "ADMIN":
        return False
    return True

def only_one_admin(staff_data):
    """
    Checks if there is only one admin remaining on the system

    Args:
        staff_data (dict): the dict object containing all staff data

    Returns:
        (bool): True if there is only one admin on the system, False o/w
    """
    total = 0
    for i in staff_data.values():
        if i == "ADMIN":
            total += 1
    if total == 1:
        return True
    return False

def success_response(status_code, detail):
    """
    Construct a response in cases when request handling succeeds
    
    Args:
        status_code (str): status code of the response
        detail (dict): ditail of the response

    Returns:
        A dict object containing status_code and detail of the response
    """
    return {
        "status_code": status_code,
        "detail": detail
    }
