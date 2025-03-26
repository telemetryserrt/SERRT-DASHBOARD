from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import time

# Path to ChromeDriver
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode (no window)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional, but recommended)
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (useful for some environments)
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Initialize WebDriver (Outside the loop for efficiency)
service = ChromeService(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 60)  # Initialize WebDriverWait

def login():
    """Logs into the Orion BMS website."""
    try:
        driver.get("https://connect.orionbms.com/")

        # Wait for login fields
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

        # Enter credentials
        username_field.send_keys("telemetryserrt@gmail.com")
        password_field.send_keys("BoricuaBolt89")

        # Click login button
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()

        # Wait for the dashboard to load
        wait.until(EC.url_contains("/dashboard"))

        # Navigate to the dashboard (if needed)
        driver.get("https://connect.orionbms.com/dashboard")

        return True  # Login successful
    except Exception as e:
        print(f"Login error: {e}")
        return False  # Login failed

def getSOC():
    """Retrieves the SOC value from the dashboard."""
    try:
        # Wait for the <text> element to be visible (SOC value)
        xpath = "//body//div[@id='board-content']//div[@class='gauge-widget-wrapper']//div[@id='gauge-0']//*[name()='svg']//*[name()='text'][1]//*[name()='tspan']"
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

        # Find the element using XPath
        element = driver.find_element(By.XPATH, xpath)

        # Get the inner HTML of the element
        inner_html = element.get_attribute("innerHTML")

        # Print the inner HTML
        print("Inner HTML of the element:", inner_html)
        return inner_html

    except Exception as e:
        print(f"Error getting SOC: {e}")
        return None

def exit():
    driver.quit()

if __name__ == "__main__":
    if login():  # Login only once
        while True:
            soc = getSOC()
            if soc:
                # Do something with the SOC value (e.g., store it, process it)
                print(f"SOC: {soc}")
            time.sleep(5)  # Wait before next scrape (adjust as needed)
    else:
        print("Script terminated due to login failure.")
    driver.quit()  # Quit the driver after the loop