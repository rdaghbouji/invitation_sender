# LinkedIn Invitation Sender

This project is a Python-based automation script that sends connection invitations on LinkedIn to a list of profiles stored in a CSV file. The script utilizes Selenium WebDriver to navigate LinkedIn profiles and send invitations without notes, using a daily limit to comply with LinkedIn’s invitation restrictions. Processed profiles are saved to avoid sending duplicate invitations and allow the script to resume where it left off.

## Features

- **Automated Connection Invitations**: Automatically sends invitations to a list of LinkedIn profiles.
- **Daily Invitation Limit**: Limits the number of invitations sent each day to stay within LinkedIn's usage policies.
- **Processed Profiles Tracking**: Saves processed profiles to avoid sending duplicate invitations.
- **Resume Capability**: Resumes from the last unprocessed profile in case of interruptions.
- **Uses Firefox Profile**: Loads a Firefox profile to manage cookies and stay logged into LinkedIn.

## Setup

### Prerequisites

1. **Python**: Ensure you have Python installed (version 3.6 or higher).
2. **Selenium**: Install the Selenium library.
   ```bash
   pip install selenium
