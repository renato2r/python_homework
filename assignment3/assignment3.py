import pandas as pd
import numpy as np
import csv
import json
import os

######### Task 1 #######################################
myDict = {"Name" : ["Alice","Bob","charlie"],
          "Age" : [25, 30, 35],
          "City" : ["New York", "Los Angeles", "Chicago"]
          } 

task1_data_frame = pd.DataFrame(myDict)
print(task1_data_frame)

# copy of dataframe
task1_with_salary= task1_data_frame.copy()

# add new column
task1_with_salary["Salary"] = [70000, 80000, 90000]
print(task1_with_salary)

# modify and existing column
task1_older = task1_with_salary.copy()
task1_older["Age"] = task1_older["Age"] + 1
print(task1_older)

# Saving dataframe as a csv file

task1_older.to_csv("employees.csv", index=False)

######### Task 2 #######################################

task2_employees = pd.read_csv("employees.csv")
print(task2_employees)

# Read data from a JSON file

with open("additional_employees.json", "r") as file:
    data = json.load(file)  # Converte JSON para um dicionário/lista

json_employees = pd.DataFrame(data)  # Cria o DataFrame corretamente

# Combine DataFrames
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print(more_employees)

######### Task 3 #######################################

# Use the head() method
first_three = more_employees.head(3)
print(first_three)

# Use the tail() method
last_two = more_employees.tail(2)
print(last_two)

# Get the Shape of DataFrame
employee_shape = more_employees.shape
print(employee_shape)

# Use the info() method

more_employees.info()

######### Task 4 #######################################

dirty_data = pd.read_csv("dirty_data.csv")
print(dirty_data)

# Remove any duplicate rows from the DataFrame
clean_data = dirty_data.copy()
clean_data = dirty_data.drop_duplicates()

print(clean_data)

# Convert Age to numeric and handle missing values
#clean_data.loc[:, "Age"] = pd.to_numeric(clean_data["Age"], errors="coerce").fillna(0).astype(float)

#clean_data.loc[:, "Age"] = pd.to_numeric(clean_data["Age"], errors="coerce")
# Corrigir valores não numéricos e garantir que fiquem no intervalo 1-100
clean_data["Age"] = clean_data["Age"].astype(str).str.extract('(\d+)')  # Mantém apenas números
clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors="coerce").fillna(0).astype(int)

# Garantir que valores abaixo de 1 sejam convertidos para um valor adequado (ex: NaN ou média)
clean_data.loc[clean_data["Age"] < 1, "Age"] = np.nan  # Converte valores inválidos para NaN
clean_data["Age"] = clean_data["Age"].fillna(clean_data["Age"].median()).astype(int)  # Substitui NaN pela mediana

print(clean_data)
print(clean_data.dtypes)


# Substituir valores "unknown" e "n/a" por NaN antes da conversão
clean_data["Salary"] = clean_data["Salary"].replace(["unknown", "n/a"], np.nan)

# Converter para numérico, tratando erros com NaN
clean_data["Age"] = pd.to_numeric(clean_data["Age"], errors="coerce")
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors="coerce")

# Preencher valores NaN
clean_data["Age"].fillna(clean_data["Age"].mean(), inplace=True)  # Média para Age
clean_data["Salary"].fillna(clean_data["Salary"].median(), inplace=True)  # Mediana para Salary


print(clean_data)

# Convert Hire Date to datetime
clean_data["Hire Date"] = pd.to_datetime(clean_data["Hire Date"], errors="coerce")
print(clean_data)

# Strip extra whitespace and standardize Name and Department as uppercase
# Remover espaços extras e converter para maiúsculas
clean_data["Name"] = clean_data["Name"].str.strip().str.upper()
clean_data["Department"] = clean_data["Department"].str.strip().str.upper()
print(clean_data)