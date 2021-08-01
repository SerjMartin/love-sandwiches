import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
"""
#this import all intire gspread library
#thi import all credintials class wich is part from service_account function
# from the google auth library
"""

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the users
    this function colect sale data from our users
    """
    while True:
        """
         While loop will repet until the data will be
         providet valed
        """
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separted by commas.")
        print("Exemple: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here:")
        """
         # use input() method to get our
         #sale data from the users to the terminal
         #(print(f"The data provide is {data_str}"))will print the data_str
         # provided back to the terminal(to check function)
        """

        sales_data = data_str.split(",")
        """
         # split(",") method retuns the broken up values as a list
         # (print(sales_data)) to check sales_data function if is
         # returning as a list
        """

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, convert all string values into integers.
    Raises ValueError if strings can not be converted into int,
    or if there aren't exactly 6 values.
    #(print(values)) check if validate_data function is working
    """
    try:
        [int(value) for value in values]
        """
         # convert each value from our value list into in integer
          # value list has to beexacly 6 values
         """
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provide {len(values)}"
            )
    except ValueError as e:
        """
          # we are assigning that ValueError object to e
          # variable is stantard Python shorthand for "error"
        """
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


"""

def update_sales_worksheet(data):
    ----------
     (Update sales worksheet, add new row with the list data provided.)
    ----------
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfuly.\n")


def update_surplus_worksheet(data):
    ---------
     (Update surplus worksheet, add new row with the list data provided.)
    ---------
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfuly.\n")
"""


def update_worksheet(data, worksheet):
    """
     Receives a list of integers to be inserted into worksheet
     Update the relevant worksheet with the data providet
     (This function will replace those two function on top)
     calls Refactoring
    """
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
     Compare sales with stock and calculate the surplus for each item type.

     The is definated as the sale figure subtracted from the stock:
     - Posutive surplus indicate waste
     - Negative surplus indicates extra made when stock was soldout
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    """
     stock_row will extract the last row from the stock worksheet
     pprint(stock_row) ysed to check function
     pprint has to be instaled on the file too
    """
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        # used zip() becouse we used two diferent type of data
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    # print(surplus_data) used to check the function
    return surplus_data


def get_last_5_entries_sales():
    """
     Collects collumns  of data from sales worksheet, callecting
     the last 5 entries for each sandwich and returns the data
     as a list of list.
    """
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3) used to check f
    """
     Used variable column becouse we need return in column
     We can access a single column by using the col_values()
     method and request a 3rd column from worksheet
    """
    # print(column) used to check f

    columns = []
    for ind in range(1, 7):  # range of number 1 to 6
        column = sales.col_values(ind)
        columns.append(column[-5:])
        """"
         Used [-5:] to access the last 5 items
         and (:) we want to slice multiple vlues from the list
        """
    # pprint(columns) used to chek f
    return columns


def calculate_stock_data(data):
    """
     Calculate the overage stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    # print(new_stock_data) used to check f
    return new_stock_data


def main():
    """
     Run all progam function
     This function will pass all the data in to worksheets
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    # used int() method to convert num data to integer
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    """
     Call out the function (update_sales_worksheet(data))
     and pas it sales_data list
    """
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    # print(stock_data) to check f
    update_worksheet(stock_data, "stock")
    # this will send data to stock worksheet


print("Welcome to Love Sandwiches Data Automation")
main()  # used to run f: main
