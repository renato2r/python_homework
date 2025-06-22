# list-comprehensions.py

import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("../csv/employees.csv")

# List comprehension to create full names
full_names = [row["first_name"] + " " + row["last_name"] for _, row in df.iterrows()]
print("All employee names:")
print(full_names)

# List comprehension to filter names containing the letter "e"
names_with_e = [name for name in full_names if "e" in name.lower()]
print("\nNames containing the letter 'e':")
print(names_with_e)
