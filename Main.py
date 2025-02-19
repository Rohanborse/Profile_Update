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
import os
import requests

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

SENDER_EMAIL = "updatenaukari1@gmail.com"  
RECEIVER_EMAIL = "rborse1213@gmail.com"

def download_resume():
    file_url = "https://drive.google.com/uc?id=19XpvXDI5-mjfyy8WSLmsaaZXq-peO83H&export=download"
    local_path = "Rohan_Borse.pdf"

    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("✅ Resume downloaded successfully!")
    else:
        print("⛔ Failed to download resume.")

    return local_path

def send_email_notification(success=True):
    """Send email notification based on resume update success or failure."""
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = Email(SENDER_EMAIL)
        to_email = To(RECEIVER_EMAIL)

        if success:
            subject = "✅ Resume Update Confirmation 🚀"
            content_text = "Hello Rohan,\n\nYour resume has been successfully updated on Naukri.com.\n\nBest Regards,\nAno.."
        else:
            subject = "⛔ Resume Update Failed"
            content_text = "Hello Rohan,\n\nThere was an error updating your resume on Naukri.com.\n\nBest Regards,\nAno.."

        mail = Mail(from_email, to_email, subject, Content("text/plain", content_text))
        response = sg.send(mail)

        if response.status_code == 202:
            print(f"📧 Email notification sent successfully! ({subject})")
        else:
            print(f"⚠️ Failed to send email. Status Code: {response.status_code}")

    except Exception as e:
        print(f"❌ Email notification error: {e}")

def update_profile_summary():
    RESUME_PATH = download_resume()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Updated headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass Selenium detection
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.naukri.com/")
        driver.maximize_window()

        # Close pop-ups (if present)
        try:
            close_popup = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
            )
            close_popup.click()
        except:
            print("✅ No pop-ups found.")

        # Click Login
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
        login_button.click()
        time.sleep(3)

        # Enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @maxlength='100']"))
        )
        email_field.send_keys(EMAIL)

        # Enter password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @maxlength='40']"))
        )
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # Navigate to Profile Page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Upload Resume
        upload_cv = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "attachCV"))
        )
        upload_cv.send_keys(RESUME_PATH)  # Upload Resume
        time.sleep(3)

        print("🎉 Resume updated successfully!")
        send_email_notification(success=True)

    except Exception as e:
        print(f"❌ Error: {e}")
        send_email_notification(success=False)

    finally:
        driver.quit()


# Run the script
update_profile_summary()
