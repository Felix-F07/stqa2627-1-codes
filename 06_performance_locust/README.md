# Introducing Locust: Testing Transactional Capacity

In this exercise, we will implement performance testing using `Locust`. Our main goal is to prove the server's ability to process transactions under simulated load.

First of all, examine the provided hit counter app. Run the app and open it via browser if necessary.

## Step 1: Writing the Virtual User Script (Locustfile)

We will create a `locustfile.py` that defines key user behaviors.

Your Tasks:
1. Create a new file named `locustfile.py`.
2. Define the `HttpUser` class and set the host to the application's URL.
3. Implement a `@task` method: A simple `GET` request to get the homepage `/`. Use `self.client.get("/")` for loading the page.
4. Make sure to use `127.0.0.1` as the host instead of `localhost`, to avoid additional latency due to IPv6 settings. Be advised that doing a performance test on localhost is **only for learning purposes**. Actual performance tests are done on production environments.

## Step 2: Execution and Analysis

We will run the test runner and then configure a simulation to observe the app's performance.

Your Tasks:
1. Run the flask app.
   ```
   python app.py
   ```
2. Run Locust from the project's root directory on a **separate terminal**.
   ```
   locust -f locustfile.py
   ```
3. Access the Locust web dashboard via web browser (usually `http://localhost:8089`).
4. Start a load test simulating 50 Users with a 5 users per second ramp-up rate.
5. Observe the real-time reports.

## Step 3: Add another task

We will add a new task as a simulated user action: clicking the button to increase the counter. We will give this primary transactional action a higher weight to ensure it is tested more frequently than the simple homepage load request.

Your tasks:
1. Implement another `@task` method: The transactional `POST` request to `/hit`. Use `self.client.post("/hit")` to simulate the button click.
2. Assign a weight of 3 to the `/hit` task and a weight of 1 to the `/` task.
3. Repeat step 2 and observe the results, especially the throughput difference between the `/` and `/hit` tasks.

## Step 4: Add wait time

We will add wait time to simulate the thinking time done by users between tasks.

Your tasks:
1. Add `between` to the imports.
2. Add a variable wait_time in the class and assign it with `between(3, 5)`.
3. Repeat step 2 and observe the results, especially the decrease of throughput compared to previous tests.
