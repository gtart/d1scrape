# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_daltile_lvt():
    url = "https://www.daltile.com/lvt"

    # Set up headless Chrome for Replit
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome invisibly
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up ChromeDriver service correctly
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("🌐 Loading page...")
    driver.get(url)

    # Wait for JavaScript to load
    time.sleep(5)

    # Grab fully rendered HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all products
    products = soup.find_all('div', class_='search-result-item')

    print(f"🔎 Found {len(products)} products on page.")

    scraped_data = []

    for product in products[:50]:  # Limit to first 50 products
        try:
            name_tag = product.find('div', class_='search-result-product-name')
            name = name_tag.get_text(strip=True) if name_tag else "No Name"

            img_tag = product.find('img')
            image_url = img_tag['src'] if img_tag else "No Image URL"

            scraped_data.append({
                'Name': name,
                'Image URL': image_url,
                'Source Page': url
            })
        except Exception as e:
            print(f"⚠️ Error parsing a product: {e}")

    driver.quit()
    return scraped_data

def main():
    print("🚀 Starting Daltile LVT scraper...")
    all_data = scrape_daltile_lvt()

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('daltile_lvt_products.csv', index=False)
        print("✅ Scraping complete! Data saved to daltile_lvt_products.csv")
    else:
        print("⚠️ No data scraped.")

if __name__ == "__main__":
    main()
