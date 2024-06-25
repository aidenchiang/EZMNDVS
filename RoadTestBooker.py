from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Which service do you want to schedule an appointment for?
# Choose from the following: ["Dealer Services", "Driver Services", "IRP & IFTA Services", "Vehicle Services"]
SERVICE_CATEGORY = "Driver Services"
SERVICE = "Class D Skill Exam - First Time"

# Load the webpage
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://onlineservices.dps.mn.gov/EServices/_/")
driver.maximize_window()

# Find the Service Appointments Link
links = driver.find_elements("xpath", "//a[@href]")

for link in links:
    if "Schedule an Appointment" in link.get_attribute("innerHTML"):
        link.click()
        break

# Click the appropriate service category button.
delay = 5
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'TDR TTDR')][.//span[text()[contains(., '{SERVICE_CATEGORY}')]]]")))
except TimeoutException:
    print("Webpage took too long to load.")

service_links = driver.find_elements("xpath", f"//tr[contains(@class, 'TDR TTDR')][.//span[text()[contains(., '{SERVICE_CATEGORY}')]]]")
service_links[0].click()

# Click the specific service.

import time
time.sleep(1)
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'TDR TTDR')][.//span[text()[contains(., '{SERVICE}')]]]")))
except TimeoutException:
    print("Webpage took too long to load.")

service_links = driver.find_elements("xpath", f"//tr[contains(@class, 'TDR TTDR')][.//span[text()[contains(., '{SERVICE}')]]]")
service_links[0].click()

