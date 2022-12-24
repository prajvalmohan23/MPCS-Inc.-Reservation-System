# <b>MPCS Inc. Reservation System</b>
### A Resource and Workshop Reservation System 


**Updated**: May 5 2022<br>
**Version**: v2_0

# Team Members

Prajval Mohan<br>
Thanushri Rajmohan<br>
Hanze Hu<br>
Yusen Zhang

# System Instructions
## Server
**Documentations**: `http://127.0.0.1:800/v1_0/docs` <br>
The preset data file could loaded by running the python file within the server subdirectory:
```
cd server
python tests/reset.py
```
The server should be run with uvicorn in the following style:
```
cd server
uvicorn web:app --reload
```

## Client
The client side program could be run by running the front.py file in the client directory
```
cd client
python main_front.py
```

## Testing
To run server side tests
```
cd server
python tests/reset.py
pytest
python tests/restore.py
```

To run frontend tests
```
cd client
pytest
```

## Transactions Listing
Update data/data.txt to the datafile currently in use
```
cd server
python list_transactions.py <data/data.txt>
```

# Simplifications
1. The system does not check for the uniqueness of a given user id, in our implementation we have assumed that the ID is unique. Also, we assume that there is going to be no space in names and IDs.
2. Although specification did not say we have to authenticate users, we authenticate that users exists on the system before showing the function menu to prevent users from finding out about not being allowed to use certain commands after they have finished inputting all required data.

# Salient Features
1. Feature: "Users should have associated roles: REGULAR staff or ADMIN" added.
2. Feature: "Regular staff should be able to perform all functions in the system except user management" added.
3. Feature: "Admins should also be able to add or remove users and change users' roles" added.
4. Feature: "Admins should not be able to remove the last admin, either by changing their role or deleting them as a user" added.
5. The project's data and documentation is updated to include role information and admin functionality.
6. Implemented all requirements from A-01 including all special requirements.
7. Implemented persistence mechanism in such a way as to not generate loss of work, change is made to the data file as soon as requests are received on the API endpoints.
8. The UI is very user friendly and We limited the number of results demonstrated so as to avoid overwhelming users.
9. Besides basic tests to show that our API works, we also test error handling (try/catch) ability of our server.
10. No apparent code smell.
11. We follow coding style guide totally.
12. We streamline the seed data handling by providing reset.py
13. The database is resettable.
14. We implemented automated tests for all the layers of the system.
15. We have used the pytest features of parametrize.

## Git Commit and Branching Policy
- All new features should be implemented in a seperate feature branch
- All commits should have a clear, relevant description of what was implemented in that commit
- Once a feature has been completed, and there's no remaining conflict, the branch should be merged onto _dev_ by the author of the branch


# Description of the Reservation System
## Introduction
The MPCS Inc. Reservation System starts off by printing a welcome message and asking the user to run the terminal on full screen. This is because, sometimes, if the enteries are long, the displays might run into multiple lines and make the output look confusing.

First, the user is asked to enter his/her staff ID. This input is authenticated by checking if it has spaces or if the ID entered is invalid. If an issue is detected, an error message will pop up. 

## Main Menu
If the Staff ID entered is correct, the user session begins and the Main Menu of the reservation system pops up. The main menu has the following options:

1. Make a reservation <br>
2. Make a recurring reservation<br>
3. Cancel a reservation<br>
4. Generate report of the current reservations over a particular time period<br>
5. Get financial transactions over a particular time period<br>
6. Manage staff<br>
7. Logout<br>

Now, the user is prompted to enter his/her choice. <br>

## If the user picked ...
## ... Option 1 ...
... He/she wants to make a reservation. Both the **admin and the regular user can make** a reservation. The user will be prompted with the reservation menu, which is displayed as follows:

### Reservation Menu
Equipment in facility:<br>
1. Press W for workshop
2. Press M for mini microvacs
3. Press I for irradiators
4. Press P for polymer extruders
5. Press C for high velocity crusher
6. Press H for 1.21 gigawatt lightning harvester
7. Press E for exit

Here, the user is asked to pick the device and input his/her details for the device he/she wants to reserve.<br>
The reservations of every device (from 1-6) is in accordance to the "E-requirement" of A-01, and follows all the regular and special constraints. <br>
If the user clicked "E" he is redirected to the Main Menu.

## ... Option 2 ...
... He/she wants to make a recurring reservation. Both the **admin and the regular user** can make a recurrig reservation. The user will be prompted with the reservation menu, which is displayed as follows:

### Reservation Menu
Equipment in facility:<br>
1. Press W for workshop
2. Press M for mini microvacs
3. Press I for irradiators
4. Press P for polymer extruders
5. Press C for high velocity crusher
6. Press H for 1.21 gigawatt lightning harvester
7. Press E for exit

Here, the user is asked to pick the device and input his/her details for the device he/she wants to reserve.<br>
The reservations of every device (from 1-6) is in accordance to the "E-requirement" of A-01, and follows all the regular and special constraints. <br>
If the user clicked "E" he is redirected to the Main Menu.

## ... Option 3 ...
... He/she wants to cancel a pre-existing reservation. Both the **admin and the regular user can cancel** a reservation.<br>
The user is asked to enter the transaction ID he/she wants to cancel, which is cancelled after confirmation.

## ... Option 4 ...
... He/she wants to get the current reservations for a given date range. Both the **admin and the regular user can access** them.<br>
Here, if the you enter a "user ID" you get the current reservations of that particular user in the entered date range, else, you get all reservations in that given date range.

## ... Option 5 ...
... He/she wants to get the financial transactions over a given date range. Both the **admin and the regular user can access** them.<br>

## ... Option 6 ...
... He/she wants to manage the staff. **Only Admins can successfully make these changes**. When this option is selected, the user is presented with the following menu:

### Staff Management Menu
Select task you want to perform:<br>
1. Press A for adding staff
2. Press D for deleting staff
3. Press U for updating staff  
4. Press E for exit

The user is now asked to pick an option.<br>

#### Option A
If the user picks A he/she wants to add a staff member. He/she will be asked for the following inputs - Staff ID to be added and Staff Role (optional: by default REGULAR). If the user performing the task is an Admin, he/she will be able to complete the action, else, he/she will be presented with an error message stating that he/she needs to be an Admin in order to complete this action. Other issues that might cause this action to fail are if the staff ID already exists or if the input is invalid.

#### Option D
If the user picks D, he/she wants to delete a staff member. He/she will be asked to input the ID of the staff he/she wants to delete. If the user performing the task is an Admin, he/she will be able to complete the action, else, he/she will be presented with an error message stating that he/she needs to be an Admin in order to complete this action. Another issue that might cause this action to fail is if the Staff ID to be deleted does not exist.

#### Option U
If the user picks U, he/she wants to update a staff member. He/she will be asked for the following inputs - ID of the staff to be modified and role the staff is to be modified to. If the user performing the task is an Admin, he/she will be able to complete the action, else, he/she will be presented with an error message stating that he/she needs to be an Admin in order to complete this action. Another issue that might cause this action to fail is if the Staff ID to be modified does not exist or if the input given in is invalid.

#### Option E
If the user picks E, he/she wants to exit from this action. When this option is selected, the user is redirected to the Main Menu.

## ... Option 7 ...
... He/she wants to loggout of the current user session. If the user logs out, he/she is asked if he/she wants to login with a different Staff ID. If the user enters No, the system shuts off, else, the entire process repeats.

# Backend Design
1. Backend contains two parts: the reserve system and the user management system. And we seperate these two parts.
2. The reserve system has a typical layered structure. It contains three layers, namely web layer (web.py), business logic layer (reserve.py), and persistence layer (persist.py). The web layer only depends on the business logic layer, and the business logic layer only depends on the persistence layer.
3. The user management system also has the same layers. The web layer is implemented in web.py and user_management_models.py. The business logic layer is in user_management.py and The persistence layer is in user_management_persist.py.
4. The pathes of files storing reserve sytem data and users are specified in config.json. We can redirect output and input to other files by changing config.json.
5. Our approach of IO operations: the system does IO operations for each request independently. Specifically, for each request, the system will load data file into memory, read/write in-memory data structures, and then save all data to disk. Another possible approach: load data into memory when the first request comes, read/write in-memory data structures for subsequent requests, and save data to disk after the last request is handled. Our approach may be less efficient but is more robust. And the performace issue will be solved once we migrate to real database.


## Contact
For any questions please contact:<br>
Prajval Mohan<br>
prajval.mohan23@gmail.com