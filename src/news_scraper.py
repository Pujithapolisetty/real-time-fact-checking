import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_news():
    """Scrapes news headlines, descriptions, and links from BBC News."""

    # Configure Selenium
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Load BBC News website
    driver.get("https://www.bbc.com/news")
    
    # Wait for JavaScript to load
    time.sleep(5)

    # Get page source
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # Close browser session

    # Extract news articles
    articles = soup.find_all("a", {"data-testid": "internal-link"})  # Finds all news article links

    scraped_data = []

    for article in articles[:15]:  # Get top 15 articles
        headline_tag = article.find("h2", {"data-testid": "card-headline"})
        description_tag = article.find("p", {"data-testid": "card-description"})
        category_tag = article.find("span", {"data-testid": "card-metadata-tag"})
        
        headline = headline_tag.get_text().strip() if headline_tag else None
        description = description_tag.get_text().strip() if description_tag else None
        category = category_tag.get_text().strip() if category_tag else None
        url = "https://www.bbc.com" + article["href"]

        # Skip articles with missing headlines or irrelevant URLs
        if not headline or "/sport" in url or "/video" in url or url == "https://www.bbc.com/":
            continue

        scraped_data.append({
            "headline": headline,
            "description": description if description else "No description",
            "category": category if category else "General",
            "url": url
        })

    print(f"✅ Found {len(scraped_data)} valid articles.")

    # Save to JSON file
    with open("scraped_news.json", "w", encoding="utf-8") as json_file:
        json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)
    
    print("✅ News data saved to scraped_news.json")

    return scraped_data

if __name__ == "__main__":
    news_articles = scrape_news()
