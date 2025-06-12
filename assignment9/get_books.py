'''
#------------- Task 1, 2, 3 ------------------

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time

# Initialize the browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# URL to search
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
driver.get(url)

# Wait for the page to fully load
time.sleep(5)

# Get all <li> elements on the page
list_items = driver.find_elements(By.TAG_NAME, "li")
results = []

# Filter only <li> elements that contain search result data
search_results = [li for li in list_items if "cp-search-result-item" in li.get_attribute("class")]

print(f"🔍 Resultados encontrados: {len(search_results)}")

# Loop through each result item
for li in search_results:
    try:
        # Extract the book title
        title_element = li.find_element(By.CLASS_NAME, "title-content")
        title = title_element.text.strip()
    except:
        title = "Título não encontrado"

    try:
        # Extract one or more authors
        authors = li.find_elements(By.CLASS_NAME, "cp-author-link")
        author_names = [a.text.strip() for a in authors]
        authors_str = "; ".join(author_names)
    except:
        authors_str = "Autor não encontrado"

    try:
        # Extract format and year information
        format_div = li.find_element(By.CLASS_NAME, "display-info-primary")
        format_year = format_div.text.strip()
    except:
        format_year = "Formato/Ano não encontrado"

    # Store the data in a dictionary
    book = {
        "Title": title,
        "Author": authors_str,
        "Format-Year": format_year
    }
    # Append the result to the list
    results.append(book)

# Close the browser
driver.quit()

# Print the DataFrame
df = pd.DataFrame(results)
print("\n📘 Livros encontrados:\n")
print(df)

# Optional: Save results to a JSON file
with open("books.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

'''

import os
import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# URL of the search page
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Find all <li> elements on the page
list_items = driver.find_elements(By.TAG_NAME, "li")
search_results = [li for li in list_items if "cp-search-result-item" in li.get_attribute("class")]

print(f"🔍 Number of search results found: {len(search_results)}")

results = []

# Extract data from each result
for li in search_results:
    try:
        title_element = li.find_element(By.CLASS_NAME, "title-content")
        title = title_element.text.strip()
    except:
        title = "Title not found"

    try:
        authors = li.find_elements(By.CLASS_NAME, "cp-author-link")
        author_names = [a.text.strip() for a in authors]
        authors_str = "; ".join(author_names)
    except:
        authors_str = "Author not found"

    try:
        format_div = li.find_element(By.CLASS_NAME, "display-info-primary")
        format_year = format_div.text.strip()
    except:
        format_year = "Format/Year not found"

    book = {
        "Title": title,
        "Author": authors_str,
        "Format-Year": format_year
    }
    results.append(book)

# Close the browser
driver.quit()

# Create a DataFrame and save to CSV in the root directory
df = pd.DataFrame(results)
df.to_csv("get_books.csv", index=False)
print("✅ CSV file saved to: get_books.csv")

# Save JSON output in the root directory
with open("get_books.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("✅ JSON file saved to: get_books.json")