# File Name: test_make_and_cancel_reservations_front.py
# File Description: Contains automated tests for make_and_cancel_reservations_front.py
#
# Date: May 6, 2022

# Importing Libraries
from io import StringIO
from unittest.mock import patch
import json
import unittest
import pytest
from pytest import MonkeyPatch 
import requests
#from fastapi.testclient import TestClient
#import web
import datetime
from datetime import timedelta
from datetime import date

from make_and_cancel_reservations_front import *
#client = TestClient(web.app)


class TestHandlerFunctions:
    '''
    Tests both valid and invalid cases all the front end handler functions
    '''

    @pytest.mark.parametrize("test_input, expected", [('W','workshop'),('w','workshop'),\
        ('M','microvac'),('m','microvac'),('I','irradiator'),('i','irradiator'),\
        ('P','extruder'),('p','extruder'), ('C','hvc'), ('c','hvc'), ('H','harvester'), ('h','harvester')])
    def test_resource_name(self,test_input, expected):
        #Tests whether resource abreviations are being mapped correctly.
        assert resource_name(test_input) == expected


    @pytest.mark.parametrize("test_input, expected", [('Y','Yes'),('y','Yes'),('N','No'),('n','No')])
    def test_confirm(self,test_input, expected):
        #Tests whether yes/no abbreviations are being mapped correctly.
        assert confirm(test_input) == expected


    @pytest.mark.parametrize("test_input, expected", [('user1',False),('user 1',True)])
    def test_check_space(self,test_input, expected):
        #Test whether "spaces in username" check is being performed correctly.
        assert check_space(test_input) == expected


    @pytest.mark.parametrize("test_input, expected", [('5-17-2022',True),\
        ('qdwjrf367',False),('100032714',False)])
    def test_check_date(self,test_input, expected):
        #Test whether date format check is being performed correctly.
        assert check_date(test_input) == expected


    @pytest.mark.parametrize("test_input, expected", [('10:00',True),\
        ('qdwjrf367',False),('100032714',False)])
    def test_check_time(self,test_input, expected):
        #Test whether time format check is being performed correctly.
        assert check_time(test_input) == expected
