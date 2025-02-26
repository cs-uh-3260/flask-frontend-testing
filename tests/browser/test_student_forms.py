import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pdb


@pytest.fixture
def driver():
    """Setup Selenium WebDriver with Chrome."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def _get_test_student():
    return {
        "name": "BrowserTestStudentName",
        "email": "browsertest@nyu.edu",
        "seniority": "Senior",
    }


def _add_test_student(driver, student):
    driver.get("http://127.0.0.1:8000/create_student")
    # wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))

    name_field = driver.find_element(By.NAME, "name")
    name_field.send_keys(student["name"])

    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(student["email"])

    seniority_field = driver.find_element(By.NAME, "seniority")
    seniority_dropdown = Select(seniority_field)
    seniority_dropdown.select_by_value(student["seniority"])

    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = Alert(driver)
    alert.accept()


def test_navigate_to_add_student_page(driver):
    driver.get("http://127.0.0.1:8000")

    # assert that there's a link foir add student
    assert "Add Student" in driver.page_source
    add_link = driver.find_element(By.LINK_TEXT, "Add Student")
    add_link.click()

    # wait until we are on the create_Student page
    # assert that we are on the right page by checking the content
    WebDriverWait(driver, 10).until(EC.url_contains("/create_student"))
    assert "Create New Student" in driver.page_source


def test_add_student(driver):
    driver.get("http://127.0.0.1:8000/create_student")

    # wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))

    assert "Create New Student" in driver.page_source

    name_field = driver.find_element(By.NAME, "name")
    name_field.send_keys("TestStudentName")

    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys("test@nyu.edu")

    seniority_field = driver.find_element(By.NAME, "seniority")
    seniority_dropdown = Select(seniority_field)
    seniority_dropdown.select_by_value("Senior")

    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = Alert(driver)
    assert "Student added successfully!" in alert.text
    alert.accept()

    driver.get("http://127.0.0.1:8000/list_students")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'TestStudentName')]")
        )
    )
    assert "TestStudentName" in driver.page_source


def test_navigate_to_delete_student_page(driver):
    driver.get("http://127.0.0.1:8000")

    # assert that there's a link foir add student
    assert "Delete Student" in driver.page_source
    add_link = driver.find_element(By.LINK_TEXT, "Delete Student")
    add_link.click()

    # wait until we are on the create_Student page
    # assert that we are on the right page by checking the content
    WebDriverWait(driver, 10).until(EC.url_contains("/delete_student"))
    assert "Delete Student by Email" in driver.page_source


def test_delete_student(driver):

    # first populate a student to make sure it's there
    # in a real setting, you would have a fixture that resets the DB for every test
    # using different configs etc. I'm just making things simple here

    test_student = _get_test_student()
    _add_test_student(driver, test_student)

    driver.get("http://127.0.0.1:8000/delete_student")

    # wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

    assert "Delete Student by Email" in driver.page_source

    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(test_student["email"])

    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = Alert(driver)
    assert "Student deleted successfully!" in alert.text
    alert.accept()

    driver.get("http://127.0.0.1:8000/list_students")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'TestStudentName')]")
        )
    )
    assert test_student["email"] not in driver.page_source
