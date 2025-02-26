import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def driver():
    """Setup Selenium WebDriver with Chrome."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_add_student(driver):
    driver.get("http://localhost:8000/create_student")

    name_input = driver.find_element(By.NAME, "name")  # Adjust selectors as needed
    name_input.send_keys("Test Student")

    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()

    driver.get("http://localhost:8000/list_students")
    assert "Test Student" in driver.page_source
