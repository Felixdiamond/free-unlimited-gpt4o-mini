from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import random

# Configuration
geckodriver_path = '/usr/local/bin/geckodriver'
url = "https://chatgpt.com"
prompt = "What is the meaning of life?"

# Setup Firefox options
options = Options()
options.headless = False  # Set to True if running in headless mode

print("Using profile")
profile = FirefoxProfile('/home/ayane/.cache/mozilla/firefox/xe09j14o.default-release')
options.profile = profile

print("Initializing Firefox driver...")
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

def random_delay(min_time=1, max_time=3):
    time.sleep(random.uniform(min_time, max_time))

def send_prompt(prompt):
    print("Sending prompt...")
    # Locate the textarea and input the prompt
    textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'prompt-textarea'))
    )
    textarea.clear()
    random_delay(0.5, 1.5)  # Simulate typing delay
    textarea.send_keys(prompt)
    random_delay(1, 2)
    textarea.send_keys(Keys.RETURN)

def await_response():
    try:
        print("Waiting for response...")
        response = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'markdown') and contains(@class, 'prose')]//p[text()='{prompt}']"))
        )
        return response
    except TimeoutException:
        print("Response waiting timed out.")
        return None

def main():
    print("Navigating to ChatGPT...")
    driver.get(url)

    random_delay(2, 4)  # Wait for the page to load fully

    try:
        # Wait for the body element to be present
        print("Getting the body element")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        try:
            # Try to locate and interact with the 'Stay logged out' link
            logged_out_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Stay logged out'))
            )
            print("Popup detected, closing")
            logged_out_link.click()
            random_delay(1, 2)
        except TimeoutException:
            print("No 'Stay logged out' link found, continuing...")

        # Continue with the rest of the script
        send_prompt(prompt)
        response = await_response()
        if response:
            print("Response: ", response.text)
        else:
            print("No response received.")
    
    finally:
        driver.quit()

def just_get_url_only():
    driver.get(url)
    random_delay(2, 4)

if __name__ == "__main__":
    main()
