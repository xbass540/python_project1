import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import random

# Generate a random 4-digit number for the filename
random_number = random.randint(1000, 9999)
filename = f'meta-descriptions-scrapping-{random_number}.csv'

# Ensure the output folder exists
output_folder = 'meta-descriptions-missing'
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

# Open CSV file and write headers
csv_file = open(os.path.join(output_folder, filename), 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Post Name', 'Post URL', 'Meta Description', 'Posts with Issues'])

# Set the base URL and a list to store visited URLs
base_url = "https://solomondesigns.co.uk"
visited_urls = set()

# Initialize counters
article_counter = 1
issues_counter = 0  # Counter for posts with issues

def scrape_page(url):
    global article_counter, issues_counter  # Use global counters

    # Avoid revisiting the same URL
    if url in visited_urls:
        return
    visited_urls.add(url)

    # Fetch the page content
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Scraping URL: {url}")

    # Extract meta description from the page
    meta_description_tag = soup.find('meta', property="og:description")
    meta_description = meta_description_tag['content'].strip() if meta_description_tag and 'content' in meta_description_tag.attrs and meta_description_tag['content'] else "No description"

    # Count posts with no meta descriptions
    if meta_description == "No description":
        issues_counter += 1

    # Extract content of interest (customize based on website structure)
    for article in soup.find_all('article'):
        headline = article.find('h2').text.strip() if article.find('h2') else "No headline"
        article_url = article.find('a', href=True)
        if article_url:
            full_url = urljoin(base_url, article_url['href'])  # Convert relative URL to absolute
            print(f"Article {article_counter}: {headline}, URL: {full_url}, Meta Description: {meta_description}")
            csv_writer.writerow([headline, full_url, meta_description, issues_counter])  # Write to CSV
            article_counter += 1  # Increment the article counter

    # Extract all links on the page
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])  # Convert relative URL to absolute
        if base_url in full_url:  # Ensure the link is part of the same domain
            scrape_page(full_url)  # Recursively scrape the next page

# Start scraping from the homepage
scrape_page(base_url)

# Write final count of posts with issues to the CSV file
csv_writer.writerow(['', '', 'Total Posts with Issues:', issues_counter])

# Close the CSV file
csv_file.close()

print(f"Scraping complete. Results saved to {os.path.join(output_folder, filename)}")
