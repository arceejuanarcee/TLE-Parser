import requests
from requests import Session
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
USERNAME = os.getenv("SPACE_TRACK_USERNAME")
PASSWORD = os.getenv("SPACE_TRACK_PASSWORD")

# Log in to Space-Track
def spacetrack_login():
    with Session() as session:
        login_url = 'https://www.space-track.org/ajaxauth/login'
        payload = {
            'identity': USERNAME,
            'password': PASSWORD
        }
        response = session.post(login_url, data=payload)

        if response.status_code == 200:
            print("Login successful.")
            return session
        else:
            print("Login failed.")
            print("Status code:", response.status_code)
            print("Response:", response.text)
            return None

# Test login
if __name__ == "__main__":
    session = spacetrack_login()
