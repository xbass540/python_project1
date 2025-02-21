import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import random
import tkinter as tk  # Import tkinter for output_text

def scrape_404_errors(base_url, output_folder, output_text, stop_scraping_flag):
    base_url = base_url.rstrip("/")  # Remove trailing slash if it exists

    # Generate a random 4-digit number for the filename
    random_number = random.randint(1000, 9999)
    filename = f'{base_url[8:]}-404-errors-{random_number}.csv'

    # Open CSV file in the selected output folder
    csv_file_path = os.path.join(output_folder, filename)
    csv_file = open(csv_file_path, 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Post Name', 'Post URL', 'Not Found', 'Posts with Issues'])

    visited_urls = set()  # Set to store visited URLs

    # Initialize counters
    article_counter = 1
    issues_counter = 0  # Counter for posts with issues

    def scrape_page(url):
        nonlocal article_counter, issues_counter  # Use nonlocal counters

        if stop_scraping_flag():
            output_text.insert(tk.END, "Scraping stopped by user.\n")
            output_text.see("end")
            return

        # Avoid revisiting the same URL
        if url in visited_urls:
            return
        visited_urls.add(url)

        # Fetch the page content
        try:
            response = requests.get(url)
            if response.status_code == 404:
                output_text.insert(tk.END, f"404 Not Found: {url}\n")
                output_text.see("end")
                csv_writer.writerow([f"Article {article_counter}", url, "404 Not Found", issues_counter])
                issues_counter += 1
                return
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            output_text.insert(tk.END, f"Failed to fetch {url}: {e}\n")
            output_text.see("end")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        output_text.insert(tk.END, f"Scraping URL: {url}\n")
        output_text.see("end")

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

    if not stop_scraping_flag():
        csv_writer.writerow(['', '', 'Total Pages with Issues:', issues_counter])
        output_text.insert(tk.END, f"\nScraping complete. Results saved to {csv_file_path}\n")
        output_text.see("end")

    csv_file.close()