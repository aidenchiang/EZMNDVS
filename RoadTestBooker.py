from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import time
from selenium.webdriver.common.action_chains import ActionChains

# Which service do you want to schedule an appointment for?
# Choose from the following: ["Dealer Services", "Driver Services", "IRP & IFTA Services", "Vehicle Services"]
SERVICE_CATEGORY = "Driver Services"
SERVICE = "Class D Skill Exam - First Time"

ID_NUMBER = "XXXX-XXX-XXX-XXX"
DOB = "MM-DD-YYYY"
PHONE_NUMBER = "XXX-XXX-XXXX"
EMAIL = "XXXXXXXX@XXXXX.XXX"

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
delay = 30
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

# Enter proper filtering information to see nearest locations + zip code + filter by available
# Opens filter menu
links = driver.find_elements("xpath", "//a[@href]")

for link in links:
    if "Filter and Sort" in link.get_attribute("innerHTML"):
        link.click()
        break

try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'InputWrapper')][.//span[text()[contains(., 'With Available Appointments')]]]")))
except TimeoutException:
    print("Webpage took too long to load.")

down_button = driver.find_element("xpath", "//a[@href][text()[contains(., 'Scroll for More')]]")
down_button.click()
time.sleep(0.5)

view_available_toggle = driver.find_element("xpath", f"//div[contains(@class, 'InputWrapper')][.//span[text()[contains(., 'With Available Appointments')]]]")
view_available_toggle.find_element(By.CSS_SELECTOR, "input").click()



apply_button = driver.find_element("xpath", "//button[contains(., 'Apply')]")
down_button.click()
time.sleep(0.5)
apply_button.click()

# Refresh page to keep checking for new openings

while True:

    # Insert code to wait until title which location works best is found
    time.sleep(1)

    ok_button = driver.find_elements("xpath", "//button[contains(., 'OK')]")
    if ok_button:
        ok_button[0].click()

    available_locations = driver.find_elements("xpath", "//tr[contains(@class, 'TDR TTDR')]")

    if len(available_locations) == 0:
        time.sleep(5)
        driver.refresh()

    found = False
    for locations in available_locations:
        # This will just click any area thats open, the commented out portion can replace TRUE if you want a specific location
        if True: #"Marsh" in locations.get_attribute("innerHTML"):
            found = True
            
            down_button = driver.find_element("xpath", "//a[@href][text()[contains(., 'Scroll for More')]]")
            down_button.click()
            time.sleep(0.5)

            locations.find_element(By.CSS_SELECTOR, "a").click()
            break

    if found:
        break
    else:
        time.sleep(5)
        driver.refresh()
    

# After we selected location, select the time.
# REPLACE TIME SLEEP WITH SELECT A TIME
time.sleep(3)
times_AM = driver.find_elements("xpath", "//a[@href][.//span[text()[contains(., 'AM')]]]")
times_PM = driver.find_elements("xpath", "//a[@href][.//span[text()[contains(., 'PM')]]]")

# Selects the latest possible time, I hate waking up early.
if len(times_PM) == 0:
    times_AM[-1].click()
else:
    times_PM[-1].click()

next_button = driver.find_element("xpath", "//button[.//span[text()[contains(., 'Next')]]]")
actions = ActionChains(driver)
actions.move_to_element(next_button).click().perform()

# Will constantly click the "OK" button so you don't get ejected for being AFK.
while True:
    ok_button = driver.find_elements("xpath", "//button[contains(., 'OK')]")
    if ok_button:
        ok_button[0].click()

        time.sleep(30)

next_button = driver.find_element("xpath", "//button[.//span[text()[contains(., 'Next')]]]")
next_button.click()


