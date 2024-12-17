# Builder-Scraper

This Python script uses **Selenium** and **BeautifulSoup** to scrape builder information from the **Ontario Home Builder Directory** website. It dynamically extracts data from the main table and individual builder profile pages and saves the collected data into a structured **CSV file**.

---

## Features
- Scrapes builder information across multiple paginated pages.
- Extracts detailed contact information (Address, Website, Email, and Phone Number) from individual profile pages.
- Handles dynamic content loaded via JavaScript using Selenium.
- Saves extracted data to a **CSV file** for easy access and analysis.
- Includes error handling for missing or incomplete data.
- For reference, the script is designed to work with the Ontario Home Builder Directory:  
[Ontario Builder Search](https://obd.hcraontario.ca/buildersearchresults).


---

## Prerequisites

Before running the script, ensure you have the following installed:

- **Python 3.x**
- **Google Chrome** (latest version)
- **ChromeDriver** (automatically managed using `webdriver-manager`)

### Install Required Libraries
Run the following command to install necessary dependencies:
```bash
pip install selenium beautifulsoup4 pandas webdriver-manager
