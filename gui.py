import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, filedialog
import threading
from meta_descriptions import scrape_meta_descriptions
from scrape_404_errors import scrape_404_errors
from missing_titles import scrape_missing_titles, export_missing_titles
from utils import ensure_https
import os
import random
from meta_descriptions import scrape_meta_descriptions, export_meta_descriptions
from scrape_404_errors import scrape_404_errors, export_404_errors


# Global variable to manage thread stopping
stop_scraping = False
missing_titles_data = []  # Store missing titles data


def start_crawling():
    global stop_scraping, missing_titles_data
    base_url = url_entry.get().strip()
    base_url = ensure_https(base_url)

    if not base_url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    # Clear output areas
    meta_output_text.delete(1.0, tk.END)
    errors_output_text.delete(1.0, tk.END)
    titles_output_text.delete(1.0, tk.END)  # Clear Missing Titles tab
    stop_scraping = False  # Reset stop flag before starting new crawl

    # Start meta descriptions scraping
    thread_meta = threading.Thread(
        target=scrape_meta_descriptions,
        args=(base_url, meta_output_text, lambda: stop_scraping)
    )
    thread_404 = threading.Thread(
        target=scrape_404_errors,
        args=(base_url, errors_output_text, lambda: stop_scraping)
    )

    # Start missing titles scraping
    def run_missing_titles():
        global missing_titles_data
        missing_titles_data = scrape_missing_titles(base_url, titles_output_text, lambda: stop_scraping)

    thread_titles = threading.Thread(target=run_missing_titles)

    # Run all threads
    thread_meta.daemon = True
    thread_404.daemon = True
    thread_titles.daemon = True
    thread_meta.start()
    thread_404.start()
    thread_titles.start()


def stop_scrape():
    global stop_scraping
    stop_scraping = True


def export_missing_titles_gui():
    global missing_titles_data
    base_url = url_entry.get().strip()
    base_url = ensure_https(base_url)

    if not base_url or not missing_titles_data:
        messagebox.showerror("Error", "No data to export.")
        return

    export_missing_titles(missing_titles_data, base_url)

def extract_data(text_widget):
    """Extracts text from a Tkinter ScrolledText widget and formats it into a list of lists for CSV export."""
    raw_text = text_widget.get("1.0", tk.END).strip()  # Get text from widget
    lines = raw_text.split("\n")  # Split into lines
    return [line.split("\t") for line in lines if line]  # Convert lines to lists

# Create the GUI window
root = tk.Tk()
root.title("SEO Analyzer")

# Configure the grid layout
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)

# URL input field
url_frame = tk.Frame(root)
url_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

url_label = tk.Label(url_frame, text="Enter URL:")
url_label.pack(side=tk.LEFT, padx=5)

url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

start_button = tk.Button(url_frame, text="Start Crawling", command=start_crawling)
start_button.pack(side=tk.LEFT, padx=5)

# Tabbed areas for results
tab_control = ttk.Notebook(root)
tab_control.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

# Meta Descriptions tab
meta_tab = ttk.Frame(tab_control)
tab_control.add(meta_tab, text="Meta Descriptions Missing")

meta_output_text = scrolledtext.ScrolledText(meta_tab, wrap=tk.WORD, height=20, width=80)
meta_output_text.pack(fill=tk.BOTH, expand=True)

export_meta_button = tk.Button(meta_tab, text="Export Meta Descriptions",
                               command=lambda: export_meta_descriptions(extract_data(meta_output_text), url_entry.get().strip()))

export_meta_button.pack(pady=5)


# 404 Errors tab
errors_tab = ttk.Frame(tab_control)
tab_control.add(errors_tab, text="404 Errors")

errors_output_text = scrolledtext.ScrolledText(errors_tab, wrap=tk.WORD, height=20, width=80)
errors_output_text.pack(fill=tk.BOTH, expand=True)

export_404_button = tk.Button(errors_tab, text="Export 404 Errors",
                              command=lambda: export_404_errors(extract_data(errors_output_text), url_entry.get().strip()))

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
button_frame.grid(row=2, column=0, columnspan=3, pady=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_scrape, bg="red", fg="white")
stop_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=lambda: [meta_output_text.delete(1.0, tk.END),
                     errors_output_text.delete(1.0, tk.END),
                     titles_output_text.delete(1.0, tk.END)],
    bg="yellow"
)
clear_button.pack(side=tk.LEFT, padx=5)

# Start the GUI loop
root.mainloop()
