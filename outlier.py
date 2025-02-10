from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests

def send_telegram_message():
    # Telegram Bot API token and chat ID
    BOT_TOKEN = "7895532465:AAFTwIFiFukfsoCNiwk1nLnqzRJnbDDIrVc"  # Replace with your bot token
    CHAT_ID = "2002142678"  # Replace with your chat ID

    # Build the URL for the Telegram Bot API
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Send a POST request with the message
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": "Projects available!"})

    # Check if the message was sent successfully
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")


def check_for_projects():
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--headless=new")  # Optional: Run in headless mode

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # **Set page load timeout for the initial page**
        driver.set_page_load_timeout(20)

        # **Open the website login page**
        print("Opening the login page...")
        try:
            driver.get('https://app.outlier.ai/en/expert/login')
        except TimeoutException:
            print("Initial page took too long to load. Stopping loading...")
            driver.execute_script("window.stop();")  # Stop the page from loading

        # **Wait for login elements**
        wait = WebDriverWait(driver, 30)
        email_field = wait.until(EC.visibility_of_element_located((By.ID, 'email')))
        password_field = wait.until(EC.visibility_of_element_located((By.ID, 'password')))

        # **Enter credentials**
        print("Entering credentials...")
        email_field.send_keys('mayankrauthan03@gmail.com')
        password_field.send_keys('Vkmvm987321t@')

        # **Locate and click login button**
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Login")]')))
        login_button.click()
        print("Logged in successfully.")

        # **After login, set another timeout**
        driver.set_page_load_timeout(15)  # Prevent infinite loading

        # **Try loading the next page**
        try:
            time.sleep(5)  # Allow some time for redirection
            driver.execute_script("window.stop();")  # Stop the page load forcefully
            print("Stopped page loading after login.")
        except Exception as e:
            print("stopped")

        # **Check for tasks**
        print("Checking for tasks...")
        try:
            no_task_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//strong[contains(text(), "Your task queue is currently empty")]'))
            )
            print("No tasks available.")
        except TimeoutException:
            print("Projects might be available!")
            send_telegram_message()


    finally:
        driver.quit()


if __name__ == "__main__":
    check_for_projects()
