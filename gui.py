import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, filedialog
import threading
from meta_descriptions import scrape_404_errors, export_meta_descriptions
from scrape_404_errors import scrape_404_errors, export_404_errors
from missing_titles import scrape_missing_titles, export_missing_titles
from utils import ensure_https
import requests
import xml.etree.ElementTree as ET

# Global variables
stop_scraping = False
missing_titles_data = []

def get_total_urls_from_sitemaps(base_url):
    """Fetches sitemap URLs and counts the total number of pages to be crawled."""
    sitemap_urls = [
        f"{base_url}/sitemap_index.xml",
        f"{base_url}/page-sitemap.xml",
        f"{base_url}/product-sitemap.xml",
        f"{base_url}/product_cat-sitemap.xml",
        f"{base_url}/product_tag-sitemap.xml"
    ]

    all_urls = set()
    headers = {"User-Agent": "Mozilla/5.0"}

    for sitemap_url in sitemap_urls:
        try:
            response = requests.get(sitemap_url, headers=headers, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                    all_urls.add(url.text)
        except Exception as e:
            print(f"Could not fetch {sitemap_url}: {e}")

    return len(all_urls), all_urls  # Return total count and URLs

def update_progress(current, total):
    """Updates the progress bar based on completed URLs."""
    if total > 0:
        progress = (current / total) * 100
        progress_var.set(progress)
        root.update_idletasks()  # Refresh GUI

def reset_progress():
    """Resets the progress bar to 0%."""
    progress_var.set(0)

def start_crawling():
    global stop_scraping, missing_titles_data
    base_url = url_entry.get().strip()
    base_url = ensure_https(base_url)

    if not base_url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    # Reset progress
    reset_progress()

    # Clear output areas
    meta_output_text.delete(1.0, tk.END)
    errors_output_text.delete(1.0, tk.END)
    titles_output_text.delete(1.0, tk.END)
    stop_scraping = False

    # Fetch URLs from sitemaps before crawling
    total_urls, all_urls = get_total_urls_from_sitemaps(base_url)

    if total_urls == 0:
        messagebox.showerror("Error", "No URLs found in the sitemap.")
        return

    # Start crawling with sitemap URLs
    thread_meta = threading.Thread(
        target=scrape_404_errors,
        args=(all_urls, meta_output_text, lambda: stop_scraping, lambda current, total: update_progress(current, total))
    )
    thread_404 = threading.Thread(
        target=scrape_404_errors,
        args=(all_urls, errors_output_text, lambda: stop_scraping, lambda current, total: update_progress(current, total))
    )
    thread_titles = threading.Thread(
        target=scrape_missing_titles,
        args=(all_urls, titles_output_text, lambda: stop_scraping, lambda current, total: update_progress(current, total))
    )

    thread_meta.daemon = True
    thread_404.daemon = True
    thread_titles.daemon = True
    thread_meta.start()
    thread_404.start()
    thread_titles.start()


def stop_scrape():
    """Stops the crawling process and resets the progress bar."""
    global stop_scraping
    stop_scraping = True
    reset_progress()


def export_missing_titles_gui():
    """Exports missing title data."""
    global missing_titles_data
    base_url = url_entry.get().strip()
    base_url = ensure_https(base_url)

    if not base_url or not missing_titles_data:
        messagebox.showerror("Error", "No data to export.")
        return

    export_missing_titles(missing_titles_data, base_url)


# Create the GUI window FIRST
root = tk.Tk()
root.title("SEO Analyzer")

# Progress tracking variable (must be created after root)
progress_var = tk.DoubleVar()

# URL input field
url_frame = tk.Frame(root)
url_frame.pack(padx=10, pady=10, fill=tk.X)

url_label = tk.Label(url_frame, text="Enter URL:")
url_label.pack(side=tk.LEFT, padx=5)

url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

start_button = tk.Button(url_frame, text="Start Crawling", command=start_crawling)
start_button.pack(side=tk.LEFT, padx=5)

# Progress Bar
progress_bar = ttk.Progressbar(url_frame, orient="horizontal", length=200, mode="determinate", variable=progress_var)
progress_bar.pack(side=tk.LEFT, padx=10)

# Tabbed areas for results
tab_control = ttk.Notebook(root)
tab_control.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)

# Meta Descriptions tab
meta_tab = ttk.Frame(tab_control)
tab_control.add(meta_tab, text="Meta Descriptions Missing")
meta_output_text = scrolledtext.ScrolledText(meta_tab, wrap=tk.WORD, height=20, width=80)
meta_output_text.pack(fill=tk.BOTH, expand=True)
export_meta_button = tk.Button(meta_tab, text="Export Meta Descriptions",
                               command=lambda: export_meta_descriptions(meta_output_text.get("1.0", tk.END).strip(),
                                                                        url_entry.get().strip()))
export_meta_button.pack(pady=5)

# 404 Errors tab
errors_tab = ttk.Frame(tab_control)
tab_control.add(errors_tab, text="404 Errors")
errors_output_text = scrolledtext.ScrolledText(errors_tab, wrap=tk.WORD, height=20, width=80)
errors_output_text.pack(fill=tk.BOTH, expand=True)
export_404_button = tk.Button(errors_tab, text="Export 404 Errors",
                              command=lambda: export_404_errors(errors_output_text.get("1.0", tk.END).strip(),
                                                                url_entry.get().strip()))
export_404_button.pack(pady=5)

# Missing Titles tab
titles_tab = ttk.Frame(tab_control)
tab_control.add(titles_tab, text="Missing Title Tags")
titles_output_text = scrolledtext.ScrolledText(titles_tab, wrap=tk.WORD, height=20, width=80)
titles_output_text.pack(fill=tk.BOTH, expand=True)
export_titles_button = tk.Button(titles_tab, text="Export Missing Titles", command=export_missing_titles_gui)
export_titles_button.pack(pady=5)

# Stop and Clear buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
stop_button = tk.Button(button_frame, text="Stop", command=stop_scrape, bg="red", fg="white")
stop_button.pack(side=tk.LEFT, padx=5)
clear_button = tk.Button(button_frame, text="Clear",
                         command=lambda: [meta_output_text.delete(1.0, tk.END), errors_output_text.delete(1.0, tk.END),
                                          titles_output_text.delete(1.0, tk.END)], bg="yellow")
clear_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
