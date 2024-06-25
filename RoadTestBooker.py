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

ID_NUMBER = "W000-083-449-500"
DOB = "02-22-2005"

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
delay = 10
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'TDR TTDR')][.//span[text()[contains(., '{SERVICE_CATEGORY}')]]]")))
except TimeoutException:
    print("Webpage took too long to load.")

service_links = driver.find_elements("xpath", f"//tr[contains(@class, 'TDR TTDR')][.//span[text()[contains(., '{SERVICE_CATEGORY}')]]]")
service_links[0].click()

# Click the specific service.
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'TDR TTDR')][.//span[text()[contains(., '{SERVICE}')]]]")))
except TimeoutException:
    print("Webpage took too long to load.")

service_links = driver.find_elements("xpath", f"//tr[contains(@class, 'TDR TTDR')][.//span[text()[contains(., '{SERVICE}')]]]")
service_links[0].click()

# Enters information for Driver's License ID Number and Date of Birth + Terms & Conditions Certification
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, f"//tr[contains(@class, 'Visible')][.//span[text()[contains(., 'ID Number')]]]")))
except TimeoutException:
    print("Webpage took too long to load.")

inputs = driver.find_elements("xpath", f"//tr[contains(@class, 'Visible')][.//input]")

for input in inputs:
    if "ID Number" in input.text:
        print("ENTERING ID")
        entry_field = input.find_element(By.CSS_SELECTOR, "input")
        entry_field.send_keys(ID_NUMBER)

    if "Date Of Birth" in input.text:
        print("ENTERING DOB")
        entry_field = input.find_element(By.CSS_SELECTOR, "input")
        entry_field.send_keys(DOB)

    if "I certify" in input.text:
        entry_field = input.find_element(By.CSS_SELECTOR, "input")
        entry_field.click()

next_button = driver.find_element("xpath", f"//button[.//span[text()[contains(., 'Next')]]]")
next_button.click()

# Clicks the OK button agreeing to a $20 fine if cancelling within 1 day of the appointment.
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, f"//button[text()[contains(., 'OK')]]")))
except TimeoutException:
    print("Webpage took too long to load.")

ok_button = driver.find_element("xpath", f"//button[text()[contains(., 'OK')]]")
ok_button.click()

