import logging
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Setup ChromeDriver automatically
logging.info("Setting up ChromeDriver...")
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Target website
url = "https://cpj.org/data/?status=Killed&start_year=1992&end_year=2025&group_by=year&motiveConfirmed%5B%5D=Confirmed&type%5B%5D=Journalist"
driver.get(url)
logging.info(f"Opened URL: {url}")

# Function to scrape data from the current page
def scrape_page():
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-report-builder-table")))
        table = driver.find_element(By.CLASS_NAME, "js-report-builder-table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        journalists_data = []
        for row in rows[1:]:  # Skip header row
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) >= 4:
                name = columns[0].text.strip()
                organization = columns[1].text.strip()
                date = columns[2].text.strip()
                location = columns[3].text.strip()
                
                try:
                    profile_link = columns[0].find_element(By.TAG_NAME, "a").get_attribute("href")
                except NoSuchElementException:
                    profile_link = "N/A"

                journalists_data.append({
                    "Name": name,
                    "Organization": organization,
                    "Date": date,
                    "Location": location,
                    "Profile Link": profile_link
                })

        logging.info(f"Scraped {len(journalists_data)} entries from the current page.")
        return journalists_data

    except Exception as e:
        logging.error(f"Error scraping page: {e}")
        return []

# Function to go to the next page
def click_next_page():
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next')]"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)

        if "disabled" in next_button.get_attribute("class"):
            logging.info("Reached the last page.")
            return False

        driver.execute_script("arguments[0].click();", next_button)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".js-report-builder-table tr:nth-child(2) td:nth-child(1) a"))
        )
        time.sleep(2)
        return True

    except TimeoutException:
        logging.info("No more pages to navigate. Ending scraping.")
        return False
    except Exception as e:
        logging.error(f"Error clicking 'Next': {e}")
        return False

# Main scraping loop
all_journalists = []
page_number = 1
max_pages = 84  # Adjust based on actual site structure

while page_number <= max_pages:
    logging.info(f"Scraping page {page_number}...")
    journalists = scrape_page()
    all_journalists.extend(journalists)

    if not click_next_page():
        break

    page_number += 1

# Save to CSV only if data is scraped
csv_filename = "cpj_missing_journalists.csv"
if all_journalists:
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Organization", "Date", "Location", "Profile Link"])
        writer.writeheader()
        writer.writerows(all_journalists)
    logging.info(f"Data saved to {csv_filename}")
else:
    logging.warning("No data scraped. CSV file not created.")

driver.quit()
logging.info("Scraping finished and browser closed.")
