import csv, os, sys
from datetime import datetime

file_name = 'NVidia History from Thomas.csv'
# can the file be found in the current directory?
if os.path.exists(file_name):
    print(f"\nThe file '{file_name}' exists.")
else:
    print(f"\nThe file '{file_name}' does not exist.\n")
    sys.exit()

# normalize_date() converts the date string into a standardized format (MM/DD/YYYY) string
# input: date as a string type in the form month/day/year
# output: date as a string type in the form ""
def normalize_date(date_str):
    try:
        month, day, year = date_str.split('/')
        if len(year) == 2:  # Handle 2-digit years (e.g., '99' or '05')
            year = '19' + year if int(year) > 50 else '20' + year
        # Ensure the components are valid integers
        month = int(month)
        day = int(day)
        year = int(year)

        # Ensure valid ranges for month, day, year
        if not (1 <= month <= 12):
            return None
        if not (1 <= day <= 31): 
            return None
        if not (1900 <= year <= 2050):  
            return None
        return f'{month:02}/{day:02}/{year}'

    except (ValueError, IndexError):
        return None  # Return None if the date is invalid or improperly formatted

# Read the CSV file and normalize dates
data = []
with open(file_name, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Assuming the first row is the header
    for row in reader:
        if len(row) >= 2 and row[0].strip() and row[1].strip():  # Ensure date and price exist
            normalized_date = normalize_date(row[0].strip())
            if normalized_date:
                try:
                    price = float(row[1].strip())  # Convert price to float
                    data.append([normalized_date, price])
                except ValueError:
                    print(f"Skipping row with invalid price: {row}")
            else:
                print(f"Skipping row with invalid date: {row}")
        else:
            print(f"Skipping malformed row: {row}")

# Sort data by the normalized date
# Note that our original data file is already sorted chronologically
data.sort(key=lambda x: datetime.strptime(x[0], '%m/%d/%Y'))

# binary_search() tries to find the stock price for a specific date using binary search
# inputs: 1. list of dates and stock prices, 2) date of desired stock price
# returns: stock price (if found)
def binary_search(data, target_date):
    target_date = normalize_date(target_date)
    if not target_date:
        return None
    left, right = 0, len(data) - 1
    date_format = "%m/%d/%Y"

    while left <= right:
        mid = (left + right) // 2
        current_date = data[mid][0]
        current_date_obj = datetime.strptime(current_date, date_format)
        target_date_obj = datetime.strptime(target_date, date_format)

        if current_date_obj == target_date_obj:
            return data[mid][1]  # Return the stock price
        elif current_date_obj < target_date_obj:
            left = mid + 1
        else:
            right = mid - 1

    return None

# ask_for_dates() is the main loop to keep rerunning the program
# inputs: no arguments are passed in; function gets input from user
# returns result of binary search for stock price on the desired date
def ask_for_dates():
    while True:
        user_input = input("Enter a date (MM/DD/YYYY) or type 'stop' to end: ")
        if user_input.lower() == 'stop':
            print("Program stopped.")
            break
        else:
            try:
                price = binary_search(data, user_input)
                if price is not None:
                    print(f"Stock price on {user_input}: ${price}\n")
                else:
                    print(f"Date {user_input} not found or invalid.\n")
            except ValueError:
                print(f"Invalid date format: {user_input}. Please enter a valid date in MM/DD/YYYY format.\n")

# Start asking for dates
ask_for_dates()
