### Solution for Step 1

```python
from os import getenv
import time
import threading
import requests
from selenium import webdriver
from app import app as flask_app

BASE_URL = getenv('BASE_URL', 'http://127.0.0.1:5000')
WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))

def before_all(context):
    """ Executed once before all tests """
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS

    # 1.2: Start Flask app in background thread
    context.server_thread = threading.Thread(
        target=flask_app.run,
        kwargs={'host': '0.0.0.0', 'port': 5000}
    )
    context.server_thread.daemon = True
    context.server_thread.start()
    time.sleep(5)

    # 1.3: Initialize headless Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=options)

    # 1.4: Reset database
    requests.post(f"{context.base_url}/pets/reset")

def after_all(context):
    """ Executed after all tests """
    context.driver.quit()
    requests.get(f"{context.base_url}/shutdown")
```

### Solution for Step 2

```python
import requests
from behave import given, when, then

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
        response = requests.post(f"{context.base_url}/pets", json=result)
        assert response.status_code == 201

```

### Solution for Step 3

```python
from selenium.webdriver.common.by import By

ID_PREFIX = 'pet_'

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
```

### Solution for Step 4

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert found

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    assert found

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element(By.ID, 'search_results')
    assert name not in element.text
```

### Solution for Step 7

```python
def before_scenario(context, scenario):
    """Enable continuing execution after step failure if tagged."""
    if "continue_after_failed_step" in scenario.effective_tags:
        scenario.continue_after_failed_step = True
```
