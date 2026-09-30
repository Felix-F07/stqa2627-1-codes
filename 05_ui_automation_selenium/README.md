# Web UI Automation with Selenium

In this exercise, we will implement end-to-end web UI automation by combining Behavior-Driven Development (BDD) via `behave` with `selenium` WebDriver. Our main goal is to test a real web application through its graphical browser interface, driving user actions like filling forms, clicking buttons, asserting on dynamically rendered DOM elements, and configuring scenario hooks to continue test execution even after step assertions fail.

First of all, examine the provided Flask pet shop application in `app.py` and review the feature specification in `features/pets.feature`. You can run the application on localhost and explore the user interface manually before automating it.

```bash
python app.py
```

## Step 0: Make sure dependencies are installed

Ensure `behave`, `selenium`, and `requests` are installed in your virtual environment. Uncomment them in `requirements.txt` if needed, then run pip:

```bash
pip install -r requirements.txt
```

## Step 1: Create the Behave Environment Hooks

The `environment.py` file is responsible for setting up and tearing down the test environment. In this step, we will implement the `behave` hooks to start the Flask application and initialize the Selenium WebDriver.

### Step 1.1: Base URL and Initial Hook

Open `features/environment.py`. Define the `BASE_URL` and initialize the basic `before_all` hook. The URL is where the Flask app will be running.

Your Tasks:
- Import `getenv` from the `os` module.
- Read `BASE_URL` from the environment or default to `'http://127.0.0.1:5000'`.
- In `before_all(context)`, store `context.base_url = BASE_URL`.

### Step 1.2: Launch the Flask App in the Background

We need our Flask application running continuously in the background using a separate thread during test execution.

Your Tasks:
- Import `threading` and `time`.
- Import `app` as `flask_app` from `app.py`.
- In `before_all(context)`, start the Flask app inside a background daemon thread:
  ```python
  context.server_thread = threading.Thread(
      target=flask_app.run,
      kwargs={'host': '0.0.0.0', 'port': 5000}
  )
  context.server_thread.daemon = True
  context.server_thread.start()
  ```
- Add `time.sleep(5)` to allow the server time to fully initialize.

### Step 1.3: Initialize the Headless WebDriver

Configure Selenium Chrome WebDriver to run headlessly.

Your Tasks:
- Import `webdriver` from `selenium`.
- Define `WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))` and assign it to `context.wait_seconds` inside `before_all`.
- Instantiate Chrome with `--no-sandbox` and `--headless` flags:
  ```python
  options = webdriver.ChromeOptions()
  options.add_argument("--no-sandbox")
  options.add_argument("--headless")
  context.driver = webdriver.Chrome(options=options)
  ```

### Step 1.4: Reset Database and Shutdown Hooks

Ensure the database starts in a known state and resources are cleanly terminated afterward.

Your Tasks:
- Import `requests`.
- At the end of `before_all(context)`, make a `POST` request to `f"{context.base_url}/pets/reset"` to clean the database before tests begin.
- Implement the `after_all(context)` hook to quit the browser via `context.driver.quit()` and send a `GET` request to `f"{context.base_url}/shutdown"` to stop the background server thread.

## Step 2: Implement Step Definitions for Test Fixtures

We will create `features/steps/web_steps.py` and implement the data-loading step definition that seeds our database from the Gherkin `Background` table.

Your Tasks:
1. Create a new file named `features/steps/web_steps.py`.
2. Import the `@given` decorator from `behave` and the `requests` library.
3. Implement the `@given('the following pets')` step definition:
   - Reset the database by sending a `POST` request to `f"{context.base_url}/pets/reset"`.
   - Iterate over `context.table` to parse each pet record (`name`, `category`, `available`, `gender`, `birthday`).
   - Send a `POST` request with JSON payload to `f"{context.base_url}/pets"` for each pet and assert that the HTTP status code is `201`.

## Step 3: Implement UI Interaction Steps

We will implement the step definitions that use Selenium WebDriver to interact with form controls and buttons.

Your Tasks:
1. In `features/steps/web_steps.py`, import `By`, `WebDriverWait`, and `expected_conditions` from `selenium`.
2. Define the prefix constant `ID_PREFIX = 'pet_'` for form input IDs.
3. Implement `@given('I am on the "Home Page"')` to navigate the browser to `context.base_url` using `context.driver.get()`.
4. Implement `@when('I set the "{element_name}" to "{text_string}"')`:
   - Compute the target input ID by converting `element_name` to lowercase, replacing spaces with underscores, and prepending `ID_PREFIX`.
   - Locate the input field using `context.driver.find_element(By.ID, element_id)`.
   - Clear any existing value using `.clear()` and type the new value using `.send_keys(text_string)`.
5. Implement `@when('I click the "{button}" button')`:
   - Compute the button ID by lowercasing the button name and appending `'-btn'` (e.g., `'search-btn'`).
   - Locate and click the button element.

## Step 4: Implement Explicit Wait Assertions

We will implement the `@then` step definitions to assert UI updates using explicit waits, ensuring our tests do not fail due to dynamic asynchronous rendering.

Your Tasks:
1. Implement `@then('I should see the message "{message}"')`:
   - Use `WebDriverWait(context.driver, context.wait_seconds).until(...)` with `expected_conditions.text_to_be_present_in_element` targeting element ID `'flash_message'`.
   - Assert that the condition evaluated to `True`.
2. Implement `@then('I should see "{name}" in the results')`:
   - Use `WebDriverWait` with `expected_conditions.text_to_be_present_in_element` targeting element ID `'search_results'`.
   - Assert that the target pet name is present.
3. Implement `@then('I should not see "{name}" in the results')`:
   - Locate the `'search_results'` element using `context.driver.find_element(By.ID, 'search_results')`.
   - Assert that `name not in element.text`.

## Step 5: Run the End-to-End Test Suite

We will execute `behave` to run our automated UI test suite against the pet shop application.

Your Tasks:
1. Open your terminal at the project root and execute `behave`:
   ```bash
   behave
   ```
2. Confirm that the browser launches headlessly, seeds the database, performs the search interactions, and passes all scenarios.

## Step 6: Observe Default Failure Behavior

We will observe how Behave behaves by default when an assertion fails midway through a scenario.

Your Tasks:
1. In your feature file, temporarily modify the existing scenario to expect a non-existent pet name or message. For example, you can modify the name "Fido" in the Gherkin statement 'And I should see "Fido" in the results' into a different name, so that the statement will fail.
2. Run `behave` in your terminal:
   ```bash
   behave
   ```
3. Notice that the failing step halts the scenario immediately, and all subsequent steps are marked as skipped (`None`).

## Step 7: Configure Continuing Scenarios After Failure

We will configure Behave to continue evaluating subsequent steps in a scenario even after an intermediate step assertion fails.

Your Tasks:
1. Open your `.feature` file and decorate the scenario with the `@continue_after_failed_step` tag right above the `Scenario:` line:
   ```gherkin
   @continue_after_failed_step
   Scenario: Search for dogs
   ```
2. Open `features/environment.py` and implement the `before_scenario(context, scenario)` hook:
   - Check if `'continue_after_failed_step'` is present in `scenario.effective_tags`.
   - If present, set `scenario.continue_after_failed_step = True`.
3. Re-run `behave`:
   ```bash
   behave
   ```
4. Confirm that subsequent steps in the tagged scenario continue executing to completion despite the earlier failure.
