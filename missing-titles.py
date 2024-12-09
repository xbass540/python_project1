import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import random

# Set the base URL and a list to store visited URLs
base_url = input('Enter website URL: ').strip()
visited_urls = set()

# Initialize counters
article_counter = 1
issues_counter = 0  # Counter for posts with missing title tags

# Generate a random 4-digit number for the filename
random_number = random.randint(1000, 9999)
filename = f'{base_url[8:].replace("/", "_")}-{random_number}.csv'

# Ensure the output folder exists
output_folder = 'post-titles-missing'
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

# Open CSV file and write headers
csv_file = open(os.path.join(output_folder, filename), 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Post Name', 'Post URL', 'Title Not Found', 'Posts with Issues'])

def scrape_page(url):
    global article_counter, issues_counter  # Use global counters

    # Avoid revisiting the same URL
    if url in visited_urls:
        return
    visited_urls.add(url)

    # Fetch the page content
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            # If the page is not found, record the issue and return
            print(f"404 Not Found: {url}")
            csv_writer.writerow([f"Article {article_counter}", url, "404 Not Found", issues_counter])
            issues_counter += 1
            return
        response.raise_for_status()

        # Validate content type
        if "text/html" not in response.headers.get("Content-Type", ""):
            print(f"Non-HTML content at {url}, skipping.")
            return

        # Handle encoding
        response.encoding = response.apparent_encoding

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    # Parse the HTML content
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return

    print(f"Scraping URL: {url}")

    # Extract the page title for the post name
    page_title = soup.find('title').text.strip() if soup.find('title') else "No title"

    # Check if the title tag is missing, and record the issue
    if page_title == "No title":
        issues_counter += 1
        not_found_message = "Missing Title Tag"
    else:
        not_found_message = "Page Found"

    # Record the article and URL
    csv_writer.writerow([page_title, url, not_found_message, issues_counter])  # Write to CSV
    article_counter += 1  # Increment the article counter

    # Extract all links on the page
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])  # Convert relative URL to absolute
        # Skip if already visited or not the same domain
        if full_url not in visited_urls and base_url in full_url:
            scrape_page(full_url)  # Recursively scrape the next page

# Start scraping from the homepage
scrape_page(base_url)

# Write final count of posts with issues to the CSV file
csv_writer.writerow(['', '', 'Total Pages with Issues:', issues_counter])

# Close the CSV file
csv_file.close()

print(f"Scraping complete. Results saved to {os.path.join(output_folder, filename)}")
