# File Name: user_management.py
# File Description: Contains model strutures for user management
#
# Date: May 5, 2022

from typing import Optional
from pydantic import BaseModel

class StaffRequest(BaseModel):
    """
    A request parent class that contains neccessary data for all user management
    related request

    Attributes:
        staff_id (str): The ID of the staff making the request
    """
    staff_id: str

class PostStaffsRequest(StaffRequest):
    """
    A class POST request to the Staffs API endpoint

    Attributes:
        new_staff_id (str): The ID/username of the staff to create
        staff_role (str): OPTIONAL, Permission role of the new user, Regular by default
        staff_id (str)(Inherited): The ID of the staff making the request
    """
    new_staff_id: str
    staff_role: Optional[str] = "REGULAR"

class PutStaffsRequest(StaffRequest):
    """
    A class PUT request to the Staffs API endpoint

    Attributes:
        staff_to_update_id (str): The ID/username of the staff to update
        staff_role (str): Permission role of the staff user
        staff_id (str)(Inherited): The ID of the staff making the request
    """
    staff_to_update_id: str
    staff_role: str

class DeleteStaffsRequest(StaffRequest):
    """
    A class DELETE request to the Staffs API endpoint

    Attributes:
        staff_to_delete_id (str): The ID/username of the staff to delete
        staff_id (str)(Inherited): The ID of the staff making the request
    """
    staff_to_delete_id: str
    staff_id: str