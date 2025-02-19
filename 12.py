import schedule
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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EMAIL = "rborse1213@gmail.com"
PASSWORD = "Rohan@1213"
RESUME_PATH = "C:\\Users\\rohan\\Downloads\\Rohan_Borse.pdf"

SENDGRID_API_KEY = 'YOUR_SENDGRID_API_KEY'  # Replace with your SendGrid API Key
SENDER_EMAIL = "borserohan5308@gmail.com"  # Replace with your verified SendGrid email
RECEIVER_EMAIL = "rborse1213@gmail.com"


def send_email_notification(success=True):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        subject = "✅ Resume Update Success" if success else "⛔ Resume Update Failed"
        content = "Your resume has been successfully updated on Naukri.com." if success else "Your resume update failed."
        mail = Mail(Email(SENDER_EMAIL), To(RECEIVER_EMAIL), subject, Content("text/plain", content))
        response = sg.send(mail)
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


def update_profile_summary():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("--disable-popup-blocking")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)  # Implicit wait for stability

    try:
        logging.info("Opening Naukri.com")
        driver.get("https://www.naukri.com/")

        # Close pop-ups if present
        try:
            close_popup = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
            )
            close_popup.click()
            logging.info("Closed pop-up window.")
        except:
            logging.info("No pop-up found.")

        # Click on Login
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
        login_button.click()
        logging.info("Clicked on Login button.")

        # Enter email and password
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        email_field.send_keys(EMAIL)

        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)
        logging.info("Entered login credentials and submitted form.")

        # Navigate to Profile Page
        driver.get("https://www.naukri.com/mnjuser/profile")
        logging.info("Navigated to profile page.")

        # Upload Resume
        upload_cv = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "attachCV"))
        )
        upload_cv.send_keys(RESUME_PATH)
        logging.info("Resume uploaded successfully!")

        send_email_notification(success=True)

    except Exception as e:
        logging.error(f"Error updating resume: {e}")
        send_email_notification(success=False)

    finally:
        driver.quit()

update_profile_summary()
# # Schedule the task to run daily
# schedule.every().day.at("09:30").do(update_profile_summary)
#
# logging.info("Scheduler started. Running every day at 09:30 AM IST.")
# while True:
#     schedule.run_pending()
#     time.sleep(60)
