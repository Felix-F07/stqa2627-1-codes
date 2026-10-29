from locust import HttpUser, task, SequentialTaskSet, between
import random
RESPONSE_TIME_LIMIT_MS = 3000.0
import time


class PetShopWorkflow(SequentialTaskSet):

    @task
    def add_new_pet(self):
        pet_name = f"Fluffy-{random.randint(1, 10000)}"

        self.client.post("/pets", json={
            "name": pet_name,
            "category": "dog"
        })

    @task
    def load_homepage(self):
        start_time = time.time()

        with self.client.get("/", catch_response=True) as response:
            response_time_ms = (time.time() - start_time) * 1000

            if response_time_ms > RESPONSE_TIME_LIMIT_MS:
                response.failure(
                    f"Response time limit ({RESPONSE_TIME_LIMIT_MS}ms) exceeded: {response_time_ms:.0f}ms"
                )

            elif response.status_code != 200:
                response.failure(
                    f"Non-200 status code: {response.status_code}"
                )

            else:
                response.success()

class PetShopUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(0, 0)
    tasks = [PetShopWorkflow]