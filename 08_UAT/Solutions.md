Please note that the solutions for this exercise are merely examples. There may be many different correct solutions.

## Part 1

### Example solution for step 1

To be written in the Spreadsheet:
```
Test ID: UAT-002
AC: AC-2
Test Scenario: Validate pet update
Test Steps:
1. Open app
2. Create "Buddy" with category dog.
3. In form, type ID: 1 and Name: Buddy Jr. (Leave all other fields blank).
4. Click Update.
5. Click List All Pets.
Expected Result: The name of "Buddy" is updated into "Buddy Jr."

Test ID: UAT-003
AC: AC-3
Test Scenario: Validate pet delete
Test Steps:
1. Open app.
2. Create a new pet (e.g. ""Buddy"")
3. Click Create.
4. In the ID field, fill in 1 (the ID of ""Buddy"").
5. Click Delete.
6. Click List All Pets.
Expected Result: "Buddy" does not appear in the list.

Test ID: UAT-004
AC: AC-4
Test Scenario: Search by name
Test Steps:
1. Open app.
2. Create a new pet (e.g. ""Buddy"")
3. Click Create.
4. Create a new pet (e.g. ""Fido"")
5. Click Create.
6. In the Name field, fill in ""Fido"".
7. Click Search.
Expected Result: "Fido" appears in the list, but "Buddy" does not appear in the list.

Test ID: UAT-005
AC: AC-5
Test Scenario: Search by category is case-insensitive
Test Steps:
1. Open app.
2. Create a new pet (e.g. Name: ""Buddy"", category: ""Dog"")
3. Click Create.
4. Create a new pet (e.g. Name: ""Neko"", category: ""Cat"")
5. Click Create.
6. In the Category field, fill in ""dog"" (with a small ""d"").
7. Click Search.
Expected Result: "Buddy" appears in the list, but "Neko" does not appear in the list.
```

## Part 2

### Example solution for step 2

```Gherkin
Feature: Pet CRUD & Search
  As a pet shop application user
  I want to be able to manage the pets in my pet shop using the application
  So that I can keep track of the pets in my pet shop

  Background:
    Given I am in the home page
    And the pet list is empty

  Scenario: Validate pet creation
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    Then the pet list should show "Buddy" with the correct details: "dog", "MALE", "2024-01-01"

  Scenario: Validate pet update
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    And I update pet ID "1" with only a new name "Buddy Jr."
    Then the pet list should show "Buddy Jr." with the correct details: "dog", "MALE", "2024-01-01"

  Scenario: Validate pet delete
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    And I delete pet ID "1"
    Then the pet list should not show "Buddy"

  Scenario: Search by name
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    And I create a pet with name "Fido", category "dog", gender "MALE", birthday "2025-06-01"
    When I search for the name "Fido"
    Then the pet list should show "Fido"
    And the pet list should not show "Buddy"

  Scenario: Search by category is case-insensitive
    When I create a pet with name "Buddy", category "dog", gender "MALE", birthday "2024-01-01"
    And I create a pet with name "Neko", category "cat", gender "FEMALE", birthday "2025-03-15"
    When I search for the category "Cat"
    Then the pet list should show "Neko"
    And the pet list should not show "Buddy"
```

### Example solution for step 3

```py
from os import getenv
from selenium import webdriver
import requests

BASE_URL = getenv('BASE_URL', 'http://127.0.0.1:5000')
WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))

def before_all(context):
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS

    # Instantiate the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=options)

    requests.post(f"{BASE_URL}/pets/reset")

def after_all(context):
    context.driver.quit()
```

### Example solution for step 4

```py
import requests
from behave import given, when, then
from selenium.webdriver.common.by import By
import time

@given('I am in the home page')
def step_impl(context):
    context.driver.get(context.base_url)

@given('the pet list is empty')
def step_impl(context):
    requests.post(f"{context.base_url}/pets/reset")

def fill_pet_form(context, name="", category="", gender=None, birthday=None, available=True):
    if name:
        context.driver.find_element(By.ID, "pet_name").send_keys(name)
    if category:
        context.driver.find_element(By.ID, "pet_category").send_keys(category)
    if gender:
        context.driver.find_element(By.ID, "pet_gender").send_keys(gender)
    if birthday:
        date_element = context.driver.find_element(By.ID, "pet_birthday")
        context.driver.execute_script(
            "arguments[0].value = arguments[1];", 
            date_element, 
            birthday
        )
    checked = context.driver.find_element(By.ID, "pet_available").is_selected()
    if available != checked:
        context.driver.find_element(By.ID, "pet_available").click()

def create_pet(context, name, category, gender=None, birthday=None, available=True):
    fill_pet_form(context, name, category, gender, birthday, available)
    context.driver.find_element(By.ID, "create-btn").click()
    time.sleep(0.5)

@when('I create a pet with name "{pet_name}", category "{pet_category}", gender "{pet_gender}", birthday "{pet_birthday}"')
def step_impl(context, pet_name, pet_category, pet_gender, pet_birthday):
    create_pet(context, pet_name, pet_category, pet_gender, pet_birthday, available=True)

@then('the pet list should show "{pet_name}" with the correct details: "{pet_category}", "{pet_gender}", "{pet_birthday}"')
def step_impl(context, pet_name, pet_category, pet_gender, pet_birthday):
    results_text = context.driver.find_element(By.ID, "search_results").text
    print(results_text)
    print(pet_name, pet_category, pet_gender, pet_birthday)
    assert pet_name in results_text, "Name problem"
    assert pet_category in results_text, "Category problem"
    assert pet_gender in results_text, "Gender problem"
    assert pet_birthday in results_text, "Birthday problem"

@when('I update pet ID "{pet_id}" with only a new name "{pet_name}"')
def step_impl(context, pet_id, pet_name):
    context.driver.find_element(By.ID, "pet_id").send_keys(pet_id)
    context.driver.find_element(By.ID, "pet_name").send_keys(pet_name)
    context.driver.find_element(By.ID, "update-btn").click()
    time.sleep(0.5)

@when('I delete pet ID "{pet_id}"')
def step_impl(context, pet_id):
    context.driver.find_element(By.ID, "pet_id").send_keys(pet_id)
    context.driver.find_element(By.ID, "delete-btn").click()
    time.sleep(0.5)

@then('the pet list should not show "{pet_name}"')
def step_impl(context, pet_name):
    results_text = context.driver.find_element(By.ID, "search_results").text
    assert pet_name not in results_text

@when('I search for the name "{pet_name}"')
def step_impl(context, pet_name):
    context.driver.find_element(By.ID, "pet_name").send_keys(pet_name)
    context.driver.find_element(By.ID, "search-btn").click()
    time.sleep(0.5)

@then('the pet list should show "{pet_name}"')
def step_impl(context, pet_name):
    results_text = context.driver.find_element(By.ID, "search_results").text
    assert pet_name in results_text

@when('I search for the category "{pet_category}"')
def step_impl(context, pet_category):
    context.driver.find_element(By.ID, "pet_category").send_keys(pet_category)
    context.driver.find_element(By.ID, "search-btn").click()
    time.sleep(0.5)
```
