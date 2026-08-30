from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


def create_driver():
    options = Options()
    options.add_experimental_option(
        "debuggerAddress",
        "127.0.0.1:9222"
    )
    return webdriver.Chrome(options=options)


def test_valid_registration():
    driver = create_driver()

    driver.get("http://localhost:8081")

    driver.find_element("id", "name").send_keys("Test Student")
    driver.find_element("id", "email").send_keys("test@example.com")
    driver.find_element("id", "phone").send_keys("9876543210")

    Select(driver.find_element("id", "department")).select_by_value("cse")
    Select(driver.find_element("id", "year")).select_by_value("3")
    Select(driver.find_element("id", "event")).select_by_value("web-development")

    driver.find_element("css selector", "button[type='submit']").click()

    message = driver.find_element("id", "message").text

    print("TC01 - Valid registration:", message)

    assert message == "Registration successful!"

    driver.quit()


def test_name_input_filtering():
    driver = create_driver()

    driver.get("http://localhost:8081")

    name = driver.find_element("id", "name")
    name.send_keys("Test123@ Student!")

    actual_value = name.get_attribute("value")

    print("TC02 - Name after filtering:", actual_value)

    assert actual_value == "Test Student"

    driver.quit()


def test_phone_input_filtering():
    driver = create_driver()

    driver.get("http://localhost:8081")

    phone = driver.find_element("id", "phone")
    phone.send_keys("987abc654@321")

    actual_value = phone.get_attribute("value")

    print("TC03 - Phone after filtering:", actual_value)

    assert actual_value == "987654321"

    driver.quit()


def test_required_fields():
    driver = create_driver()

    driver.get("http://localhost:8081")

    driver.find_element("css selector", "button[type='submit']").click()

    message = driver.find_element("id", "message").text

    print("TC04 - Message with empty required fields:", message)

    assert message == ""

    driver.quit()


test_valid_registration()
test_name_input_filtering()
test_phone_input_filtering()
test_required_fields()

print("All Selenium test cases passed successfully.")
