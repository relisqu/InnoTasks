import uuid
import logging

from locust import HttpUser, task, between, events


@events.quitting.add_listener
def _(environment, **_):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed: failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed: average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed: 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0


class TestInnoTasks(HttpUser):
    def on_start(self):
        self.user = {"username": str(uuid.uuid4()), "password": "password"}
        self.client.post("/register", json=self.user)
        response = self.client.post("/login", json=self.user)
        self.id = response.json()[0]

    wait_time = between(1, 2)

    @task
    def test_login(self):
        # register a user
        self.client.post("/login", json=self.user)

    @task
    def test_add_task(self):
        # add a task for the user
        self.client.post("/task",
                         json={"user_id": self.id,
                               "task": "task",
                               "task_status": "task_status",
                               "task_priority": "task_priority",
                               "task_due_date": "task_due_date"})

    @task
    def test_get_task(self):
        # get the task added
        self.client.get(f"/tasks/{self.id}")
