# Schema
The API exchanges JSON objects of the following types:

## ReservationRequest
customer_id: a non-empty string representing id of the customer who wants to create a reservation

resource: a non-empty string representing resource the customer wants to reserve; valid resources: workshop, microvac, irradiator, extruder, hvc (for "high velocity crusher"), and harvester

start_date: a non-empty string representing the starting date of the reservation; format: mm-dd-yyyy

start_time: a non-empty string representing the starting time of the reservation; format: HH:MM

end_date (optional): a non-empty string representing the ending date of the reservation; by default, end_date = start_date; format: same as start_date

end_time (optional): a non-empty string representing the ending time of the reservation; by default, end_time = start_time + 30 minutes; format: same as start_time

staff_id: a non-empty string representing id of the staff using the software

Example:
```
{
	"customer_id": "user1",
	"resource": "workshop",
	"start_date": "04-22-2022"
	"start_time": "09:30"
	"end_date": "04-23-2022"
	"end_time": "10:30"
	"staff_id": "1"
}
```

## ReservationResponse
status_code: a stirng representing status code of the resposne

detail: a JSON object representing detail of the reservation, consisting of the following fields:

reservation_id: a string representing the id of the reservation created

discount: a string of integer, representing discount rate

total_cost: a string representing total cost

down_payment: a string representing down payment

Example:
```
{
	"status_code": "201", 
	"detail": {
        	"reservation_id": "12",
        	"discount": "25", // means 25% off
        	"total_cost": "13.2",
        	"down_payment": "6.6"
    }
}
```

## CancellationRequest
reservation_id: a non-empty string representing id of the reservation that the customer wants to cancel

staff_id: a non-empty string representing id of the staff using the software

Example:
```
{
	"reservation_id": "3",
	"staff_id": "staff1"
}
```

## CancellationResponse
status_code: a stirng representing status code of the resposne

detail: a JSON object representing detail of the cancellation, consisting of the following fields:

percent_returned: a string of integer, representing refund rate

refund: a string of float number, representing refund

Example:
```
{
	"status_code": "200", 
	"detail": {
        	"percent_returned": "75", // means 75% are returned
        	"refund": "5.5",
    }
}
```

## GetReservationsResponse
status_code: a stirng representing status code of the resposne

detail: a JSON object containing a list of reservation_data

reservation_data: a JSON object representing detail of a reservation, consisting of the following fields:

reservation_id: a string representing the id of the reservation

customer_id: a string representing id of the customer who wants to create a reservation

resource: a string representing resource the customer wants to reserve

start_date: a string representing the starting date of the reservation; format: mm-dd-yyyy

start_time: a string representing the starting time of the reservation; format: HH:MM

end_date: a string representing the ending date of the reservation; format: mm-dd-yyyy

end_time: a string representing the ending time of the reservation; format: HH:MM

total_cost: a string representing total cost

down_payment: a string representing down payment

Example:
```
{
	"status_code": "200",
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
```

## GetTransactionsResponse
status_code: a stirng representing status code of the resposne

detail: a JSON object containing a list of transaction_data

transaction_data: a JSON object representing detail of a transaction, consisting of the following fields:

transaction_id: a string representing the id of the transaction

transaction_type: a string representing the type of the transaction; valid values are RESERVATION and CANCELLATION

transaction_date: a string representing the date of the transaction; format: mm-dd-yyyy

reservation_id: a string representing the id of the reservation

customer_id: a string representing id of the customer who created the reservation

resource: a string representing resource the customer reserved

total_cost: a string representing total cost of the reservation

transaction_amount: a string representing down payment if the transaction type is RESERVATION; a string representing refund if the transaction type is CANCELLATION

Example:
```
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
```

## StaffCreationRequest
new_staff_id: a non-empty string representing the id of the staff to be added

staff_role (optional): a non-empty string representing role assigned to the new staff; valid values: "ADMIN" or "REGULAR"; by default, "REGULAR"

staff_id: a non-empty string representing id of the staff using the software

Example:
```
{
	"new_staff_id": "fresh",
	"staff_role": "REGULAR",
	"staff_id": "admin"
}
```

## StaffDeletionRequest
staff_to_delete_id: a non-empty string representing the id of the staff to be deleted

staff_id: a non-empty string representing id of the staff using the software

Example:
```
{
	"staff_to_delete_id": "fresh",
	"staff_id": "admin"
}
```

## StaffUpdateRequest
staff_to_update_id: a non-empty string representing the id of the staff to be added

staff_role: a non-empty string representing role assigned to the new staff; valid values: "ADMIN" or "REGULAR";

staff_id: a non-empty string representing id of the staff using the software

Example:
```
{
	"staff_to_update_id": "fresh",
	"staff_role": "ADMIN",
	"staff_id": "admin"
}
```

## ErrorReponse
detail: error message string

Example:
```
{
	"detail": "Reservation failed: Cannot reserve time interval from 9:00 to 11:00 on 2022-04-30"
}
```


# POST /v2_0/reservations
Create a (recurring) reservation. If end_date is specified and start_date is prior to end_date, a recurring reservation will be created.

Request body: a ReservationRequest object

Query parameters: none

Returns: a ReservationResponse object if success; an ErrorReponse object otherwise

Status codes:
1. 201: success
2. 400: if the request violates any constraints specified in A-01

# DELETE /v2_0/reservations
Cancel a reservation

Request body: a CancellationRequest object

Query parameters: none

Returns: a CancellationResponse object if success; an ErrorReponse object otherwise

Status codes:
1. 200: success
2. 400: if the request violates any constraints specified in A-01

# GET /v2_0/reservations
Request a report of current reservations for a given customer for a given date range

Request body: none

Query parameters:
1. start_date (optional): a non-empty string representing the starting date of the reservation
2. end_date (optional): a non-empty string representing the ending date of the reservation
3. customer_id (optional): a non-empty string representing the customer to generate the report on; by default: generate report on all customers
4. staff_id: a non-empty string representing id of the staff using the software

Returns: a GetReservationsResponse object if success; an ErrorReponse object otherwise

Status codes:
1. 200: success
2. 400: if the request violates any constraints specified in A-01

# GET /v2_0/transactions
Request financial transactions for a given date range

Request body: none

Query parameters:
1. start_date (optional): a non-empty string representing the starting date of the transaction
2. end_date (optional): a non-empty string representing the ending date of the transaction
3. staff_id: a non-empty string representing id of the staff using the software

Returns: a GetTransactionsResponse object if success; an ErrorReponse object otherwise

Status codes:
1. 200: success
2. 400: if the request violates any constraints specified in A-01

# POST /v2_0/staffs
Register a staff

Request body: StaffCreationRequest object

Query parameters: none

Returns: none

Status codes:
1. 201: success
2. 403: if current operating staff is not an admin
3. 409: if staff_id is already in use
4. 400: invalid input

# DELETE /v2_0/staffs
Unregister a staff

Request body: StaffDeletionRequest object

Query parameters: none

Returns: none

Status codes:
1. 200: success
2. 403: if current operating staff is not an admin
3. 404: staff to delete not found

# PUT /v2_0/staffs
Change the role of a staff

Request body: StaffUpdateRequest object

Query parameters: none

Returns: none

Status codes:
1. 200: success
2. 403: if current operating staff is not an admin
3. 404: staff to delete not found
4. 400: invalid input
