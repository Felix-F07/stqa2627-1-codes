# User Acceptance Testing

## Part 1: Traditional UAT

In this first part of the exercise, we will not be developers or technical testers. Our role is that of a Product Owner or Business Analyst. The development team has just delivered the "Pet shop CRUD & Search" feature and claims it's "finished." Our job is to perform User Acceptance Testing (UAT).

Our goal is Validation ("Did they build the right thing?") not Verification ("Did the code run without errors?"). Our final "Sign-Off" will decide if this feature is good enough to release to customers.

We have the following assets:
1. `app.py` and `index.html`: The "buggy" Python server and UI from the dev team.
2. `UAT_Spreadsheet.xlsx`: Our UAT spreadsheet. This is our most important tool.

### Step 1: Creating the Test Cases

The dev team is technical; we are business-focused. Our test cases must be a "contract" that translates the business rules into a testable plan.

The `UAT_Spreadsheet.xlsx` spreadsheet is incomplete. It's our job to finish it.
1. Open `UAT_Spreadsheet.xlsx`.
2. Go to the "Acceptance Criteria" tab. Read all 5 ACs to understand the business requirements.
3. Go to the "Test Cases" tab. We will see `UAT-001` is already written for us as an example.
4. The task: Write the test cases for `UAT-002`, `UAT-003`, `UAT-004`, and `UAT-005`.
5. Fill in these columns for each new test case:
   - AC: Link it to the requirement (e.g., AC-2).
   - Test Scenario: A short description (e.g., "Validate partial update").
   - Test Steps: Simple, non-technical steps a user would take in the browser (e.g., "1. Fill in ID. 2. Fill in Name. 3. Click Update.").
   - Expected Result: The business outcome we expect, based only on the Acceptance Criteria.

### Step 2: Test the Application

1. Run the backend server on localhost in the terminal, and open the interface in the browser.
2. Execute the test cases:
   - Go to the "Test Cases" tab in the spreadsheet.
   - Start with `UAT-001`. Follow the `Test Steps` exactly as written.
   - Observe what actually happens in the browser.
   - In the `Actual Result` column, write down what we saw.
   - In the `Status (Pass/Fail)` column, mark Pass or Fail.
3. Repeat this process for every test case (UAT-002 through UAT-005).

As a note, the `pets` are stored in memory. If we need to "reset" the database between tests, simply stop and restart the `app.py` server.

### Step 3: Log the Defects

1. For every test case we marked as "Fail", go to the "Defect Log" tab.
2. Create a new entry for the bug.
3. Fill in the details:
   - Test ID: Which test failed? (e.g., `UAT-003`)
   - Defect Description: Describe the problem (e.g., "The app crashes when I try to delete a pet.")
   - Expected Result: (e.g., "The pet should be deleted.")
   - Actual Result: (e.g., "The app showed 'Failed to delete pet.'")
   - Severity: Is this a High (show-stopper), Medium (bad, but app works), or Low (e.g., typo) bug?

## Part 2: UAT with Behave

In this second part of the exercise, we will automate our entire UAT Test Plan. You can use the traditional UAT scenarios you already created from Part 1. Our goal is to convert them into a "living document" that automatically runs our tests in a real browser.

### Step 1: Create the Directory Structure

Create the default directory structure for `behave`:
```
/08_UAT/
  |-- app.py
  |-- templates/
      |-- index.html
  |-- UAT_Spreadsheet.xlsx
  |-- README.md
  |-- features/
      |-- environment.py
      |-- steps/
```

### Step 2: Write the Feature File

This is our new, automated UAT plan. We will translate all 5 test cases from our spreadsheet into Gherkin scenarios.
1. Inside the `features/` folder, create a new file named `pet_shop.feature`.
2. Translate each test case from the spreadsheet into one Gherkin scenario in the feature file.

### Step 3: Prepare the Testing Environment

In this part we will prepare the hooks necessary for running the tests. Initialize the Selenium Chrome WebDriver.

### Step 4: Write the Python Steps

In this part, we will write the Python and Selenium code that `behave` will use to execute our Gherkin steps.

1. Inside the `features/steps/` folder, create a new file named `pet_shop_steps.py`.
2. Create all the necessary steps for the scenarios.

### Step 5: Run the Tests

Run `behave` and observe the results.
