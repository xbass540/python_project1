import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import random

# Set the base URL and a list to store visited URLs
base_url = "https://womenoutdoors.co.uk"
visited_urls = set()

# Initialize counters
article_counter = 1
issues_counter = 0  # Counter for posts with issues

# Generate a random 4-digit number for the filename
random_number = random.randint(1000, 9999)
filename = f'{base_url[8:]}-{random_number}.csv'

# Ensure the output folder exists
output_folder = 'not-found-404'
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

# Open CSV file and write headers
csv_file = open(os.path.join(output_folder, filename), 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Post Name', 'Post URL', 'Not Found', 'Posts with Issues'])

def scrape_page(url):
    global article_counter, issues_counter  # Use global counters

    # Avoid revisiting the same URL
    if url in visited_urls:
        return
    visited_urls.add(url)

    # Fetch the page content
    try:
        response = requests.get(url)
        if response.status_code == 404:
            # If the page is not found, record the issue and return
            print(f"404 Not Found: {url}")
            csv_writer.writerow([f"Article {article_counter}", url, "404 Not Found", issues_counter])
            issues_counter += 1
            return
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Scraping URL: {url}")

    # Extract the page title for the post name
    page_title = soup.find('title').text.strip() if soup.find('title') else "No title"

    # Record the article and URL
    csv_writer.writerow([page_title, url, "Page Found", issues_counter])  # Write to CSV
    article_counter += 1  # Increment the article counter

    # Extract all links on the page
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])  # Convert relative URL to absolute
        if base_url in full_url:  # Ensure the link is part of the same domain
            scrape_page(full_url)  # Recursively scrape the next page

# Start scraping from the homepage
scrape_page(base_url)

# Write final count of posts with issues to the CSV file
csv_writer.writerow(['', '', 'Total Pages with Issues:', issues_counter])

# Close the CSV file
csv_file.close()

print(f"Scraping complete. Results saved to {os.path.join(output_folder, filename)}")
