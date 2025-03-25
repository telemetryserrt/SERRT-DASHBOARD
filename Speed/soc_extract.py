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

# Start Chrome WebDriver
service = ChromeService(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def getSOC():
    try:
        # Open the BMS login page
        driver.get("https://connect.orionbms.com/")
            
        # Wait for login fields
        wait = WebDriverWait(driver, 60)  # Wait for the page to load
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

        # Navigate to the dashboard
        driver.get("https://connect.orionbms.com/dashboard")

        # Add a small wait for the page to fully load
        driver.implicitly_wait(5)  # Implicit wait for 5 seconds

        # Debugging: Check if the page loaded and contains an expected element
        print("Page title:", driver.title)  # Print the title to confirm the page is loaded

        # Wait for the <text> element to be visible (SOC value)
        xpath="//body//div[@id='board-content']//div[@class='gauge-widget-wrapper']//div[@id='gauge-0']//*[name()='svg']//*[name()='text'][1]//*[name()='tspan']"
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, xpath)
        ))

            # Define the XPath
        # xpath = "//body//div[@id='board-content']//div[@class='gauge-widget-wrapper']//div[@id='gauge-0']//*[name()='svg']//*[name()='text'][1]//*[name()='tspan']"

        # Find the element using XPath
        element = driver.find_element(By.XPATH, xpath)

        # Get the inner HTML of the element
        inner_html = element.get_attribute("innerHTML")

        # Print the inner HTML
        print("Inner HTML of the element:", inner_html)
        return inner_html

    except Exception as e:

        print(e)

if __name__ == "__main__":
    getSOC()