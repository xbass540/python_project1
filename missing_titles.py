import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import random
import tkinter as tk  # For output_text display


def scrape_missing_titles(base_url, output_text, stop_scraping_flag):
    base_url = base_url.rstrip("/")  # Normalize URL
    visited_urls = set()
    scraped_data = []  # Store results in memory

    def scrape_page(url):
        nonlocal scraped_data

        if stop_scraping_flag():
            output_text.insert(tk.END, "Scraping stopped by user.\n")
            output_text.see("end")
            return

        if url in visited_urls:
            return
        visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 404:
                output_text.insert(tk.END, f"404 Not Found: {url}\n")
                output_text.see("end")
                scraped_data.append(["Article", url, "404 Not Found"])
                return
            response.raise_for_status()

            if "text/html" not in response.headers.get("Content-Type", ""):
                return

            response.encoding = response.apparent_encoding

        except requests.exceptions.RequestException as e:
            output_text.insert(tk.END, f"Failed to fetch {url}: {e}\n")
            output_text.see("end")
            return

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            output_text.insert(tk.END, f"Error parsing {url}: {e}\n")
            output_text.see("end")
            return

        output_text.insert(tk.END, f"Scraping URL: {url}\n")
        output_text.see("end")

        page_title = soup.find('title').text.strip() if soup.find('title') else "No title"
        issue_status = "Missing Title Tag" if page_title == "No title" else "Page Found"
        scraped_data.append([page_title, url, issue_status])

        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if base_url in full_url:
                scrape_page(full_url)

    scrape_page(base_url)

    output_text.insert(tk.END, "Scraping complete.\n")
    return scraped_data  # Return collected data for export


def export_missing_titles(scraped_data, base_url):
    if not scraped_data:
        print("No data to export.")
        return

    from tkinter import filedialog, Tk
    root = Tk()
    root.withdraw()

    folder_selected = filedialog.askdirectory(title="Select Folder to Save CSV")
    if not folder_selected:
        print("Export canceled. No folder selected.")
        return

    random_number = random.randint(1000, 9999)
    safe_url_part = base_url.replace("https://", "").replace("http://", "").replace("/", "_")[:30]
    filename = f"{random_number}_missing_titles_{safe_url_part}.csv"
    csv_file_path = os.path.join(folder_selected, filename)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Post Name", "Post URL", "Title Status"])
        csv_writer.writerows(scraped_data)

    print(f"Export complete. File saved to: {csv_file_path}")
