"""
Web Steps
Steps file for web interactions with Selenium
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
ID_PREFIX = 'pet_'
@given('the following pets')
def step_impl(context):
    """Refresh pets in database from feature table"""
    requests.post(f"{context.base_url}/pets/reset")

    for row in context.table:
        result = {
            "name": row['name'],
            "category": row['category'],
            "available": row['available'] in ['True', 'true', '1'],
            "gender": row['gender'],
            "birthday": row['birthday']
        }

        response = requests.post(
            f"{context.base_url}/pets",
            json=result
        )
        assert response.status_code == 201

@given('I am on the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I click the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert found

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(
        context.driver,
        context.wait_seconds
    ).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    assert found

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element(
        By.ID, 'search_results'
    )
    assert name not in element.text