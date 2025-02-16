import requests
import time
import os
from datetime import datetime

RETRIES = 5
DOWNLOAD_INTERVAL = 5
GIT_INTERVAL = 10

def login(session, url, data):
    try:
        response = session.post(url, data=data)
        if "dashboard" in response.url or response.status_code == 200:
            print("Login successful!")
            return True
        else:
            print("Login failed. Check your credentials.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Login request failed: {e}")
        return False

def download_file(session, url, filename):
    for i in range(RETRIES):
        try:
            response = session.get(url)
            if response.status_code == 200:
                with open(filename, "wb") as file:
                    file.write(response.content)
                print("File downloaded successfully!")
                return True
            else:
                print(f"Failed to download file. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < RETRIES - 1:
                time.sleep(2 ** i)
            else:
                print("Max retries reached. Exiting.")
                return False
    return False

def git_operations(filename):
    try:
        time.sleep(GIT_INTERVAL)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if os.system(f"git add {filename}") != 0:
            raise Exception("Failed to add file to the staging area")
        if os.system("git diff --cached --quiet") != 0:
            commit_message = f'updated at {current_time}'
            if os.system(f'git commit -m "{commit_message}"') != 0:
                raise Exception("Failed to commit changes")
            if os.system("git push") != 0:
                raise Exception("Failed to push changes to the repository")
            print("Updated at:", current_time)
    except Exception as e:
        print(f"An error occurred during git operations: {e}")

def main(login_url, export_url, login_data):
    session = requests.Session()
    if login(session, login_url, login_data):
        while True:
            if download_file(session, export_url, "Data.csv"):
                git_operations("Data.csv")
            time.sleep(DOWNLOAD_INTERVAL)

if __name__ == "__main__":
    LOGIN_URL = "http://localhost/runcoco/login.php"
    EXPORT_URL = "http://localhost/runcoco/form1/export_result_lap.php"
    LOGIN_DATA = {
        "txtEmailaddress": "runcoco@gmail.com",
        "txtPassword": "123",
        "cboEvent": "10",
        "btnLogin2": "Sign in"
    }
    main(LOGIN_URL, EXPORT_URL, LOGIN_DATA)
