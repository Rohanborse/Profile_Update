import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
RESUME_PATH = "C:\\Users\\rohan\\Downloads\\Rohan_Borse.pdf"

SENDER_EMAIL = "borserohan5308@gmail.com"  # Replace with your verified SendGrid email
RECEIVER_EMAIL = "rborse1213@gmail.com"

import os
import requests

def download_resume():
    """Download the resume from Google Drive and save it locally."""
    file_url = "https://drive.google.com/uc?id=19XpvXDI5-mjfyy8WSLmsaaZXq-peO83H&export=download"
    local_path = "Rohan_Borse.pdf"

    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("Resume downloaded successfully!")
    else:
        print("Failed to download resume.")

    return local_path


def send_email_notification():
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        # Create email content
        from_email = Email(SENDER_EMAIL)
        to_email = To(RECEIVER_EMAIL)
        subject = "✅Resume Update🚀 Confirmation👍✅"
        content = Content("text/plain", "Hello Rohan,\n\nYour resume has been successfully updated on Naukri.com. \n\nBest Regards,\nAno..")

        # Prepare the mail object
        mail = Mail(from_email, to_email, subject, content)

        # Send the email
        response = sg.send(mail)

        # Check the response status code
        if response.status_code == 202:
            print("Email notification sent successfully!✅✅✅✅")
        else:
            print(f"Failed to send email. Status Code: {response.status_code}")

    except Exception as e:
        print(f"Failed to send email: {e}")

def not_send_email_notification():
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        # Create email content
        from_email = Email(SENDER_EMAIL)
        to_email = To(RECEIVER_EMAIL)
        subject = "⛔⛔⛔⛔Resume Update Error ⛔⛔⛔⛔"
        content = Content("text/plain", "Hello Rohan,\n\nYour resume has not updated on Naukri.com. \n\nBest Regards,\nAno..")

        # Prepare the mail object
        mail = Mail(from_email, to_email, subject, content)

        # Send the email
        response = sg.send(mail)

        # Check the response status code
        if response.status_code == 202:
            print("Email notification sent successfully!⛔⛔⛔")
        else:
            print(f"Failed to send email. Status Code: {response.status_code}")

    except Exception as e:
        print(f"Failed to send email: {e}")

def update_profile_summary():
    RESUME_PATH = download_resume()
    # Setup WebDriver with options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-popup-blocking")  # Prevent pop-ups from interfering
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.naukri.com/")
        driver.maximize_window()

        # Handle pop-ups (if any)
        try:
            close_popup = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
            )
            close_popup.click()
        except:
            pass  # No pop-up found

            # Click on Login
            login_button = driver.find_element(By.LINK_TEXT, "Login")
            login_button.click()
            time.sleep(3)

            # Enter email
            email_field = driver.find_element(By.XPATH, "//input[@type='text' and @maxlength='100']")
            email_field.send_keys(EMAIL)

            # Enter password
            password_field = driver.find_element(By.XPATH, "//input[@type='password' and @maxlength='40']")
            password_field.send_keys(PASSWORD)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)

            # Navigate to Profile Page
            driver.get("https://www.naukri.com/mnjuser/profile")
            time.sleep(5)

        # Find "Attach CV" input and upload file
        upload_cv = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "attachCV"))
        )
        upload_cv.send_keys(RESUME_PATH)  # Upload Resume
        time.sleep(3)

        print("Resume updated successfully!")
        send_email_notification()  # Send Email Notification

    except Exception as e:
        print(f"Error: {e}")
        not_send_email_notification()
    finally:
        driver.quit()


# Run the script
update_profile_summary()
