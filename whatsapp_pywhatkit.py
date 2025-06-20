import pywhatkit
import time
import pandas as pd
from typing import List, Optional
import os

class WhatsAppPyWhatKit:
    def __init__(self, wait_time: int = 15, tab_close: bool = True, close_time: int = 2):
        """
        Initialize the WhatsAppPyWhatKit class.
        
        Args:
            wait_time (int): Time in seconds to wait for QR code scan
            tab_close (bool): Whether to close the browser tab after sending
            close_time (int): Time in seconds to keep the tab open after sending
        """
        self.wait_time = wait_time
        self.tab_close = tab_close
        self.close_time = close_time

    def send_message(self, phone_number: str, message: str) -> None:
        """
        Send a WhatsApp message to a single contact.
        
        Args:
            phone_number (str): Phone number with country code (e.g., '+1234567890')
            message (str): Message to send
        """
        try:
            print(f"Sending message to {phone_number}...")
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone_number,
                message=message,
                wait_time=self.wait_time,
                tab_close=self.tab_close,
                close_time=self.close_time
            )
            print(f"Message sent to {phone_number} successfully!")
            time.sleep(2)  # Small delay between messages
        except Exception as e:
            print(f"Error sending message to {phone_number}: {str(e)}")

    def send_bulk_messages(self, phone_numbers: List[str], message: str) -> None:
        """
        Send the same message to multiple contacts.
        
        Args:
            phone_numbers (List[str]): List of phone numbers with country codes
            message (str): Message to send
        """
        for number in phone_numbers:
            self.send_message(number, message)

    def send_messages_from_csv(self, csv_path: str, phone_column: str, message_column: Optional[str] = None, 
                             message: Optional[str] = None) -> None:
        """
        Send messages to contacts from a CSV file.
        
        Args:
            csv_path (str): Path to the CSV file
            phone_column (str): Name of the column containing phone numbers
            message_column (str, optional): Name of the column containing messages (if using custom messages)
            message (str, optional): Fixed message to send (if not using message_column)
        """
        if not os.path.exists(csv_path):
            print(f"Error: File not found at {csv_path}")
            return

        try:
            df = pd.read_csv(csv_path)
            
            if message_column and message_column in df.columns:
                # Send custom messages from the specified column
                for _, row in df.iterrows():
                    phone = str(row[phone_column]).strip()
                    msg = str(row[message_column])
                    self.send_message(phone, msg)
            elif message:
                # Send the same message to all contacts
                for phone in df[phone_column]:
                    self.send_message(str(phone).strip(), message)
            else:
                print("Error: Either message_column or message must be provided")
                
        except Exception as e:
            print(f"Error processing CSV file: {str(e)}")


def main():
    # Example usage
    whatsapp = WhatsAppPyWhatKit()
    
    # Example 1: Send to a single contact
    # whatsapp.send_message("+1234567890", "Hello from PyWhatKit!")
    
    # Example 2: Send to multiple contacts
    # contacts = ["+1234567890", "+1987654321"]
    # whatsapp.send_bulk_messages(contacts, "Hello everyone!")
    
    # Example 3: Send from CSV
    # whatsapp.send_messages_from_csv(
    #     csv_path="contacts.csv",
    #     phone_column="phone",
    #     message_column="message"  # Optional: Use this for custom messages
    #     # OR use this for same message to all:
    #     # message="Your fixed message here"
    # )

    print("Please uncomment and modify the example code in main() to start sending messages.")

if __name__ == "__main__":
    main()
