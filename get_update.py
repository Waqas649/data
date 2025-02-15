import time
import subprocess

def pull_updates():
    try:
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        if 'Already up to date.' not in result.stdout:
            print("Repository updated.")
        else:
            print("No updates found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        pull_updates()
        time.sleep(10)