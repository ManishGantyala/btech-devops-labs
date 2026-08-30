from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

options = Options()
options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

driver.get("http://localhost:8082")

driver.find_element("id", "name").send_keys("Test Student")
driver.find_element("id", "email").send_keys("test@example.com")
driver.find_element("id", "phone").send_keys("9876543210")

Select(driver.find_element("id", "department")).select_by_value("cse")
Select(driver.find_element("id", "year")).select_by_value("3")
Select(driver.find_element("id", "event")).select_by_value("web-development")

driver.find_element("css selector", "button[type='submit']").click()

message = driver.find_element("id", "message").text

print("Registration message:", message)

assert message == "Registration successful!"

print("Selenium test passed successfully.")

driver.quit()