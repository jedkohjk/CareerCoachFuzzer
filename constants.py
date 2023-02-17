from functions import *
from generator.main import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

# Stores the constants used in the program

FIELD_ORDER = ('Name', 'NRIC', 'Contact Number', 'Email Address')
MAX_WAIT = 20
SITE = 'https://stg.mycareers.coach/'
USERNAME = 'wsgcoach1'
PASSWORD = 'appian@Mar2022'
APPIAN_BUTTON = '/html/body/div[4]/div/div[3]/div[1]/a'
USERNAME_FIELD = '/html/body/div[4]/div/form[2]/div[1]/div/input'
PASSWORD_FIELD = '/html/body/div[4]/div/form[2]/div[2]/div/input'
LOGIN_BUTTON = '/html/body/div[4]/div/form[2]/div[3]/div/div[2]/input'
SEARCH_FIELD = '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div[2]/div/input'
SEARCH_BUTTON = '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div/button'
TABLE = '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[5]/div[2]/div/div/table/tbody'
TABLE_HEADER = 'Name\nSortable column, sorted ascending, activate to sort descending\nNRIC\nSortable column, activate to sort ascending\nContact Number\nSortable column, activate to sort ascending\nEmail Address\nSortable column, activate to sort ascending\n'
DEFAULT_TABLE = 'No items available'
NO_RECORDS = "No matching records found, please try using an alternative search criteria, e.g. Name, Contact Number or Email. If you are searching via NRIC or GUID, please submit your search with the client's full NRIC or GUID."
AC2 = '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[6]/div[2]/div/p'
AC5 = '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div[2]/div[2]'
AC5_MSG = 'Please provide at least one input to start searching'
ITEM_COUNT = '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[5]/div[2]/div/div[2]/div/div'
NEXT_PAGE = '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[5]/div[2]/div/div[2]/div/div/span[4]/a[1]'
EXCESS = '/html/body/div[2]/div[1]/main/div/div/div[1]/div/div/div[6]/div[2]/div/p'
EXCESS_MSG = '• Your search criteria has returned more than 50 records, and only the first 50 records will be shown.\n• If you are not able to find the required record, please refine your search criteria (eg search by full NRIC, input more characters/ numbers) to perform a new search.'
