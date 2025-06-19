# WhatsApp Automation Tool

A Python-based automation tool that sends personalized WhatsApp messages to multiple contacts using Selenium WebDriver.

## Features

- Send personalized messages to multiple WhatsApp contacts
- Maintains chat history and tracks successful/unsuccessful message deliveries
- Handles errors and timeouts gracefully
- Saves progress to resume later
- Cross-platform compatible (Windows, macOS, Linux)

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- WhatsApp Web access
- A CSV file containing contact information (name and phone number)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/donkorBN/whatsapp-automation.git
   cd whatsapp-automation
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   If you don't have a requirements.txt file, install the dependencies manually:
   ```bash
   pip install selenium pandas webdriver-manager keyboard
   ```

## Usage

1. Prepare a CSV file named `clean.csv` with the following columns:
   - `name`: Contact's name
   - `phone`: Contact's phone number with country code (e.g., +1234567890)

2. Run the script:
   ```bash
   python whatsapp_text.py
   ```

3. When prompted, scan the QR code with your WhatsApp mobile app to log in.

4. The script will start sending messages to the contacts in your CSV file.

## How It Works

1. The script uses Selenium WebDriver to automate Chrome browser interactions with WhatsApp Web.
2. It reads contact information from the CSV file.
3. For each contact, it:
   - Searches for the contact in WhatsApp Web
   - Sends a personalized message
   - Tracks successful and failed deliveries
   - Saves progress to resume later if interrupted

## Important Notes

- **Use Responsibly**: This tool is for educational purposes only. Please respect WhatsApp's Terms of Service and use it responsibly.
- **Rate Limiting**: The script includes random delays between messages to avoid being flagged as spam.
- **Data Privacy**: Your WhatsApp data and contact information remain on your local machine.

## Troubleshooting

- **ChromeDriver Issues**: The script automatically manages ChromeDriver using webdriver-manager.
- **Login Problems**: Ensure you have a stable internet connection and can access WhatsApp Web in your browser.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This project is not affiliated with, authorized, maintained, sponsored, or endorsed by WhatsApp or any of its affiliates or subsidiaries. This is an independent and unofficial software. Use at your own risk. Thank you
