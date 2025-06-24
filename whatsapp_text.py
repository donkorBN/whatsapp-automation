import os
import re
import time
import random
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, UnexpectedAlertPresentException, NoAlertPresentException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import threading
import signal
import struct
import sys
import keyboard 

# Check Python architecture
print(f"Python architecture: {struct.calcsize('P') * 8}-bit")

# Set up Chrome options
chrome_options = Options()
user_data_dir = os.path.abspath("./User_Data")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--profile-directory=Default")

# Ensure correct version of ChromeDriver
driver_path = ChromeDriverManager().install()
driver_path = os.path.join(os.path.dirname(driver_path), 'chromedriver.exe')  # Correct the executable path
print(f"ChromeDriver executable path: {driver_path}")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

INDEX_FILE = 'current_index.txt'
stop_flag = False

def signal_handler(sig, frame):
    global stop_flag
    stop_flag = True

signal.signal(signal.SIGINT, signal_handler)

def listen_for_stop():
    global stop_flag
    print("Type 'stop' to terminate the process.")
    while not stop_flag:
        user_input = input("Enter command: ").strip().lower()
        if user_input == "stop":
            print("Stop signal detected. Exiting...")
            stop_flag = True

def get_greeting():
    current_hour = datetime.now().hour
    return "Good morning" if 5 <= current_hour < 12 else "Good evening"

def filter_non_bmp_characters(text):
    return re.sub(r'[\U00010000-\U0010FFFF]', '', text)

def whatsapp_update(driver, phone, message, not_found_file, full_name):
    try:
        print(f"Starting update for {full_name} ({phone})")
        
        # First try to click the new chat button directly
        try:
            new_chat_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='New chat']"))
            )
            new_chat_button.click()
            print("Clicked new chat")
        except Exception as e:
            print(f"Couldn't find new chat button, trying plan B: {e}")
            # Alternative method to open new chat
            try:
                menu_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@title='Menu']"))
                )
                menu_button.click()
                new_chat_menu = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'New chat')]"))
                )
                new_chat_menu.click()
                print("Opened new chat through menu")
            except Exception as e:
                print(f"Alternative method also failed: {e}")
                return False
        
        # Now enter the phone number
        try:
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@title='Search input textbox']//div[@contenteditable='true']"))
            )
            search_input.clear()
            search_input.send_keys(phone)
            print(f"Entered number: {phone}")
            time.sleep(2)  # Wait for search results
            
            # Try to find and click the contact
            try:
                contact = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[contains(@title, '{phone}')]"))
                )
                contact.click()
                print("Clicked on contact")
            except:
                # If no contact found, try to press enter
                try:
                    search_input.send_keys(Keys.ENTER)
                    print("Pressing ENTER to start chat")
                    time.sleep(2)
                except Exception as e:
                    print(f"Could not start chat: {e}")
                    return False
                    
            # Wait for the message box to appear
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
                )
                return True
            except:
                print(f"Message box not found for {full_name} ({phone})")
                return False
                
        except Exception as e:
            print(f"Error in search input: {e}")
            return False
            

        print(f"Message box found for {full_name}. Preparing to send message.")
        message_box = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        )

        try:
            filtered_message = filter_non_bmp_characters(message)
            print(f"Sending message: {filtered_message}")
            message_box.send_keys(filtered_message + Keys.ENTER)
            time.sleep(1)
            print(f"Message sent to {full_name} ({phone})")
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException: Trying to locate message box again for {full_name}")
            message_box = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
            )
            message_box.send_keys(filtered_message + Keys.ENTER)
            print(f"Message sent to {full_name} after retrying")

        return True
    except (TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException, WebDriverException) as e:
        print(f"Error sending message to {full_name} ({phone}): {str(e)}")
        return False
    finally:
        try:
            print(f"Cleaning up search box for {full_name}")
            search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
            search_box.send_keys(Keys.ESCAPE)
            search_box.clear()
            search_box.send_keys(Keys.ESCAPE)
            search_box.clear()
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

# Open WhatsApp Web
print("Opening WhatsApp Web...")
driver.get("https://web.whatsapp.com")
input("Press Enter after scanning the QR code and ensuring you're logged in: ")

try:
    contacts = pd.read_csv('clean.csv', dtype={'phone': str}, on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error reading CSV: {e}")
    driver.quit()
    sys.exit(1)

if 'phone' not in contacts.columns or 'name' not in contacts.columns:
    print("Error: 'phone' or 'name' column is missing in the CSV file.")
    driver.quit()
    sys.exit(1)

contacts.drop_duplicates(subset='phone', inplace=True)

message_template = (
"Hello {name}, I hope this message finds you well. My name is Nana Asiamah. I wanted to reach out because I organized the LinkedIn webinar last semester that you attended. I've already saved your contact in my phone, and I'd appreciate it if you could save mine as well if you haven't already so we stay connected. Let me know if there's anyway I can help"
)

if input("Do you want to start from the top? (yes/no): ").strip().lower() == 'yes':
    current_index = 0
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)
else:
    current_index = int(open(INDEX_FILE).read().strip()) if os.path.exists(INDEX_FILE) else 0

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
successful_file_path = f'./User_Data/successful_contacts_{timestamp}.txt'
not_found_file_path = f'./User_Data/not_found_contacts.txt'
sent_numbers = []
processed_numbers = set()

stop_thread = threading.Thread(target=listen_for_stop)
stop_thread.start()

try:
    for index in range(current_index, len(contacts)):
        if stop_flag:
            break

        current_index = index
        row = contacts.iloc[index]

        if pd.isna(row['phone']) or pd.isna(row['name']):
            continue

        phone = row['phone']
        full_name = row['name']

        if phone in processed_numbers:
            continue

        first_name = full_name.split()[0]
        personalized_message = message_template.format(name=first_name)

        if whatsapp_update(driver, phone, personalized_message, not_found_file_path, full_name):
            sent_numbers.append((full_name, phone))
            processed_numbers.add(phone)

        with open(INDEX_FILE, 'w') as f:
            f.write(str(current_index))

        time.sleep(random.uniform(1, 5))

finally:
    with open(successful_file_path, 'w', encoding='utf-8') as f:
        for number in sent_numbers:
            f.write(f"{number}\n")

    if stop_flag:
        print("Process stopped by user.")
    else:
        print("All messages sent successfully.")

    driver.quit()
