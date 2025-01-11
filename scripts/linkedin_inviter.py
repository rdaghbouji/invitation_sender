import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Load configuration from config.json
with open("../config/config.json", 'r') as f:
    config = json.load(f)

# Load the contacts data from CSV
data = pd.read_csv("../data/contacts.csv", encoding='ISO-8859-1')

# Load processed profiles if the file exists
processed_file = "../data/processed_profiles.csv"
if os.path.exists(processed_file):
    processed_profiles = pd.read_csv(processed_file)["profile_url"].tolist()
else:
    processed_profiles = []

# Filter data to exclude already processed profiles
data = data[~data["favoriteUrl"].isin(processed_profiles)]

# Define a daily invitation limit
DAILY_LIMIT = 10  # Set the maximum number of invitations per day
invitations_sent_today = 0  # Counter to keep track of invitations sent

# Set up Firefox options with the profile path
options = Options()
options.set_preference('profile', config["firefox_profile_path"])

# Initialize the Firefox WebDriver with options
driver = webdriver.Firefox(options=options)

# Open LinkedIn and log in
driver.get("https://www.linkedin.com/")
time.sleep(3)

# Load cookies from JSON file and add them to the driver
with open("../config/linkedin_cookies.json", "r") as cookiesfile:
    cookies = json.load(cookiesfile)
    for cookie in cookies:
        cookie = {key: cookie[key] for key in cookie if key in ["name", "value", "domain", "path", "expiry", "secure"]}
        driver.add_cookie(cookie)

# Refresh to confirm login
driver.refresh()
time.sleep(3)

# Function to send an invitation
def send_invitation(profile_url):
    global invitations_sent_today
    
    driver.get(profile_url)
    time.sleep(2)
    
    try:
        # Click the 'More' button
        more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[7]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[1]/div[2]/div[3]/div[1]/div[2]/button[1]/span[1]"))
        )
        more_button.click()
        time.sleep(2)

        # Click the 'Connect' button
        connect_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[7]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[3]/div[1]/span[1]"))
        )
        connect_button.click()
        print("Clicked the 'Connect' button.")
        
        # Click 'Send without a note' button
        send_without_note_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[4]/div[1]/div[1]/div[3]/button[2]/span[1]"))
        )
        send_without_note_button.click()
        print("Sent invitation without note")
        
        # Save the processed profile
        save_processed_profile(profile_url)
        
        # Increment the counter
        invitations_sent_today += 1

    except Exception as e:
        print("Could not send invitation:", e)

# Function to save processed profile URL
def save_processed_profile(profile_url):
    with open(processed_file, "a") as file:
        file.write(f"{profile_url}\n")
    print(f"Saved processed profile: {profile_url}")

# Iterate over each contact and send an invitation until the daily limit is reached
for index, row in data.iterrows():
    if invitations_sent_today >= DAILY_LIMIT:
        print(f"Reached daily limit of {DAILY_LIMIT} invitations.")
        break
    
    profile_url = row['favoriteUrl']
    print(f"Processing profile: {profile_url}")
    send_invitation(profile_url)

# Close the browser when done
driver.quit()
