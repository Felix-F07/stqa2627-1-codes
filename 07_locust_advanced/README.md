# Part 1: Sequential User Flows

In this exercise, we will use Locust's `SequentialTaskSet` to simulate a realistic, ordered workflow against our Pet Shop application.

## Step 1: Create the sequential workflow

We will create a `SequentialTaskSet` to model a user who performs two actions **in order**:
1. First, they add a new pet to the shop.
2. Second, they view the list of all pets (the "dashboard").

Your Tasks:
1. Create a locust file: `locustfile.py`.
2. Define the `SequentialTaskSet` class.
3. In the class, implement a `@task` method: A `POST` request to add a new pet. Use `self.client.post("/pets")` with the pet data as a json variable.
4. Implement another `@task` method: A `GET` request to get the homepage. Use `self.client.get("/")`.

```py
from locust import HttpUser, task, SequentialTaskSet, between
import random

class PetShopWorkflow(SequentialTaskSet):

    # This task will always run FIRST because the TaskSet is Sequential
    @task
    def add_new_pet(self):
        # Create a unique name for our new pet
        pet_name = f"Fluffy-{random.randint(1, 10000)}"
        
        self.client.post("/pets", json={
            "name": pet_name,
            "category": "dog"
        })

    # This task will always run SECOND
    @task
    def load_homepage(self):
        self.client.get("/")
```

## Step 2: Create the simulated user that executes the TaskSet

Your Tasks:
1. In the same locust file, create a new `HttpUser` class.
2. Set the host to `http://127.0.0.1:5000` and `wait_time` to `between(1, 3)`.
3. Set the tasks variable to a list containing the workflow class.

```py
class PetShopUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 3)
    tasks = [PetShopWorkflow]
```

## Step 3: Execution and Analysis

Your Tasks:
1. Run the flask app.
```
python app.py
```
2. Run Locust from the project's root directory on a **separate terminal**.
```
locust
```
3. Access the Locust web dashboard via web browser (usually `http://localhost:8089`).
4. Start a load test simulating 10 Users with a 2 users per second ramp-up rate.
5. Observe the real-time reports.


# Part 2: Stress Testing

In this part, we will we will simulate an unrealistic, overwhelming mob of users, to perform a **Stress Test**. We will intentionally break the Pet Shop application to find its maximum capacity. You will remove all simulated "thinking time" and apply a massive, rapid load until the server fails. Your objective is to watch this failure happen in real-time and analyze the results in Locust's **Errors** and **Charts** tabs.

## Step 1: Remove wait time

Your tasks:
1. Remove Wait Time: In the `PetShopUser` class, we need to change the `wait_time` from a realistic `between(1, 3)` to zero. This tells the virtual users to execute the workflow as fast as possible, with no "thinking" time between runs.

```py
    wait_time = between(0, 0)
```

## Step 2: Re-run Locust with many more users

Your Tasks:
1. Restart Locust on the project's root directory.
```
locust
```
2. Start a test simulating **200 Users** with a **50 users per second** ramp-up rate.
3. Observe the results and experiment by increasing the number of users and/or ramp-up rate.


# Part 3: Manual Failure

In the previous part, we would have only seen "Failures" when the server crashes with a 500 error. However, this happens very rarely. This happens because the server is "too polite": it doesn't crash, it just queues requests and gets very, very slow. We can see how the response time increases proportionally to the number of requests. But in the real world, a user who has to wait too long for a page to load considers the app broken.

In this part, you will modify your Locust script to enforce a **Service Level Objective (SLO)**. You will tell Locust to **manually fail** any requests that takes longer than 3,000 milliseconds, even if the server returns a 200 OK.

## Step 1: Define Our SLO Constant

Define our "failure" threshold as a global variable in the locustfile. This makes it easy to change later.

```py
RESPONSE_TIME_LIMIT_MS = 3000.0
```

## Step 2: Rewrite Our Task to Check Time

Modify a task (e.g., `load_homepage`) to manually time the request and apply our logic.

```py
import time

    @task
    def load_homepage(self):
        
        # 1. Record the time *before* the request
        start_time = time.time()
        
        # 2. Make the request, but use 'catch_response=True'.
        # This tells Locust we want to decide whether the request is a success or not.
        with self.client.get("/", catch_response=True) as response:
            
            # 3. Calculate the total response time in milliseconds
            response_time_ms = (time.time() - start_time) * 1000
            
            # 4. Implement our custom SLO logic
            if response_time_ms > RESPONSE_TIME_LIMIT_MS:
                # 5. MANUALLY fail the request
                response.failure(f"Response time limit ({RESPONSE_TIME_LIMIT_MS}ms) exceeded: {response_time_ms:.0f}ms")
            
            elif response.status_code != 200:
                # 6. Manually fail on bad status codes
                response.failure(f"Non-200 status code: {response.status_code}")
                
            else:
                # 7. MANUALLY mark it as a success
                response.success()
```

## Step 3: Re-run Locust

Your Tasks:
1. Restart Locust on the project's root directory.
```
locust
```
2. Start a load test with a large number of users and observe the results.
3. If you see your system is still able to handle the stress test, you can increase the number of concurrent users and ramp-up rate.


# Part 4: Scaling the Test with Master/Worker Architecture

So far, we have run Locust on a single machine. This is fine for small tests, but we have a small issue: Our laptop most likely cannot generate enough load to break a truly powerful server. Our locust process will hit 100% CPU long before a real production-grade server does. The tester itself becomes the bottleneck. This is a common occurrence.

In this part, we will solve this by scaling Locust horizontally. We will run Locust in a distributed mode, using its Master/Worker architecture to generate massive-scale load, far beyond what one machine can handle.

We can have 1 Master and hundreds of Workers, allowing us to simulate millions of users by combining the power of many machines. For today, we'll simulate this on our one machine by running all the processes locally.

## Step 1: Run the Master Node

We do not need to change our locustfile. To run a master node, simply run locust with the `--master` flag on a terminal.
```
locust --master
```

## Step 2: Run the Worker Node(s)

Run locust with the `--worker` flag on **separate** terminals.
```
locust --worker
```

## Step 3: Re-run Locust tests

Start a load test simulating **5000 Users** with a **100 users per second** ramp-up rate. Observe how the RPS improves when using more than 1 worker, showing that distributed testing allows us to increase the load-generating capacity of the tester.
