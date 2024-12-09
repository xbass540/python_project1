import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
import random

# Global variable to manage thread stopping
stop_scraping = False
output_folder = ""  # Folder selected by the user for CSV export

def select_folder():
    global output_folder
    folder = filedialog.askdirectory(
        title="Select Existing Folder for CSV Export"
    )
    if folder:
        output_folder = folder
        folder_label.config(text=f"Selected Folder: {output_folder}")

def create_new_folder():
    global output_folder
    folder = filedialog.asksaveasfilename(
        title="Create New Folder for CSV Export",
        initialfile="",
        filetypes=[("Folder", "*.folder")],
        defaultextension=".folder",
    )
    if folder:
        folder_path = os.path.splitext(folder)[0]  # Remove the dummy extension
        os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
        output_folder = folder_path
        folder_label.config(text=f"Created and Selected Folder: {output_folder}")

def scrape_website():
    global stop_scraping, output_folder
    base_url = url_entry.get().strip()  # Get URL from input field
    base_url = base_url.rstrip("/")  # Remove trailing slash if it exists
    if not base_url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    if not output_folder:
        messagebox.showerror("Error", "Please select or create a folder for exporting the CSV.")
        return

    # Clear the output area
    output_text.delete(1.0, tk.END)
    stop_scraping = False  # Reset the stop flag

    def scrape_process():
        global stop_scraping
        # Generate a random 4-digit number for the filename
        random_number = random.randint(1000, 9999)
        filename = f'{base_url[8:]}-{random_number}.csv'

        # Open CSV file and write headers
        csv_file = open(os.path.join(output_folder, filename), 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Post Name', 'Post URL', 'Meta Description', 'Posts with Issues'])

        visited_urls = set()  # Set to store visited URLs

        # Initialize counters
        article_counter = 1
        issues_counter = 0  # Counter for posts with issues

        def scrape_page(url):
            nonlocal article_counter, issues_counter  # Use nonlocal counters
            global stop_scraping

            if stop_scraping:
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
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                output_text.insert(tk.END, f"Failed to fetch {url}: {e}\n")
                output_text.see("end")
                return

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            output_text.insert(tk.END, f"Scraping URL: {url}\n")
            output_text.see("end")

            # Extract meta description from the page
            meta_description_tag = soup.find('meta', property="og:description")
            meta_description = meta_description_tag['content'].strip() if meta_description_tag and 'content' in meta_description_tag.attrs and meta_description_tag['content'] else "No description"

            # Count posts with no meta descriptions
            if meta_description == "No description":
                issues_counter += 1

            # Extract content of interest (customize based on website structure)
            for article in soup.find_all('article'):
                if stop_scraping:
                    output_text.insert(tk.END, "Scraping stopped by user.\n")
                    output_text.see("end")
                    return
                headline = article.find('h2').text.strip() if article.find('h2') else "No headline"
                article_url = article.find('a', href=True)
                if article_url:
                    full_url = urljoin(base_url, article_url['href'])  # Convert relative URL to absolute
                    article_info = f"# {article_counter}: {headline} \n URL: {full_url}\n Meta Description: {meta_description}\n\n"
                    output_text.insert(tk.END, article_info)
                    output_text.see("end")
                    csv_writer.writerow([headline, full_url, meta_description, issues_counter])  # Write to CSV
                    article_counter += 1  # Increment the article counter

            # Extract all links on the page
            for link in soup.find_all('a', href=True):
                if stop_scraping:
                    output_text.insert(tk.END, "Scraping stopped by user.\n")
                    output_text.see("end")
                    return
                full_url = urljoin(base_url, link['href'])  # Convert relative URL to absolute
                if base_url in full_url:  # Ensure the link is part of the same domain
                    scrape_page(full_url)  # Recursively scrape the next page

        # Start scraping from the homepage
        scrape_page(base_url)

        if not stop_scraping:
            # Write final count of posts with issues to the CSV file
            csv_writer.writerow(['', '', 'Total Posts with Issues:', issues_counter])
            output_text.insert(tk.END, f"\nScraping complete. Results saved to {os.path.join(output_folder, filename)}\n")
            output_text.see("end")
            messagebox.showinfo("Success", f"Scraping complete! Results saved to {os.path.join(output_folder, filename)}")

        # Close the CSV file
        csv_file.close()

    # Run the scraping process in a separate thread
    thread = threading.Thread(target=scrape_process)
    thread.daemon = True  # Ensure thread ends when the main program exits
    thread.start()

# Function to stop the scraping process
def stop_scrape():
    global stop_scraping
    stop_scraping = True

# Create the GUI window
root = tk.Tk()
root.title("Meta Descriptions Analyzer Website Scraper")

# Configure the grid layout to make widgets resize dynamically
root.rowconfigure(5, weight=1)  # Row for the output text
root.columnconfigure(0, weight=1)  # Column for all widgets

# Create and place the URL entry field
url_label = tk.Label(root, text="Enter Website URL:")
url_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

# Create and place the folder selection button
select_folder_button = tk.Button(root, text="Select Existing Folder", command=select_folder)
select_folder_button.grid(row=1, column=0, pady=10, padx=5)

# Create and place the folder creation button
create_folder_button = tk.Button(root, text="Create New Folder", command=create_new_folder)
create_folder_button.grid(row=1, column=1, pady=10, padx=5)

# Create and place the folder display label
folder_label = tk.Label(root, text="No folder selected", anchor="w")
folder_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10)

# Create and place the execute button
execute_button = tk.Button(root, text="Execute", command=scrape_website)
execute_button.grid(row=3, column=0, pady=10, padx=5)

# Create and place the stop button
stop_button = tk.Button(root, text="Stop", command=stop_scrape)
stop_button.grid(row=3, column=1, pady=10, padx=5)

# Create and place the output area
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_text.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Run the GUI event loop
root.mainloop()
