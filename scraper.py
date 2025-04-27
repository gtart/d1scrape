# scraper.py

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_daltile_lvt():
    url = "https://www.daltile.com/lvt"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)  # wait 5 seconds for JS to load

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find_all('div', class_='search-result-item')

    scraped_data = []

    for product in products[:50]:  # limit to first 50 products
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

    return scraped_data

def main():
    print("🚀 Starting Daltile LVT scraper with Playwright...")
    all_data = scrape_daltile_lvt()

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('daltile_lvt_products.csv', index=False)
        print("✅ Scraping complete! Data saved to daltile_lvt_products.csv")
    else:
        print("⚠️ No data scraped.")

if __name__ == "__main__":
    main()
