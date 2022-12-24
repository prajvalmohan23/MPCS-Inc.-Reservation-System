# File Name: reserve.py
# File Description: business logic of the reserve system
#
# Date: May 7, 2022

from datetime import datetime, timedelta
import persist, json, time

def workshop_is_closed(start_time, end_time, date):
    """
    Given the date, start and end time of a reservation, determine if the
    workshop is going to be open for the duration of the reservation

    Returns: 
        (bool) True if workshop is open, False otherwise
    """
    if date.weekday() == 6:
        return True
    if date.weekday() == 5 and (start_time < 100 or end_time > 160):
        return True
    return start_time < 90 or end_time > 180
        
def split_time(start, end):
    """
    Split the start and end time into an integer representation
    E.g. 150 represents 15:00, 105 represents 10:30

    Args:
        Arguments are of format HH:MM
        start (str): The start time
        end (str): The end time
    
    Returns:
        Integer representation of the start time and end time
    """
    start_hour, start_minute = map(int, start.split(':'))
    end_hour, end_minute = map(int, end.split(':'))
    start_time = start_hour * 10 + start_minute // 30 * 5
    end_time = end_hour * 10 + end_minute // 30 * 5
    return start_time, end_time

def is_available(reservation_type, count):
    """
    Given the type of reservation and the number of bookings already made for
    that type of workshop/equipment, determine if it is still available for booking

    Args:
        reservation_type (str): The type of resource to reserve
        count (int): The number of reservations already made for that resource

    Returns:
        (bool) True if the workshop/equipment is still available, False otherwise
    """
    if reservation_type == 'workshop':
        return count <= 15
    elif reservation_type == 'microvac':
        return count <= 2
    elif reservation_type == 'irradiator':
        return count <= 2
    elif reservation_type == 'extruder':
        return count <= 3
    elif reservation_type == 'hvc':
        return count <= 1
    elif reservation_type == 'harvester':
        return count <= 1
    print(f"Unsupported resource: {reservation_type}.")
    return False

def between(date, start, end):
    """
    Given three date strings, determine if the first date is between the
    start (second) and the end (third) date

    Args:
        All arguments are strings of the format MM-DD-YYYY
        date (str): The date to check for
        start (str): The start date
        end (str): The end date

    Returns:
        True if it is between the start and end date, False otherwise
    """
    start_date = datetime.strptime(start, "%m-%d-%Y")
    end_date = datetime.strptime(end, "%m-%d-%Y")
    ddate = datetime.strptime(date, "%m-%d-%Y")
    return (ddate - start_date).days >= 0 and (end_date - ddate).days >=0

def reservation_is_not_in_date_range(reservation_datetime, start_datetime, end_datetime):
    """
    Given all dates of a reservation to be made, check if it is within the
    allowed date range (0 to 30 days in advance)

    Args:
        Contraint: All inputs are datetime objects
        reservation_datetime (datetime): The date on which the reservation is made
        start_datetime (datetime): The first day of the reservation
        end_datetime (datetime): The last day day of the reservation

    Returns:
        (False, None) if it is between the allowed date range, (True, error response) otherwise
    """
    # Check if reservation is in the future
    if (reservation_datetime - start_datetime).days > 0:
        print('Reservation Failed: cannot reserve time already passed.')
        return True, error_response(400, "Reservation", 'Cannot reserve time already passed.')
    
    # Check if reservation is within 30 days
    if (end_datetime - reservation_datetime).days > 30:
        # "Clients expect to be able to make reservations up to 30 days in advance"
        print('Reservation Failed: cannot reserve time more than 30 days away.')
        return True, error_response(400, "Reservation", 'Cannot reserve time more than 30 days away.')
    
    return False, None

def reservation_type_is_not_known(reservation_type):
    """
    Check if the reservation type is valid

    Args:
        reservation_type (str):The workshop/resouce type to reserve

    Returns:
        (True, error response) if it is owned by the workshop, (False, None) otherwise
    """
    if reservation_type not in ['workshop', 'microvac', 'irradiator', 'extruder', 'hvc', 'harvester']:
        print(f"Unsupported resource: {reservation_type}.")
        return True, error_response(400, "Reservation", f"Unsupported resource: {reservation_type}")
    return False, None

def reservation_is_not_on_half_hour(minute):
    """
    Check if a reservation is made on the half hour

    Args:
        reservation_type (int): The minute mark of a reservation

    Returns:
        (True, error response) if it is on the half hour, (False, None) otherwise
    """
    if minute != 0 and minute != 30:
        print('Reservation Failed: reservations for all resources are made in 30 minute blocks and always start on the hour or half hour.')
        return True, error_response(400, "Reservation", f"Reservations for all resources are made in 30 minute blocks and always start on the hour or half hour")
    return False, None

def check_only_one_special_machine(all_reservations, days_to_reserve, reservation):
    """
    Check that there is only one special machine reserved by a single client
    at any given time

    Args:
        all_reservations (ResevationManager): the reservation manager of the system
        days_to_reserve (int): All the days this reservation is trying to make
        reservation (Reservation): Reservation Object for this reservation

    Returns:
        (True, None) if only no special machine has been reserved, (False, error response) otherwise
    """
    customer_id = reservation.customer_id
    reservation_type = reservation.reservation_type
    start_time, end_time = split_time(reservation.start_time, reservation.end_time)

    for day in days_to_reserve:
        for reservation in all_reservations:
            if reservation.customer_id != customer_id:
                continue
            if reservation_type == 'workshop':
                continue
            if not between(f'{day.month}-{day.day}-{day.year}', reservation.start_date, reservation.end_date):
                continue
            reservation_start, reservation_end = split_time(reservation.start_time, reservation.end_time)
            if not (reservation_end <= start_time or end_time <= reservation_start):
                # "They can only reserve one special machine at a time"
                print('Reservation Failed: a client can only reserve one special machine at a time')
                return False, error_response(400, "Reservation", "A client can only reserve one special machine at a time")
    return True, None

def over_three_reservations(all_reservations, days_to_reserve, customer_id):
    """
    Check if a customer is going to go over the limit of three reservations for
    a single week, given that they are trying to make reservations given by
    days_to_reserve

    Args:
        all_reservations (ResevationManager): the reservation manager of the system
        days_to_reserve (int): All the days this reservation is trying to make
        customer_id (str): The customer that is trying to make the reservation

    Returns:
        (False, None) if the customer is not going to go over the three days
        restriction, (True, error response) if they are going to go over the restriction
    """
    weekr = {}
    # Count up the number of reservations that this customer has already made
    for reservation in all_reservations:
        if reservation.customer_id != customer_id:
            continue
        reservation_start_datetime = datetime.strptime(reservation.start_date, "%m-%d-%Y")
        reservation_end_datetime = datetime.strptime(reservation.end_date, "%m-%d-%Y")
        rdays = []
        rcur = reservation_start_datetime
        while (reservation_end_datetime - rcur).days >= 0:
            rdays.append(rcur)
            rcur += timedelta(days=1)
        for day in rdays:
            key = f'{day.year}-{day.isocalendar()[1]}'
            if key not in weekr:
                weekr[key] = 1
            else:
                weekr[key] += 1
    # Add the days that are going to be reserved now
    for day in days_to_reserve:
        key = f'{day.year}-{day.isocalendar()[1]}'
        if key not in weekr:
            weekr[key] = 1
        else:
            weekr[key] += 1
    # Check if it is going to go over three
    for k in weekr:
        if weekr[k] > 3:
            print(f'Reservation Failed: A client can only make reservations for 3 different days in a given week.')
            return True, error_response(400, "Reservation", "A client can only make reservations for 3 different days in a given week")
            
    return False, None

def check_non_cooldown_requirements(all_reservations, day, reservation_type, start_time, end_time):
    """
    Given the day of reservation, type of reservation and the start and end time, check all
    the non-cooldown related rules that must be applied to the reservation, if the rules
    correctly applies without error, return True, return False if there exists some error
    and the reservation cannot be made

    Args:
        all_reservations (ReservationManager): The reservation manager of the system
        day (datetime): the datetime object of the day that is being checked
        reservation_type (str): the machine/workshop to make reservation for
        start_time (str): the start time of this reservation
        end_time (str): the finish time of this reservation

    Returns:
        (False, error response) if the reservation violates some requirement, (True, None) otherwise
    """
    for t in range(start_time, end_time, 5):
        count = 0
        s_cnt = 0
        h_run = False
        for reservation in all_reservations:
            reservation_start, reservation_end = split_time(reservation.start_time, reservation.end_time)
            if not (t >= reservation_start and t < reservation_end):
                continue
            if not between(f'{day.month}-{day.day}-{day.year}', reservation.start_date, reservation.end_date):
                continue
            if reservation.reservation_type == 'harvester':
                h_run = True
            if reservation.reservation_type != 'workshop':
                # increament special_count by 1
                s_cnt += 1
            if reservation.reservation_type == reservation_type:
                # increament count by 1
                count += 1
        if not is_available(reservation_type, count+1):
            print(f'Reservation Failed: not enough available {reservation_type}, {count} already reserved.')
            return False, error_response(400, "Reservation", f'Not enough available {reservation_type}, {count} already reserved')
            
        if reservation_type == 'irradiator' and count == 1:
            print('Reservation Failed: only 1 irradiator can be used at a time.')
            return False, error_response(400, "Reservation", 'Only 1 irradiator can be used at a time')
            
        if reservation_type != 'workshop':
            s_cnt += 1
        if h_run and s_cnt > 4:
            print('Reservation Failed: only 3 other machines can run while the 1.21 gigawatt lightning harvester is operating.')
            return False, error_response(400, "Reservation", 'Only 3 other machines can run while the 1.21 gigawatt lightning harvester is operating')
            
    return True, None

def check_hvc_requirements(all_reservations, day, start_time, end_time):
    """
    Given a start time and an end time, check that on a given day, the hvc machine
    is used in accordance with the cooldown rules

    Args:
        all_reservations (ReservationManager): The reservation manager of the system
        day (datetime): the datetime object of the day that is being checked
        start_time (str): the start time of this reservation
        end_time (str): the finish time of this reservation

    Returns:
        (True, None) if the hvc is being operated within requirements, (False, error response) otherwise
    """
    hvc_start = start_time - 60
    hvc_end = end_time + 60
    for reservation in all_reservations:
        if reservation.reservation_type == 'hvc':
            if not between(f'{day.month}-{day.day}-{day.year}', reservation.start_date, reservation.end_date):
                continue
            reservation_start, reservation_end = split_time(reservation.start_time, reservation.end_time)
            if not (hvc_end <= reservation_start or reservation_end <= hvc_start):
                print(f'Reservation Failed: high velocity crusher needs to cool down for 6 hours between uses, hvc currently reserved for {reservation.start_time}-{reservation.end_time}.')
                return False, error_response(400, "Reservation", f'High velocity crusher needs to cool down for 6 hours between uses, hvc currently reserved for {reservation.start_time}-{reservation.end_time}.')
    return True, None

def check_irradiator_requirements(all_reservations, day, start_time, end_time):
    """
    Given a start time and an end time, check that on a given day, the irradiator
    is used in accordance with the cooldown rules

    Args:
        all_reservations (ReservationManager): The reservation manager of the system
        day (datetime): the datetime object of the day that is being checked
        start_time (str): the start time of this reservation
        end_time (str): the finish time of this reservation

    Returns:
        (True, None) if the irradiator is being operated within requirements, (False, error response) otherwise
    """
    irradiator_start = start_time - 10
    irradiator_end = end_time + 10
    count = 0
    for reservation in all_reservations:
        if reservation.reservation_type == 'irradiator':
            if not between(f'{day.month}-{day.day}-{day.year}', reservation.start_date, reservation.end_date):
                continue
            reservation_start, reservation_end = split_time(reservation.start_time, reservation.end_time)
            if not (irradiator_end <= reservation_start or reservation_end <= irradiator_start):
                count += 1
    if count == 2:
        print(f'Reservation Failed: irradiators need to cool down for 1 hour between uses.')
        return False, error_response(400, "Reservation","Irradiators need to cool down for 1 hour between uses")
    return True, None

def handle_reservation(all_reservations, reservation):
    """
    Given a reservation, check all conditions to see if it is a valid reservation
    that does not break any of the reservation rules

    Args:
        all_reservations (ReservationManager): The reservation manager of the system
        reservation (Reservation): The reservation to be made

    Returns:
        (True, None) if it is the reservation can be made in accordance to all
        the rules, (False, error response) otherwise
    """
    # Unpack all required data from the Reservation object
    customer_id = reservation.customer_id
    reservation_type = reservation.reservation_type
    start_datetime = datetime.strptime(reservation.start_date, "%m-%d-%Y")
    end_datetime = datetime.strptime(reservation.end_date, "%m-%d-%Y")
    start_time = reservation.start_time
    end_time = reservation.end_time
    reservation_datetime = datetime.strptime(reservation.date_of_reservation, "%m-%d-%Y")

    # Check if the type of machine is known
    failed, error = reservation_type_is_not_known(reservation_type)
    if failed:
        return False, error

    failed, error = reservation_is_not_in_date_range(reservation_datetime, start_datetime, end_datetime)
    if failed:
        return False, error
    
    # Convert hour and minue to form 105 for 10:30, 160 for 16:00
    original_start_time = start_time
    original_end_time = end_time
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))
    start_time = start_hour * 10 + start_minute // 30 * 5
    end_time = end_hour * 10 + end_minute // 30 * 5

    failed, error = reservation_is_not_on_half_hour(start_minute)
    if failed:
        return False, error
    failed, error = reservation_is_not_on_half_hour(end_minute)
    if failed:
        return False, error

    # A list of days to make reservations for, based on start date and end date
    days_to_reserve = []
    cur = start_datetime
    while (end_datetime - cur).days >= 0:
        days_to_reserve.append(cur)
        cur += timedelta(days=1)
    
    # Check if the workshop is open for each of the reservation days
    for day in days_to_reserve:
        if workshop_is_closed(start_time, end_time, day):
            print(f'Reservation Failed: cannot reserve time interval from {original_start_time} to {original_end_time} on {str(day).split()[0]}')
            return False, error_response(400, "Reservation", f'Cannot reserve time interval from {original_start_time} to {original_end_time} on {str(day).split()[0]}')
    
    # Make sure that one client only makes one special machine reservation at any time
    succeeded, error = check_only_one_special_machine(all_reservations, days_to_reserve, reservation)
    if not succeeded:
        return False, error
    
    # For each day in the attempted reservation, check that it does not violate some
    # requirement for booking to be successful
    for day in days_to_reserve:
        # Check that all non-cooldown rules for a reservation
        succeeded, error = check_non_cooldown_requirements(all_reservations, day, reservation_type, start_time, end_time)
        if not succeeded:
            return False, error
        
        # check that the high velocity crusher has 6 hours cooldown between uses
        if reservation_type == 'hvc':
            succeeded, error = check_hvc_requirements(all_reservations, day, start_time, end_time)
            if not succeeded:
                return False, error
    
        # check that irradiators have a 60 minutes cooldown period after use
        if reservation_type == 'irradiator':
            succeeded, error = check_irradiator_requirements(all_reservations, day, start_time, end_time)
            if not succeeded:
                return False, error
    
    # Check if A customer is going to go over 3 reservations in a given week
    failed, error = over_three_reservations(all_reservations, days_to_reserve, customer_id)
    if failed:
        return False, error
    
    return True, None


def handle_request(request):
    """
    Main function of this reservation program, the format of commands are as follows:
    reserve.py reserve <customer_id> <resource> <start_date> <end_date> <start_time> <end_time> <reserve_date>
    reserve.py cancel <reservation_id> <cancel_date>
    reserve.py reservations <start_date> <end_date>
    reserve.py financial <start_date> <end_date>
    reserve.py reservations <start_date> <end_date> <customer_id>
    
    Any date is of the form mm-dd-yyyy
    Any time is of the form hh:mm in 24 hour format

    Handle the above requests by loading the data from data.txt, performing request
    and then saving updated data back into data.txt

    Args:
        request (list): A list of comand and arugments

    Returns:
        (True, response) if success, (False, error) otherwise
    """

    # Initialize DataManager
    data_file = parse_data_file()
    data_manager = persist.DataManager(data_file)

    response = None

    # Handle request
    command = request[0]
    if command == 'reserve':
        # Get all the required arguments from the command line
        reserve_request = ReserveRequest(request[1:])
        # Check if the reservation is possible
        all_reservations = data_manager.all_reservations()
        success, error = handle_reservation(all_reservations, reserve_request)
        if not success:
            data_manager.close()
            return False, error
        # Make the reservation
        reservation_id = get_new_reservation_id(data_manager)
        reservation_info, discount = generate_reservation_details(reservation_id, reserve_request)
        new_reservation = persist.Reservation(reservation_info)
        data_manager.add_reservation(new_reservation)
        # Add a transaction for this reservation
        staff_id = request[8]
        transaction_id = get_new_transaction_id(data_manager)
        transaction_date = new_reservation.date_of_reservation
        transaction_info = generate_transaction_details(transaction_id, 'RESERVATION', transaction_date, reservation_info, str(int(time.time())), staff_id)
        new_transaction = persist.Transaction(transaction_info)
        data_manager.add_transaction(new_transaction)
        # Print reservation successful message (including total cost and down payment)
        print(f"Reservation succeeded! Reservation id: {new_reservation.reservation_id}, Total cost: ${new_reservation.total_cost}, down payment: ${new_reservation.down_payment}.")
        response = reservation_response_detail(new_reservation, discount)
    
    elif command == 'cancel':
        reservation_id = int(request[1])
        cancel_date = request[2]
        # Find the reservation to be cancelled
        reservation = data_manager.select_reservation(reservation_id)
        
        if not reservation:
            data_manager.close()
            return False, error_response(400, "Cancellation", f"Invalid reservation id: {reservation_id}")
        
        # Delete the reservation from the database
        data_manager.delete_reservation(reservation_id)
        
        # Ask the transaction manager to manage refund and record refund
        percent_returned, refund = calculate_refund(reservation, cancel_date)

        # Add a cancellation transaction
        staff_id = request[3]
        transaction_id = get_new_transaction_id(data_manager)
        transaction_info = generate_transaction_details(transaction_id, f'CANCELLATION${refund}', cancel_date, reservation.tolist(), str(int(time.time())), staff_id)
        new_transaction = persist.Transaction(transaction_info)
        data_manager.add_transaction(new_transaction)

        print(f"Cancellation succeeded! Refund: ${refund}")

        response = cancellation_response_detail(percent_returned, refund)
    
    elif command == 'reservations':
        start_date = request[1]
        end_date = request[2]
        customer_id = request[3] if len(request) == 4 else ""
        all_reservations = data_manager.all_reservations()
        response = generate_reservations_report(all_reservations, start_date, end_date, customer_id)
    
    elif command == 'financial':
        # List transactions between the two dates
        start_date = request[1]
        end_date = request[2]
        all_transactions = data_manager.all_transactions()
        response = generate_transactions_report(all_transactions, start_date, end_date)
    
    else:
        print(f"Unsupported command: {command}")
        data_manager.close()
        return False, error_response(400, "Cancellation", f"Invalid request: {command}")
    
    data_manager.close()
    return True, response


def error_response(code, operation_name, detail):
    """
    Construct a error response

    Args:
        code (int): status code
        operation_name (str): name of the operation that causes an error
        detail (str): error message

    Returns:
        A dict object containing detail information of the error response
    """
    return {
        "status_code": code,
        "operation_name": operation_name,
        "detail": detail
    }


def reservation_response_detail(new_reservation: persist.Reservation, discount):
    """
    Construct detail of a reservation

    Args:
        new_reservation (Reservation): a Reservation object
        discount (int): an interger representing discount

    Returns:
        A dict object containing detail information of the reservation
    """
    return {
        'reservation_id': str(new_reservation.reservation_id),
        'discount': str(discount),
        'total_cost': str(new_reservation.total_cost),
        'down_payment': str(new_reservation.down_payment)
    }


def cancellation_response_detail(percent_returned, refund):
    """
    Construct detail of a cancellation

    Args:
        percent_returned (int): percentage of the refund to total cost
        refund (float): money refunded to the customer 

    Returns:
        A dict object containing detail information of the cancellation
    """
    return {
        'percent_returned': str(percent_returned),
        'refund': str(refund)
    }


#--------------------------------- helpers -------------------------------------#


class ReserveRequest:
    def __init__(self, request_info):
        self.customer_id = request_info[0]
        self.reservation_type = request_info[1]
        self.start_date = request_info[2]
        self.end_date = request_info[3]
        self.start_time = request_info[4]
        self.end_time = request_info[5]
        self.date_of_reservation = request_info[6]


def calculate_totalcost_discount(reserve_request):
    """
    Calculate the total cost and discount based on the current ReserveRequest object

    Args:
        reserve_request (ReserveRequest): a ReserveRequest object

    Returns:
        total cost (float), discount (int)
    """
    
    start_date = datetime.strptime(reserve_request.start_date, "%m-%d-%Y")
    end_date = datetime.strptime(reserve_request.end_date, "%m-%d-%Y")
    date_of_reservation = datetime.strptime(reserve_request.date_of_reservation, "%m-%d-%Y")
    
    # Note that if the reservation start date and end date are different days
    # It is considered to be multiple appointments from start_time to end_time
    # for each of those days, not from start_day start_time to end_day end_time
    days = (end_date - start_date).days + 1
    start_hour, start_minute = map(int, reserve_request.start_time.split(':'))
    end_hour, end_minute = map(int, reserve_request.end_time.split(':'))

    # Number of half hour blocks for this reservation
    half_hours = (end_hour - start_hour) * 2
    half_hours += -start_minute // 30 + end_minute // 30
    half_hours *= days

    # Base price
    total_cost, discount = 0, 0
    if reserve_request.reservation_type == 'workshop':
        total_cost = half_hours * 99 / 2
    elif reserve_request.reservation_type == 'microvac':
        total_cost = half_hours * 1000 / 2
    elif reserve_request.reservation_type == 'irradiator':
        total_cost = half_hours * 2220 / 2
    elif reserve_request.reservation_type == 'extruder':
        total_cost = half_hours * 600 / 2
    elif reserve_request.reservation_type == 'hvc':
        total_cost = half_hours * 10000
    elif reserve_request.reservation_type == 'harvester':
        total_cost = half_hours * 8800 / 2
    else:
        print(f"Unsupported resource: {reserve_request.reservation_type}.")

    # Discount by 75% if reservation is made 14 days in advance
    if (start_date - date_of_reservation).days >= 14:
        total_cost *= 0.75
        discount = 25
    
    return total_cost, discount


def down_payment_percent(reserve_request: ReserveRequest):
    """
    Calculate the amount of down payment that needs to be made
    based on the total cost of the reservation

    Args:
        reserve_request (ReserveRequest): a ReserveRequest object
    
    Returns:
        A float representing down payment percent rate
    """
    if reserve_request.reservation_type == 'workshop':
        return 0.0
    return 0.5


def get_new_reservation_id(data_manager):
    """
    Create a new reservation id
    
    Args:
        data_manager (DataManager): a DataManager object
    
    Returns:
        An integer
    """
    return data_manager.max_reservation_id() + 1


def get_new_transaction_id(data_manager):
    """
    Create a new transaction id
    
    Args:
        data_manager (DataManager): a DataManager object
    
    Returns:
        An integer
    """
    return data_manager.max_transaction_id() + 1


def generate_reservation_details(reservation_id, reserve_request: ReserveRequest):
    """
    Create reservation details
    
    Args:
        reservation_id (int): reservation id
        reserve_request (ReserveRequest): a ReserveRequest object
    
    Returns:
        A list containing reservation info (List[str])
        discount (int)
    """
    total_cost, discount = calculate_totalcost_discount(reserve_request)
    print(total_cost)
    down_payment = total_cost * down_payment_percent(reserve_request)
    print(down_payment)
    reservation_info = [str(reservation_id), reserve_request.customer_id, reserve_request.reservation_type,
                    reserve_request.start_date, reserve_request.end_date, reserve_request.start_time, 
                    reserve_request.end_time, reserve_request.date_of_reservation, str(total_cost), str(down_payment)]
    return reservation_info, discount


def generate_transaction_details(transaction_id, transaction_type, transaction_date, reservation_info, timestamp, staff_id):
    """
    Create transaction details
    
    Args:
        transaction_id (str): transaction id
        transaction_type (str): type of the transaction
        transaction_date (str): date of the transaction
        reservation_info (List[str]): A list containing reservation info
        timestamp (str): time of the transaction
        staff_id (str): id of the operating staff
    
    Returns:
        A list containing transaction info (List[str])
    """
    return [transaction_id, transaction_type, transaction_date] + reservation_info + [timestamp, staff_id]


def calculate_refund(cancelled_reservation, cancel_date):
    """
    Given a cancelled reservation and the date on which the cancellation ismade
    Calculate the amount that should be refunded and make the refund by
    recording it as a cancellation transaction

    Args:
        cancelled_reservation (Reservation): The reservation to refund
        cancel_date (str): the date on which the cancellation is requested
    
    Returns:
        percent of total cost refunded
        refund
    """
    # print refund
    start_date = datetime.strptime(cancelled_reservation.start_date, "%m-%d-%Y")
    cancel_datetime = datetime.strptime(cancel_date, "%m-%d-%Y")
    refund = 0
    days_before_reservation = (start_date - cancel_datetime).days

    percent_returned = 0
    # calculate the amount of refund based on how many days ahead
    if days_before_reservation >= 7:
        percent_returned = 75
        refund = 0.75 * cancelled_reservation.down_payment
    elif days_before_reservation >= 2:
        percent_returned = 50
        refund = 0.5 * cancelled_reservation.down_payment

    return percent_returned, refund


def generate_reservations_report(all_reservations, start_date, end_date, customer_id):
    """
    Generate a JSON report of all reservations in the system based
    Formatted according to the API design dcoument

    Args:
        all_reservations(List[Reservation]): a list of reservations
        start_date (str): The starting date of reservations to report on 
        end_date (str): The ending date of reservations to report on
        customer_id (str): OPTIONAL, the customer ID to generate report on

    Returns:
        A JSON formatted report in accordance with API design document for
        the 'GET reservations' API endpoint
    """
    list_reservation_data = []
    for reservation in all_reservations:
        # If customer id matches or not specified
        if (customer_id == "" or reservation.customer_id == customer_id):
            # Print all reservations between this date
            if between(reservation.start_date, start_date, end_date):
                list_reservation_data.append({
                    "reservation_id":reservation.reservation_id,
                    "customer_id": reservation.customer_id,
                    "resource": reservation.reservation_type,
                    "start_date": reservation.start_date,
                    "end_date": reservation.end_date,
                    "start_time": reservation.start_time,
                    "end_time": reservation.end_time,
                    "total_cost": reservation.total_cost, 
                    "down_payment": reservation.down_payment
                })
    return {"reservations": list_reservation_data}


def generate_transactions_report(all_transactions, start_date, end_date):
    """
    Generate a JSON report of all transactions in the system based
    Formatted according to the API design given in web.py

    Args:
        all_transactions(List[Transaction]): a list of transactions
        start_date (str): The starting date of transaction to report on 
        end_date (str): The ending date of transactions to report on

    Returns:
        A JSON formatted report in accordance with API design document for
        the 'GET transactions' API endpoint
    """
    list_transaction_data = []
    for transaction in all_transactions:
        if between(transaction.transaction_date, start_date, end_date):
            reservation = transaction.detail
            transaction_type = transaction.type.split("$")
            transaction_amount = reservation.down_payment
            if len(transaction_type) == 2:
                transaction_amount = transaction_type[1]
            transaction_type = transaction_type[0]

            list_transaction_data.append({
                "transaction_id": transaction.transaction_id,
                "transaction_type": transaction_type,
                "transaction_date": transaction.transaction_date,
                "reservation_id": reservation.reservation_id,
                "customer_id": reservation.customer_id,
                "resource": reservation.reservation_type,
                "total_cost": reservation.total_cost,
                "transaction_amount": transaction_amount
            })
    return {"transactions": list_transaction_data}


def parse_data_file():
    """
    Parse the config file to get data file

    Returns:
        data file path
    """
    config_file = "config.json"
    with open(config_file, "r") as cf:
        config = json.load(cf)
        return config["data_file"]