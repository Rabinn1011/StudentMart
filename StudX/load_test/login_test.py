from locust import HttpUser, TaskSet, task, between
import random
from bs4 import BeautifulSoup

# Example list of test users with different passwords
TEST_USERS = [
    {"username": f"user{i}", "password": f"pass{i}"} for i in range(1, 1001)
]

class LoginBehavior(TaskSet):
    @task(1)
    def login(self):
        # Fetch the CSRF token
        response = self.client.get("/login/")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", attrs={"name": "csrfmiddlewaretoken"})

        if csrf_token:
            csrf_token = csrf_token.get("value")
        else:
            print("CSRF token not found!")
            return

        # Randomly select a user from the list
        user = random.choice(TEST_USERS)

        # Post login data with CSRF token
        self.client.post("/login/", data={
            "csrfmiddlewaretoken": csrf_token,
            "username": user["username"],
            "password": user["password"]
        }, headers={"Referer": "/login/"})

class WebsiteUser(HttpUser):
    tasks = [LoginBehavior]
    wait_time = between(1, 5)