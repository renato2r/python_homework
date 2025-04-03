import csv
import os
import custom_module
from datetime import datetime

############### Task2 #######################################################

def read_employees():

    myDict = {}
    myList = []
    try:

        with open('../csv/employees.csv','r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)

            myDict['fields'] = headers

            for row in reader:
                myList.append(row)
                
            myDict["rows"] = myList


    except FileNotFoundError:
        print("Error: file was not found")               
        exit(1)

    except Exception as e:
        print(f"An error ocurred: {e}")    
        exit(1)

    return myDict

employees = read_employees()
print(employees)

############ Task3 ############################################

def column_index(string):
    try:
        return employees['fields'].index(string)
    
    except ValueError:
        print(f"Error: Column '`column_name' not found")
        return -1
    except Exception as e:
        print(f"An error ocurred: {e}")
        return -1

employee_id_column = column_index("employee_id")

print(f"Index of 'employee_id' column: {employee_id_column}")

############ Task 4 ###########################################

def first_name(row_number):
    try:
        first_name_col = column_index("first_name")
        if first_name_col == -1:
            return "Column 'first_name' not found"
        
        return employees['rows'][row_number][first_name_col]
    
    except Exception as e:
        print(f"An error ocurred: {e}")
        return -1

print (first_name(0))

########### Task 5 ############################################

def employee_find(employee_id):

    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    
    matches = list(filter(employee_match, employees['rows']))

    return matches

print(employee_find(101))

########### Task 6 ############################################
def employee_find_2(employeed_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employeed_id, employees['rows']))
    return matches

########### Task 7 ############################################

def sort_by_last_name():
    
    last_name_column = column_index("last_name")
    
    employees["rows"].sort(key=lambda row: row[last_name_column])

    return employees["rows"]  

sort_by_last_name()

print(employees)

########### Task 8 ############################################

def employee_dict(row):
    
    headers = employees["fields"]
    
    employee_id_col = column_index("employee_id")
    
    # Create a dictionary excluding the employee_id column
    employee_dict = {headers[i]: row[i] for i in range(len(headers)) if i != employee_id_col}
    
    return employee_dict

# Test: Convert the first row of employees["rows"] into a dictionary and print it
if employees["rows"]:
    employee_sample = employee_dict(employees["rows"][0])
    print(employee_sample)

################ Task 9 ####################################

def all_employees_dict():
   
    
    employee_id_col = column_index("employee_id")
    
    all_employees_dict = {row[employee_id_col]: employee_dict(row) for row in employees["rows"]}
    
    return all_employees_dict

employees_data = all_employees_dict()
print(employees_data)

############# Task 10 #####################################

def get_this_value():
    return os.getenv("THISVALUE")

print(get_this_value())

############ Task 11 #####################################

def set_that_secret(newSecret):
    custom_module.set_secret(newSecret)
    

set_that_secret("test")

print(custom_module.secret)

############ Task 12 #####################################

def read_csv_file(filepath):
    """Helper function to read a CSV file and return a dictionary with fields and rows."""
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            fields = next(reader)  # Read the first row as headers
            rows = [tuple(row) for row in reader]  # Convert each row to a tuple
            return {"fields": fields, "rows": rows}
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        exit(1)

def read_minutes():
    """Reads minutes1.csv and minutes2.csv, returning them as dictionaries."""
    minutes1 = read_csv_file("../csv/minutes1.csv")
    minutes2 = read_csv_file("../csv/minutes2.csv")
    return minutes1, minutes2

# Call the function and store the results in global variables
minutes1, minutes2 = read_minutes()

# Print the results to verify
print("Minutes1:", minutes1)
print("Minutes2:", minutes2)


########### Task 13 ########################################################

def create_minutes_set():
    """Creates a set of unique meeting records by combining minutes1 and minutes2 rows."""
    set1 = set(minutes1["rows"])  # Convert list of tuples to a set
    set2 = set(minutes2["rows"])  # Convert list of tuples to a set
    
    # Combine both sets using union operation
    combined_set = set1 | set2  # Equivalent to set1.union(set2)
    
    return combined_set

# Call the function and store the result in a global variable
minutes_set = create_minutes_set()

# Print the result to verify
print("Minutes Set:", minutes_set)

########## Task 14 ##################################################

def create_minutes_list():
    
    
    # Convert the set to a list
    minutes_list = list(minutes_set)
    
    # Use map() to convert date strings to datetime objects
    minutes_list = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list))
    
    return minutes_list

# Call the function and store the result in the global variable
minutes_list = create_minutes_list()

# Print the resulting minutes_list to check the output
print("Minutes List:", minutes_list)

########### Task 15 ################################################
import csv
from datetime import datetime

def write_sorted_list():
    """Sort the minutes_list and write the sorted data to a CSV file."""
    
    minutes_list.sort(key=lambda x: x[1])  # Sorting by the datetime object
    
    # Use map to convert datetime back to string
    converted_list = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), minutes_list))
    
    # Open a CSV file for writing
    with open('./minutes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the fields as the first row
        writer.writerow(["name", "date"])  
        
        # Write the sorted data rows
        for row in converted_list:
            writer.writerow(row)
    
    # Return the converted list
    return converted_list
