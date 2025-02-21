import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import random
import re
import tkinter as tk
from tkinter import filedialog  # For selecting save location

def sanitize_filename(url):
    """Convert URL into a safe filename by removing protocol and special characters."""
    clean_url = re.sub(r"https?://", "", url)  # Remove http:// or https://
    clean_url = re.sub(r"[^\w\-]", "_", clean_url)  # Replace non-alphanumeric chars
    return clean_url[:30]  # Keep filename manageable (limit to 30 chars)


def scrape_meta_descriptions(base_url, output_text, stop_scraping_flag):
    base_url = base_url.rstrip("/")
    scraped_data = []
    visited_urls = set()
    article_counter = 1
    issues_counter = 0

    def scrape_page(url):
        nonlocal article_counter, issues_counter
        if stop_scraping_flag():
            output_text.insert(tk.END, "Scraping stopped by user.\n")
            output_text.see("end")
            return
        if url in visited_urls:
            return
        visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            output_text.insert(tk.END, f"Failed to fetch {url}: {e}\n")
            output_text.see("end")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        output_text.insert(tk.END, f"Scraping URL: {url}\n")
        output_text.see("end")

        meta_description_tag = soup.find('meta', property="og:description")
        meta_description = meta_description_tag['content'].strip() if meta_description_tag and 'content' in meta_description_tag.attrs else "No description"

        if meta_description == "No description":
            issues_counter += 1

        for article in soup.find_all('article'):
            if stop_scraping_flag():
                output_text.insert(tk.END, "Scraping stopped by user.\n")
                output_text.see("end")
                return

            headline = article.find('h2').text.strip() if article.find('h2') else "No headline"
            article_url = article.find('a', href=True)
            if article_url:
                full_url = urljoin(base_url, article_url['href'])
                scraped_data.append([headline, full_url, meta_description, issues_counter])
                article_counter += 1

        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if base_url in full_url:
                scrape_page(full_url)

    scrape_page(base_url)

    output_text.insert(tk.END, "\nScraping complete. Click 'Export' to save the data.\n")
    output_text.see("end")

    return scraped_data

def export_meta_descriptions(scraped_data, base_url):
    if not scraped_data:
        print("No data to export.")
        return

    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        print("Export canceled.")
        return

    random_number = random.randint(1000, 9999)
    safe_url_part = sanitize_filename(base_url)
    filename = f"{random_number}_meta_descriptions_{safe_url_part}.csv"
    csv_file_path = os.path.join(folder_selected, filename)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Post Name', 'Post URL', 'Meta Description', 'Posts with Issues'])
        csv_writer.writerows(scraped_data)

    print(f"\nExport complete. File saved to: {csv_file_path}")
