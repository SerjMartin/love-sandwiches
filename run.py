# python code goes here
import gspread # this import all intire gspread library 
from google.oauth2.service_account import Credentials # thi import all credintials class wich is part from service_account function from the google auth library 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():# this function colect sale data from our users
     """
     Get sales figures input from the users
     """
     print("Please enter sales data from the last market.")
     print("Data should be six numbers, separted by commas.")
     print("Exemple: 10, 20, 30, 40, 50, 60\n") # using \n for space betwen new line

     data_str = input("Enter your data here:")# use input() method to get our sale data from the users to the terminal
     print(f"The data provide is {data_str}")#will print the data_str provided back to the terminal

get_sales_data()
