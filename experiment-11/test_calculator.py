from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)

driver.get("http://localhost:8000")

driver.find_element("id", "firstNumber").send_keys("10")
driver.find_element("id", "secondNumber").send_keys("20")

driver.find_element("id", "addButton").click()

result = driver.find_element("id", "result").text

print("Calculator result:", result)

assert result == "30"

print("Selenium test passed successfully.")

driver.quit()