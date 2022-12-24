# File Name: web.py
#
# Date: May 7, 2022

from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from fastapi_versioning import VersionedFastAPI, version
from pydantic import BaseModel
from datetime import datetime, timedelta
import reserve
from user_management import *

#-------------------- Input Structures -------------------#
class ReservationRequest(BaseModel):
    """
    A class used to parse submitted data for the "create reservation" API

    Attributes:
        customer_id (str): Id of the customer who wants to create a reservation
        resource (str): Resource the customer wants to reserve
        start_date (str): The starting date of the reservation 
        end_date (str): Optional, the ending date of the reservation
        start_time (str): The starting time of the reservation 
        end_time (str): Optional, the ending time of the reservation
        staff_id (str): Id of the operating staff
    """
    customer_id: str
    resource: str
    start_date: str
    end_date: Optional[str] = None
    start_time: str
    end_time: Optional[str] = None
    staff_id: str


class CancellationRequest(BaseModel):
    """
    A class used to parse submitted data for the "cancel reservation" API

    Attributes:
        reservation_id (str): Id of the reservation that the customer wants to cancel
        staff_id (str): Id of the operating staff
    """
    reservation_id: str
    staff_id: str


class GetTransactionRequest(BaseModel):
    """
    A class GET request to the Transactions API endpoint

    All Attributes are Optional, all dates are in mm-dd-yyyy format
    Attributes:
        start_date (str): The starting date of the reservation 
        end_date (str): The ending date of the reservation
    """
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class GetReservationsRequest(BaseModel):
    """
    A class GET request to the Reservations API endpoint

    All Attributes are Optional, all dates are in mm-dd-yyyy format
    Attributes:
        start_date (str): The starting date of the report 
        end_date (str): The ending date of the report
        customer_id (str): A unique string representing the customer
    """
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    customer_id: Optional[str] = None


#-------------------- API -------------------#

app = FastAPI()

VERSION = (2, 0)

@app.post("/reservations", status_code = 201)
@version(VERSION[0], VERSION[1])
def create_reservation(request: ReservationRequest):
    """
    Create a (recurring) reservation. A recurring resrvation will
    be created if start_date is prior to end_date

    - **customer_id**: Id of the customer who wants to create a reservation
    - **resource**: Resource the customer wants to reserve
    - **start_date**: The starting date of the reservation 
    - **end_date**: Optional, the ending date of the reservation 
        (default: same as start_date)
    - **start_time**: The starting time of the reservation 
    - **end_time**: Optional, the ending time of the reservation 
        (default: start_time + 30min)

    Returns:
    
        dict object

    Example returns:

        On success:
        {   'status_code': '200', 
		    'detail':{
        		    'reservation_id': '12',
        		    'discount': '25', // means 25% off
        		    'total_cost': '13.2', 
        		    'down_payment': '6.6'
    		}
	    }

        On error:
        {
            'detail': 'error message'
        }
    """
    return handle_request(reserve_args(request), 201)


@app.delete("/reservations", status_code = 200)
@version(VERSION[0], VERSION[1])
def cancel_resrevation(request: CancellationRequest):
    """
    Cancel a reservation

    - **reservation_id**: Id of the reservation that the customer wants to cancel

    Returns:
    
        dict object

    Example returns:

        On success:
        {
		    'status_code': '200', 
		    'detail': {
        		    'percent_returned': '75', // means 75% are returned
        		    'refund': '5.5',
    		}
	    }

        On error:
        {
            'detail': 'error message'
        }
    """
    return handle_request(cancel_args(request))


@app.get("/transactions", status_code = 200)
@version(VERSION[0], VERSION[1])
def get_transactions(request: GetTransactionRequest = Depends()):
    """
    Get a report of all transactions recorded by the system between the
    start date and end date<br>
    Note: The start date must be given for the end date argument to be valid

    - **start_date**: optional, the start date of the report to generate (default: today)
    - **end_date**: optional, the end date of the report to generate (default: 7 days from start_date)

    Returns:

        dict object

    Example returns:

        On success:
        {
	    	"status_code": 200,
	    	"detail": {
	    		"reservations" : [list of reservation_data]
	    	}
	    }
	    reservation_data: {
	    	"reservation_id": "12",
	    	"customer_id": "1",
	    	"resource": "workshop"
	    	"start_date": "04-12-2022",
	    	"end_date": "04-12-2022",
	    	"start_time": "9:00",
	    	"end_time": "10:00",
	    	"total_cost": "99",
	    	"down_payment": "0"
	    }

        On error:
        {   
            "status_code": 400,
            'detail': 'error message'
        }
    """
    return handle_request(transaction_args(request))


@app.get("/reservations", status_code = 200)
@version(VERSION[0], VERSION[1])
def get_reservation(request: GetReservationsRequest = Depends()):
    """
    Get a report of all reservations currently in the system between the
    start date and end date, can specify a unique user to generate report for<br>
    Note: The start date must be given for the end date argument to be valid

    - **start_date**: optional, the start date of the report to generate (default: today)
    - **end_date**: optional, the end date of the report to generate (default: 7 days from start_date)
    - **customer_id**: optional, the customer to generate report on (default: '' to generate report on all customers)

    Returns:
    
        dict object

    Example returns:
    
        On success:
        {
	    	"status_code": "200",
	    	"detail": {
	    		"transactions": [list of transaction_data]
	    	}
	    }
	    transaction_data: {
	    	"transaction_id": "1",
	    	"transaction_type": "CANCELLATION",
	    	"transaction_date": "04-12-2022",
	    	"reservation_id": "12",
	    	"customer_id": "1",
	    	"resource": "workshop",
	    	"total_cost": 99,
	    	"transaction_amount": "0"
	    }

        On error:
        {
            'detail': 'error message'
        }
    """
    return handle_request(reservations_args(request))


@app.get("/login", status_code = 200)
@version(VERSION[0], VERSION[1])
def staff_login(request: StaffRequest):
    """
    Allow users to check if they are eligible for login (allowed if the user
    exists in the staff database without forms of authentication)

    - **staff_id**: The ID of the staff trying to login

    Returns:
    
        dict object

    Example returns:
    
        {
	    	"status_code": "200",
	    	"detail": ""
	    }
    """
    return handle_user_management_web("LOGIN", request, 200, "LOGIN")


@app.post("/staffs", status_code = 201)
@version(VERSION[0], VERSION[1])
def post_staffs(request: PostStaffsRequest):
    """
    Create a new staff user, with default permission role of REGULAR staff.
    
    - **new_staff_id**: The ID/username of the staff to create
    - **staff_role**: OPTIONAL, Permission role of the new user, Regular Staff by default
    - **staff_id**: The ID of the staff making the request

    Returns:
    
        dict object

    Example returns:
    
        {
	    	"status_code": "201",
	    	"detail": "New Staff with ID <staff_id> has been created"
	    }
    """
    return handle_user_management_web("POST", request, 201, "CREATE STAFF")

@app.put("/staffs", status_code = 200)
@version(VERSION[0], VERSION[1])
def put_staffs(request: PutStaffsRequest):
    """
    Create a new staff user, with default permission role of REGULAR staff.
    
    - **staff_to_update_id**: The ID/username of the staff to update
    - **staff_role**: Permission role of the new user, Regular Staff by default
    - **staff_id**: The ID of the staff making the request

    Returns:
    
        dict object

    Example returns:
    
        {
	    	"status_code": "200",
	    	"detail": "Role of Staff with ID <staff_id> has been updated to <new_role>"
	    }

    """
    return handle_user_management_web("PUT", request, 200, "UPDATE_STAFF")

@app.delete("/staffs", status_code = 200)
@version(VERSION[0], VERSION[1])
def delete_staffs(request: DeleteStaffsRequest):
    """
    Create a new staff user, with default permission role of REGULAR staff.
    
    - **staff_to_delete_id**: The ID/username of the staff to delete
    - **staff_id**: The ID of the staff making the request

    Returns:
    
        dict object

    Example returns:
    
        {
	    	"status_code": "200",
	    	"detail": "Staff with ID <staff_id> has been deleted"
	    }

    """
    return handle_user_management_web("DELETE", request, 200, "DELETE_STAFF")


app = VersionedFastAPI(app)

## --------------------- HANDLER FUNCTIONS --------------------- ##

def handle_request(request, success_code=200):
    """
    Handle a request by invoking the reservation system
    
    Args:
        request (List[str]): the request to be handled
        success_code (int): the status code in cases when the handling succeeds
    
    Raises:
        HTTPException Error: if the request violates any constraints specified
        in A-01

    Returns:
        A dict object containing status code and detail information
    """
    success, result = reserve.handle_request(request)
    if not success:
        handle_error(result["status_code"], result["operation_name"], result["detail"])
    return success_response(success_code, result)


def handle_user_management_web(command, request, success_code, operation):
    """
    Handle a request by invoking the reservation system
    
    Args:
        command (List[str]): The type of request/command to be handled
        request (StaffRequest): The model that contains all request data
        success_code (int): the status code to return when handling succeeds
        operation (str): The type of operation being performed, used in output
    
    Raises:
        HTTPException Error: if the request violates any constraints

    Returns:
        A dict object containing status code and detail information
    """
    result = handle_user_management_request(command, request)
    if result["status_code"] != success_code:
        handle_error(result["status_code"], operation, result["detail"])
    return result

## --------------------- HELPER FUNCTIONS --------------------- ##

def invalid_time_format(time):
    """
    Check if time is of HH:MM format
    
    Args:
        time (str): time to be validated

    Returns:
        True if time is not of HH:MM format;
        False otherwise
    """
    time = time.split(':')
    if len(time) != 2:
        return True
    if not time[0].isdigit() or not time[1].isdigit():
        return True
    return False


def time_after_30min(time):
    """
    Return time after 30 minutes since a given time
    
    Args:
        time (str): start time in HH:MM format

    Returns:
        time + 30 minutes in HH:MM format
    """
    if invalid_time_format(time):
        return time
    hour, minute = map(int, time.split(':'))
    d = datetime(2022, 4, 26, hour, minute)
    d += timedelta(minutes=30)
    return d.strftime("%H:%M")

def date_after_7days(date):
    """
    Return date after 7 days since a given date
    
    Args:
        date (str): start date in mm-dd-yyyy format

    Returns:
        date + 7 days in mm-dd-yyyy format
    """
    dt_date = datetime.strptime(date, "%m-%d-%Y")
    dt_date += timedelta(days=7)
    return dt_date.strftime("%m-%d-%Y")


def get_today_date():
    """Returns the date of today in mm-dd-yyyy format"""
    today = datetime.today()
    return f"{today.month}-{today.day}-{today.year}"


def check_time_format(time):
    """
    Check whether format of time is valid
    
    Args:
        time (str): time to verify
    
    raise:
        HTTPException Error: Invalid time format
    """
    if time is None:
        return
    if invalid_time_format(time):
        handle_error(400, "Reservation", f"Invalid time format: {time}")


def check_date_format(date):
    """
    Check whether format of date is valid
    
    Args:
        date (str): date to verify
    
    raise:
        HTTPException Error: Invalid date format
    """
    if not date_format_is_correct(date):
        handle_error(400, "Reservation", f"Invalid date format: {date}")


def reserve_args(request: ReservationRequest):
    """
    Return a list of arguments to be sent to the reservation system
    to create a reservation
    
    Args:
        request (ReservationRequest): submitted data of the request
    
    raise:
        HTTPException Error: Invalid time format
        HTTPException Error: Invalid date format
        HTTPException Error: Empty customer_id

    Returns:
        List of command and arguments to sent to reservation system
        to create a reservation
    """
    if request.customer_id == "":
        handle_error(400, "Reservation", "Empty customer_id")
    check_time_format(request.start_time)
    check_time_format(request.end_time)
    check_date_format(request.start_date)
    check_date_format(request.end_date)
    end_date = request.end_date if request.end_date else request.start_date
    end_time = request.end_time if request.end_time else time_after_30min(request.start_time)
    reservation_date = get_today_date()
    return ["reserve", request.customer_id, request.resource, request.start_date, 
            end_date, request.start_time, end_time, reservation_date, request.staff_id]


def cancel_args(request: CancellationRequest):
    """
    Return a list of arguments to be sent to the reservation system
    to cancel a reservation
    
    Args:
        request (CancellationRequest): submitted data of the request

    Returns:
        List of command and arguments to sent to reservation system
        to cancel a reservation
    """
    cancellation_date = get_today_date()
    return ['cancel', request.reservation_id, cancellation_date, request.staff_id]

def date_format_is_correct(date):
    """
    Check that a given date is in mm-dd-yyyy format, or is None

    Args:
        date (str): A string representing a date

    Returns:
        (bool) True if format is correct (or if is empty), False otherwise
    """
    if date == None:
        return True
    try:
        datetime.strptime(date, "%m-%d-%Y")
        return True
    except:
        return False
        

def transaction_args(request: GetTransactionRequest):
    """
    Check the format of arguments in the transaction request, if formatting is
    correct, return a list of arguments to be sent to the reservation system
    
    Args:
        request (GetTransactionRequest): inputs received from API endpoint

    Raises:
        HTTPException Error: Dates in wrong format

    Returns:
        List of command and arguments to sent to reservation system to generate
        a transactions report
    """
    if  not date_format_is_correct(request.start_date) or \
        not date_format_is_correct(request.end_date):
            handle_error(400, "Get Transactions", "date format incorrect")
            
    if request.start_date == None:
        request.start_date = get_today_date()
        request.end_date = date_after_7days(request.start_date)
    elif request.end_date == None:
        request.end_date = date_after_7days(request.start_date)
    return ["financial", request.start_date, request.end_date]


def reservations_args(request: GetReservationsRequest):
    """
    Check the format of arguments in the get reservations request, if formatting
    is correct, return a list of arguments to be sent to the reservation system
    
    Args:
        request (GetReservationsRequest): inputs received from API endpoint

    Raises:
        HTTPException Error: Dates in wrong format

    Returns:
        List of command and arguments to sent to reservation system to generate
        a reservations report
    """
    if  not date_format_is_correct(request.start_date) or \
        not date_format_is_correct(request.end_date):
            handle_error(400, "Get Reservations", "date format incorrect")

    if request.start_date == None:
        request.start_date = get_today_date()
        request.end_date = date_after_7days(request.start_date)
    elif request.end_date == None:
        request.end_date = date_after_7days(request.start_date)
    
    if request.customer_id == None:
        return ["reservations", request.start_date, request.end_date]
    else:
        return ["reservations", request.start_date, request.end_date, request.customer_id]

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

def handle_error(code, operation_name, detail):
    """
    Raise a HTTPException

    Args:
        code (int): status code
        operation_name (str): name of the operation that triggered this error
        detail (str): error message indicating reason of the error

    Raises:
        HTTPException
    """
    raise HTTPException(status_code=code, detail=f"{operation_name} failed: {detail}")
