from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://owasp.org/www-project-top-ten/")
time.sleep(5)  # Wait for the page to load

# Find the list items containing the Top 10 risks
li_elements = driver.find_elements(By.XPATH, '//li[a/strong]')

results = []
for li in li_elements:
    try:
        link_element = li.find_element(By.TAG_NAME, 'a')
        title_element = link_element.find_element(By.TAG_NAME, 'strong')
        title = title_element.text.strip()
        link = link_element.get_attribute('href').strip()
        if title and link:
            results.append({'Title': title, 'Link': link})
    except Exception as e:
        print("Error parsing an item:", e)

driver.quit()

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("owasp_top_10.csv", index=False)

# Print preview
print(df.head())
