### Step 1 solution

```py
from locust import HttpUser, task

class HitCounterUser(HttpUser):
    """
    Simulates a user interacting with the Hit Counter app.
    """
    host = "http://127.0.0.1:5000"
    
    @task
    def load_homepage(self):
        self.client.get("/")
```

### Step 3 solution

```py
    @task(3)
    def post_hit(self):
        self.client.post("/hit")

    @task(1)
    def load_homepage(self):
        self.client.get("/")
```

### Step 4 solution

```py
from locust import between

    wait_time = between(3, 5)
```
