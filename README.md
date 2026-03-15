Google Maps Lead Scraper
A powerful, asynchronous Python scraper built with Playwright and Playwright-Stealth to extract business information (Names, Phone Numbers, and Addresses) from Google Maps.

This specific implementation is configured to find "Madrasas" in specific areas, but it can be easily adapted for any business type.

🚀 Features
Asynchronous Scraping: Uses asyncio to handle multiple locations simultaneously.

Stealth Mode: Integrates playwright-stealth to reduce the risk of being blocked or flagged as a bot.

Automated CSV Export: Saves all extracted data into a clean, UTF-8 encoded CSV file.

Deep Extraction: Clicks into each listing to fetch phone numbers and addresses that aren't visible on the main results page.

🛠️ Prerequisites
Before running the script, ensure you have Python 3.8+ installed and the following libraries:

Playwright: For browser automation.

Playwright-Stealth: To bypass bot detection.

📥 Installation
Clone the repository (or save the script to a folder):

Bash
git clone https://github.com/yourusername/gmaps-scraper.git
cd gmaps-scraper
Install Python dependencies:

Bash
pip install playwright playwright-stealth
Install Playwright Browsers:
Playwright requires its own browser binaries to run. Install them using:

Bash
playwright install chromium
⚙️ How to Use
Configure Search:
Open the script and locate the main() function. You can change the locations list and the query variable:

Python
locations = ["Tongi", "Uttara", "Dhaka"]
query = "Pharmacy" # Or any other business type
Run the Scraper:

Bash
python scraper.py
View Results:
Once finished, a file named madrasa_leads_final.csv will be created in your project directory.

📂 Project Structure
scraper.py: The main asynchronous script.

madrasa_leads_final.csv: The output file containing the scraped data.

README.md: Project documentation.

⚠️ Important Notes & Disclaimer
Headless Mode: The script is currently set to headless=True. If you want to see the browser in action while debugging, change it to False in the main() function.

Wait Times: The script includes asyncio.sleep(5) to allow the Google Maps side panel to load. If your internet is slow, you may need to increase this.

Ethics: This tool is for educational purposes. Please respect Google's Terms of Service and use the data responsibly.