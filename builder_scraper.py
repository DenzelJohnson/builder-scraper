from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://obd.hcraontario.ca"
SEARCH_URL = f"{BASE_URL}/buildersearchresults?&page="

def fetch_detail_page(driver, detail_url):
    detail_data = {"Address": "", "Website": "", "Email": "", "Phone Number": ""}
    
    if not detail_url:
        print("Warning: No detail URL found.")
        return detail_data

    print(f"Visiting Detail Page: {BASE_URL + detail_url}")
    driver.get(BASE_URL + detail_url)
    
    try:
        # Wait for the Overview section to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.bold")))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Safely extract fields
        fields = soup.find_all("div", style=lambda x: x and "padding-left: 15px" in x)
        for field in fields:
            header = field.find("span", class_="bold")
            value = field.find("p")
            
            if header and value:  # Safeguard for missing elements
                header_text = header.text.strip()
                value_text = value.text.strip()
                print(f"Extracted: {header_text} -> {value_text}")

                if "Address" in header_text:
                    detail_data["Address"] = value_text
                elif "Website" in header_text:
                    detail_data["Website"] = value_text
                elif "Email" in header_text:
                    detail_data["Email"] = value_text
                elif "Phone Number" in header_text:
                    detail_data["Phone Number"] = value_text

    except Exception as e:
        print(f"Error fetching detail page: {e}")
    
    return detail_data


def scrape_builders_to_csv():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    all_data = []

    for page in range(1, 6):  # Adjust for total pages
        print(f"--- Scraping Page {page} ---")
        driver.get(SEARCH_URL + str(page))

        try:
            # Wait for table rows to appear
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr")))
            print("Table rows loaded successfully.")
            
            # Parse fully-loaded content
            soup = BeautifulSoup(driver.page_source, "html.parser")
            rows = soup.select("tbody tr")
            print(f"Number of Rows Found: {len(rows)}")

            for row in rows:
                try:
                    # Vendor Link and Name
                    vendor_link = row.select_one("a.title")
                    vendor = vendor_link.text.strip() if vendor_link else "N/A"
                    detail_url = vendor_link["href"] if vendor_link else None
            
                    # DBA Name
                    dba_name_tag = row.select_one("td.title")
                    dba_name = dba_name_tag.text.strip() if dba_name_tag else "N/A"
            
                    # Location
                    location_tag = row.select_one("td.sentenceCase")
                    location = location_tag.text.strip() if location_tag else "N/A"
            
                    # Licensed and License Status
                    licensed_cells = row.select("td.unlicensed.bold")
                    licensed = licensed_cells[0].get_text(strip=True) if len(licensed_cells) > 0 else "N/A"
                    license_status = licensed_cells[1].get_text(strip=True) if len(licensed_cells) > 1 else "N/A"
            
                    print(f"Vendor: {vendor}, DBA Name: {dba_name}, Location: {location}, Licensed: {licensed}, License Status: {license_status}")
            
                    # Fetch data from the detail page
                    detail_data = fetch_detail_page(driver, detail_url) if detail_url else {}
                    
                    # Combine all data into a dictionary
                    row_data = {
                        "Vendor": vendor,
                        "DBA Name": dba_name,
                        "Location": location,
                        "Licensed": licensed,
                        "License Status": license_status,
                        "Address": detail_data.get("Address", ""),
                        "Website": detail_data.get("Website", ""),
                        "Email": detail_data.get("Email", ""),
                        "Phone Number": detail_data.get("Phone Number", "")
                    }
                    print("Row Data Extracted:", row_data)
                    all_data.append(row_data)
            
                except Exception as e:
                    print(f"Error processing row: {e}")


        except Exception as e:
            print(f"Error on Page {page}: {e}")
            continue
    
    # Save data to CSV
    df = pd.DataFrame(all_data)
    df.to_csv("ontario_builders.csv", index=False)
    print("Data successfully saved to 'ontario_builders.csv'!")
    driver.quit()

if __name__ == "__main__":
    scrape_builders_to_csv()
