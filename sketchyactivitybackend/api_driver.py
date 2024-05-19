import os
import requests
from dotenv import load_dotenv
import json

load_dotenv('../.env')

class SketchyActivityAPIDriver:
    def __init__(self):
        self.api = "https://sketchyactivity.com/api"
        self.username = os.getenv("SKETCHYACTIVITY_USERNAME")
        self.password = os.getenv("SKETCHYACTIVITY_PASSWORD")
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
        self.headers["Authorization"] = f"Token {self.get_token()}"
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_token(self):
        # url = self.api + "/login/"
        url = self.api + "/obtain-auth-token/"
        response = requests.post(url, data=json.dumps({
            "username": self.username,
            "password": self.password
        }), headers=self.headers)
        if "token" not in response.json():
            raise Exception("Failed to get token")

        return response.json()["token"]

    def get_portfolio(self):
        url = self.api + "/portfolio/"
        response = self.session.get(url)
        return response.json()


if __name__ == "__main__":
    driver = SketchyActivityAPIDriver()
    with open("portfolio.json", "w") as f:
        json.dump(driver.get_portfolio(), f, indent=4)
