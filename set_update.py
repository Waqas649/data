import os
import time
from datetime import datetime

while True:
    try:
        # Wait for 10 seconds
        time.sleep(10)

        # Get the current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add Data.csv to the staging area
        if os.system("git add Data.csv") != 0:
            raise Exception("Failed to add Data.csv to the staging area")

        # Check if there are changes to commit
        if os.system("git diff --cached --quiet") != 0:
            # Commit with the message "updated at {time}"
            commit_message = f'updated at {current_time}'
            if os.system(f'git commit -m "{commit_message}"') != 0:
                raise Exception("Failed to commit changes")

            # Push the changes to the repository
            if os.system("git push") != 0:
                raise Exception("Failed to push changes to the repository")

            print("Updated at : ", current_time)
    except Exception as e:
        print(f"An error occurred: {e}")