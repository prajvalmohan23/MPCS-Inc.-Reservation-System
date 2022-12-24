# File Name: test_user_management.py
# File Description: Contains the tests for user_management functionality
#
# Date: May 5, 2022

from fastapi.testclient import TestClient
from user_management import *
import pytest
import json
import shutil
import os
import web

def current_env():
    return os.path.abspath(__file__)

DATA_FILE = current_env() + "/../data/test_user_data.json"
BACKUP_FILE = current_env() + '/../data/test_user_data_backup.json'

def reset_data_file():
    shutil.copyfile(BACKUP_FILE, DATA_FILE)

def update_staff_config(new_config_file):
    config_file = os.path.abspath(__file__) + "/../../config.json"
    with open(config_file, "r") as cf:
        config = json.load(cf)
    
    output = config["staff_data_file"]
    config["staff_data_file"] = new_config_file
    with open(config_file, "w") as cf:
        json.dump(config, cf)
    return output

class TestUserManagementAPI:
    client = TestClient(web.app)
    temp_config = update_staff_config("tests/data/test_user_data.json")
    '''
    Test both valid and invalid cases for API calls to staffs endpoint
    '''
    def test_update_config(self):
        reset_data_file()

    @pytest.mark.parametrize("new_staff,staff_id,role,response_code",
        [
            ("peter", "hanzeh", "REGULAR", 201),
            ("spencer", "yusen", "REGULAR", 403),
            ("peter", "hanzeh", "REGULAR", 409),
            ("kariyushi", "hanzeh", "SUPERADMIN", 400)
        ]
    )
    def test_api_create_staff(self, new_staff, staff_id, role, response_code):
        """
        Test various POST API calls to the /staff endpoint and check their
        response
        """
        response = self.client.post("/v2_0/staffs", json = {
            "new_staff_id": new_staff, "staff_id": staff_id, "staff_role":role})
        assert response.status_code == response_code

    @pytest.mark.parametrize("update_staff,staff_id,role,response_code",
        [   
            ("hanzeh", "hanzeh", "REGULAR", 403),
            ("yusen", "hanzeh", "ADMIN", 200),
            ("hayder", "hayder", "ADMIN", 403),
            ("spencer", "hanzeh", "REGULAR", 404),
            ("hayder", "hanzeh", "SUPERADMIN", 400)
        ]
    )
    def test_api_update_staff(self, update_staff, staff_id, role, response_code):
        """
        Test various PUT API calls to the /staff endpoint and check their
        response
        """
        response = self.client.put("/v2_0/staffs", json = {"staff_to_update_id":
                    update_staff, "staff_id": staff_id, "staff_role":role})
        assert response.status_code == response_code

    @pytest.mark.parametrize("delete_staff,staff_id,response_code",
        [   
            ("kariyushi", "hanzeh", 404),
            ("yusen", "hanzeh", 200),
            ("hayder", "hayder", 403),
            ("hanzeh", "hanzeh", 403)
        ]
    )
    def test_api_delete_staff(self, delete_staff, staff_id, response_code):
        """
        Test various PUT API calls to the /staff endpoint and check their
        response
        """
        response = self.client.delete("/v2_0/staffs", json = {
                    "staff_to_delete_id": delete_staff, "staff_id": staff_id})
        assert response.status_code == response_code

    @pytest.mark.parametrize("staff_id,response_code",
        [   
            ("hanzeh", 200),
            ("staffx", 404)
        ]
    )
    def test_api_login(self, staff_id, response_code):
        """
        Test various PUT API calls to the /staff endpoint and check their
        response
        """
        response = self.client.get("/v2_0/login", json = {"staff_id": staff_id})
        assert response.status_code == response_code

    def test_revert_config(self):
        assert update_staff_config(self.temp_config) == "tests/data/test_user_data.json"

"""
    def test_get_reservations_invalid_start_date(self):
        #Invalid GET reservations request due to invalid start date.
        response = self.client.get("/v2_0/reservations?start_date=19-19-2022")
        assert response.status_code == 400
        assert response.json() == {'detail': 'Get Reservations failed: date format incorrect'}

    def test_get_reservations_invalid_end_date(self):
        #Invalid GET reservations request due to invalid end date.
        response = self.client.get("/v2_0/reservations?end_date=19-19-2022")
        assert response.status_code == 400
        assert response.json() == {'detail': 'Get Reservations failed: date format incorrect'}"""
    
class TestUserManagementHandler:
    def test_post_user_error_no_permission(self):
        # Test when posting user has no permission
        expected = generate_response(403, "yusen does not have permission to manage staffs")
        
        request = PostStaffsRequest(new_staff_id="hanzeh", staff_id="yusen", staff_role="REGULAR")
        actual = handle_user_management_request("POST", request, DATA_FILE)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]

    def test_put_user_error_no_permission(self):
        # Test when posting user has no permission
        expected = generate_response(403, "yusen does not have permission to manage staffs")
        
        request = PutStaffsRequest(staff_to_update_id="hanzeh", staff_id="yusen", staff_role="REGULAR")
        actual = handle_user_management_request("PUT", request, DATA_FILE)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]
    
    def test_delete_user_error_no_permission(self):
        # Test when posting user has no permission
        expected = generate_response(403, "yusen does not have permission to manage staffs")
        
        request = DeleteStaffsRequest(staff_to_delete_id="hanzeh", staff_id="yusen")
        actual = handle_user_management_request("DELETE", request, DATA_FILE)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]

    def test_handler_create_user(self):
        """
        Tests that adding two staff (staff1 and staff2) by an admin succeeds
        with code 201 and updates the datafile as expected
        """
        reset_data_file()
        expected = generate_response(201, "")
        
        request = PostStaffsRequest(new_staff_id="staff1", staff_id="hanzeh")
        actual = handle_user_management_request("POST", request, DATA_FILE)
        assert expected["status_code"] == actual["status_code"]

        request = PostStaffsRequest(new_staff_id="staff2", staff_id="hanzeh", staff_role="ADMIN")
        actual = handle_user_management_request("POST", request, DATA_FILE)
        assert expected["status_code"] == actual["status_code"]

        with open(DATA_FILE) as FILE:
            staff_data = json.load(FILE)
        assert staff_data == {"hanzeh":"ADMIN", "yusen": "REGULAR",
            "hayder": "REGULAR", "staff1": "REGULAR", "staff2": "ADMIN"}

    def test_handler_update_user(self):
        """
        Tests that editing a regular user to and admin and then back to a
        regular user by an admin succeeds with code 200 and updates the datafile
        """
        reset_data_file()
        expected = generate_response(200, "")
        
        request = PutStaffsRequest(staff_to_update_id="yusen",
                    staff_id="hanzeh", staff_role="ADMIN")
        actual = handle_user_management_request("PUT", request, DATA_FILE)
        assert expected["status_code"] == actual["status_code"]

        request = PutStaffsRequest(staff_to_update_id="yusen", staff_id="hanzeh",
                    staff_role="REGULAR")
        actual = handle_user_management_request("PUT", request, DATA_FILE)
        assert expected["status_code"] == actual["status_code"]

        with open(DATA_FILE) as FILE:
            staff_data = json.load(FILE)
        assert staff_data == {"hanzeh":"ADMIN", "yusen": "REGULAR",
                              "hayder": "REGULAR"}

    def test_handler_delete_user(self):
        """
        Tests that deleting a regular user and deleting an admin user succeeds
        with code 200 and updates the datafile
        """
        reset_data_file()
        expected = generate_response(200, "")
        
        request = DeleteStaffsRequest(staff_to_delete_id="hayder", staff_id="hanzeh")
        actual = handle_user_management_request("DELETE", request, DATA_FILE)
        assert expected["status_code"] == actual["status_code"]

        request = PutStaffsRequest(staff_to_update_id="yusen", staff_id="hanzeh",
                    staff_role="ADMIN")
        actual = handle_user_management_request("PUT", request, DATA_FILE)
        assert expected["status_code"] == actual["status_code"]

        request = DeleteStaffsRequest(staff_to_delete_id="yusen", staff_id="hanzeh")
        actual = handle_user_management_request("DELETE", request, DATA_FILE)
        assert expected["status_code"] == actual["status_code"]

        with open(DATA_FILE) as FILE:
            staff_data = json.load(FILE)
        assert staff_data == {"hanzeh":"ADMIN"}

class TestLoginUser:
    """
    Test Functionality for creating new users
    Test the following cases:
        - Successful Login with user being in the system
        - Failure to login due to user not being in the system
    """
    @pytest.mark.parametrize("user_id,response_code",
        [("hanzeh", 200),
         ("yusen", 404)]
    )
    def test_post_user_success(self, user_id, response_code):
        # Test valid post requests
        expected = generate_response(response_code, "")
        
        request = StaffRequest(staff_id=user_id)
        actual = handle_user_management_request("LOGIN", request,
                    current_env() + "/../data/test_user_data.json")

        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]

class TestPostUser:
    """
    Test Functionality for creating new users
    Test the following cases:
        - Successful creation
        - Failure due to lack of authorization
        - Failure due to user_id already existing
        - Failure due to staff_role being incorrect
    """
    def create_request(self, new_staff_id, staff_id, role = "REGULAR"):
        return PostStaffsRequest(new_staff_id= new_staff_id,
                                staff_id = staff_id, staff_role = role)

    def test_post_user_success(self):
        # Test valid post requests
        staff_data = {"hanzeh": "ADMIN"}

        expected = generate_response(201, "staff1 has been created with role REGULAR")
        
        request = self.create_request("staff1", "hanzeh")
        actual = handle_post_user(request, staff_data)

        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]
        assert staff_data == {"hanzeh": "ADMIN", "staff1": "REGULAR"}

    def test_post_user_error_already_exist(self):
        # Test when the user id to be created already exists
        staff_data = {"hanzeh": "ADMIN"}

        expected = generate_response(409, "hanzeh already exists in the system")
        
        request = self.create_request("hanzeh", "hanzeh")
        actual = handle_post_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]

    def test_post_user_error_invalid_role(self):
        # Test when posting user has no permission
        staff_data = {"hanzeh": "ADMIN"}

        expected = generate_response(400, "superadmin is not a valid user role")
        
        request = self.create_request("staff1", "hanzeh", "superadmin")
        actual = handle_post_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]

class TestPutUser:
    """
    Test Functionality for updating existing users
    Test the following cases:
        - Successful creation
        - Failure due to user to be updated to REGULAR being the last ADMIN
        - Failure due to user to be updated being not in system
        - Failure due to staff_role being incorrect
    """
    def create_request(self, update_staff_id, staff_id, role = "REGULAR"):
        return PutStaffsRequest(staff_to_update_id= update_staff_id,
                                staff_id = staff_id, staff_role = role)

    def test_put_user_success(self):
        # Test valid put requests
        staff_data = {"hanzeh": "ADMIN", "yusen": "REGULAR"}

        expected = generate_response(200, "yusen's role has been updated to ADMIN")
        
        request = self.create_request("yusen", "hanzeh", "ADMIN")
        actual = handle_put_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]
        assert staff_data == {"hanzeh": "ADMIN", "yusen": "ADMIN"}


    def test_put_user_error_last_admin(self):
        # Test when changing the last admin to a regular staff
        staff_data = {"hanzeh": "ADMIN"}

        expected = generate_response(403, "hanzeh is the only remaining Admin in the system")
        
        request = self.create_request("hanzeh", "hanzeh")
        actual = handle_put_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]

    def test_put_user_error_user_non_exist(self):
        # Test when the user to be updated does not exist
        staff_data = {"hanzeh": "ADMIN"}

        expected = generate_response(404, "yusen is not in the system")
        
        request = self.create_request("yusen", "hanzeh")
        actual = handle_put_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]

    def test_post_user_error_invalid_role(self):
        # Test when posting user has no permission
        staff_data = {"hanzeh": "ADMIN", "yusen": "REGULAR"}

        expected = generate_response(400, "superadmin is not a valid user role")
        
        request = self.create_request("yusen", "hanzeh", "superadmin")
        actual = handle_put_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]
    
class TestDeleteUser:
    """
    Test Functionality for deleting existing users
    Test the following cases:
        - Successful creation
        - Failure due to user to be updated to REGULAR being the last ADMIN
        - Failure due to user to be deleted not being in the system
    """
    def create_request(self, delete_staff_id, staff_id):
        return DeleteStaffsRequest(staff_to_delete_id= delete_staff_id,
                                    staff_id = staff_id)

    def test_delete_user_success(self):
        # Test valid delete request
        staff_data = {"hanzeh": "ADMIN", "yusen": "REGULAR"}

        expected = generate_response(200, "yusen has been removed from the system")
        
        request = self.create_request("yusen", "hanzeh")
        actual = handle_delete_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]
        assert staff_data == {"hanzeh": "ADMIN"}

    def test_delete_user_error_last_admin(self):
        # Test when deleting the last admin
        staff_data = {"hanzeh": "ADMIN"}

        expected = generate_response(403, "hanzeh is the only remaining Admin in the system")
        
        request = self.create_request("hanzeh", "hanzeh")
        actual = handle_delete_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]

    def test_delete_user_error_user_non_exist(self):
        # Test when the user to be deleted does not exist
        staff_data = {"hanzeh": "ADMIN"}

        expected = generate_response(404, "yusen is not in the system")
        
        request = self.create_request("yusen", "hanzeh")
        actual = handle_delete_user(request, staff_data)
        
        assert expected["status_code"] == actual["status_code"]
        assert expected["detail"] == actual["detail"]