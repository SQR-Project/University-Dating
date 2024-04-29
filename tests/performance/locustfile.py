from locust import HttpUser, task, between

EMAIL = "test@innopolis.university"
PASSWORD = "test123"


class WebsiteUser(HttpUser):
    wait_time = between(0.3, 0.5)

    @task(1)
    def fetch_profile_workflow(self):
        self.create_profile()
        self.delete_profile()

    def create_profile(self):
        self.client.post(
            "/profile/create",
            json={
                "name": "test",
                "surname": "testovich",
                "age": 20,
                "primary_interest": "programming"
            })

    def delete_profile(self):
        self.client.delete("/profile/")

    @task(1)
    def fetch_get_all_profiles(self):
        self.client.get("/profile/all")

    @task(1)
    def fetch_route_healthz(self):
        self.client.get("/status/healthz")

    def on_start(self):
        self.client.post(
            "/auth/login",
            json={
                "email": EMAIL,
                "password": PASSWORD
            })
