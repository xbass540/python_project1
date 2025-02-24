import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import random
import re
import tkinter as tk
from tkinter import filedialog
from collections import deque


def sanitize_filename(url):
    """Convert URL into a safe filename by removing protocol and special characters."""
    clean_url = re.sub(r"https?://", "", url)  # Remove http:// or https://
    clean_url = re.sub(r"[^\w\-]", "_", clean_url)  # Replace non-alphanumeric chars
    return clean_url[:20]  # Keep filename manageable (limit to 20 chars)


def scrape_missing_titles(urls, output_text, stop_scraping_flag, update_progress):
    """Scrape multiple URLs for missing title tags."""
    visited_urls = set()
    scraped_data = []  # Store results in memory
    queue = deque(urls)  # Use BFS with the provided URLs

    total_urls = len(urls)  # Total URLs to process

    while queue:
        if stop_scraping_flag():
            output_text.insert(tk.END, "Scraping stopped by user.\n")
            output_text.see("end")
            break

        url = queue.popleft()

        if url in visited_urls:
            continue
        visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 404:
                output_text.insert(tk.END, f"404 Not Found: {url}\n")
                output_text.see("end")
                scraped_data.append(["Article", url, "404 Not Found"])
                continue

            response.raise_for_status()

            if "text/html" not in response.headers.get("Content-Type", ""):
                scraped_data.append(["Non-HTML Content", url, "Skipped"])
                continue

            response.encoding = response.apparent_encoding

        except requests.exceptions.RequestException as e:
            output_text.insert(tk.END, f"Failed to fetch {url}: {e}\n")
            output_text.see("end")
            continue

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            output_text.insert(tk.END, f"Error parsing {url}: {e}\n")
            output_text.see("end")
            continue

        output_text.insert(tk.END, f"Scraping URL: {url}\n")
        output_text.see("end")
        output_text.update_idletasks()  # Keep GUI responsive

        page_title = soup.find('title').text.strip() if soup.find('title') else "No title"
        issue_status = "Missing Title Tag" if page_title == "No title" else "Page Found"
        scraped_data.append([page_title, url, issue_status])

        update_progress(len(visited_urls), total_urls)  # Update progress

    output_text.insert(tk.END, "Scraping complete.\n")
    output_text.see("end")
    return scraped_data  # Return collected data for export


def export_missing_titles(scraped_data, base_url):
    if not scraped_data:
        print("No data to export.")
        return

    root = tk.Tk()
    root.withdraw()

    folder_selected = filedialog.askdirectory(title="Select Folder to Save CSV")
    if not folder_selected:
        print("Export canceled. No folder selected.")
        return

    random_number = random.randint(1000, 9999)
    safe_url_part = sanitize_filename(base_url)
    filename = f"{random_number}_missing_titles_{safe_url_part}.csv"
    csv_file_path = os.path.join(folder_selected, filename)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Post Name", "Post URL", "Title Status"])
        csv_writer.writerows(scraped_data)

    print(f"Export complete. File saved to: {csv_file_path}")
