import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from meta_descriptions import scrape_meta_descriptions
from scrape_404_errors import scrape_404_errors
from utils import ensure_https, select_folder, create_new_folder

# Global variable to manage thread stopping
stop_scraping = False
output_folder = ""  # Folder selected by the user for CSV export

def select_folder_gui():
    global output_folder
    folder = select_folder()
    if folder:
        output_folder = folder
        folder_label.config(text=f"Selected Folder: {output_folder}")

def create_new_folder_gui():
    global output_folder
    folder = create_new_folder()
    if folder:
        output_folder = folder
        folder_label.config(text=f"Created and Selected Folder: {output_folder}")

def scrape_meta_descriptions_gui():
    global stop_scraping, output_folder
    base_url = url_entry.get().strip()
    base_url = ensure_https(base_url)

    if not base_url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    if not output_folder:
        messagebox.showerror("Error", "Please select or create a folder for exporting the CSV.")
        return

    output_text.delete(1.0, tk.END)
    stop_scraping = False

    # Pass output_folder to the scraping function
    thread = threading.Thread(target=scrape_meta_descriptions, args=(base_url, output_folder, output_text, lambda: stop_scraping))
    thread.daemon = True
    thread.start()

def scrape_404_errors_gui():
    global stop_scraping, output_folder
    base_url = url_entry.get().strip()
    base_url = ensure_https(base_url)

    if not base_url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    if not output_folder:
        messagebox.showerror("Error", "Please select or create a folder for exporting the CSV.")
        return

    output_text.delete(1.0, tk.END)
    stop_scraping = False

    # Pass output_folder to the scraping function
    thread = threading.Thread(target=scrape_404_errors, args=(base_url, output_folder, output_text, lambda: stop_scraping))
    thread.daemon = True
    thread.start()

def stop_scrape():
    global stop_scraping
    stop_scraping = True

def quit_app():
    root.quit()
    root.destroy()

# Create the GUI window
root = tk.Tk()
root.title("Meta Descriptions & 404 Errors Analyzer")

# Configure the grid layout to make widgets resize dynamically
root.rowconfigure(5, weight=1)  # Row for the output text
root.columnconfigure(0, weight=1)

# Input field and button for base URL
url_label = tk.Label(root, text="Enter Base URL:")
url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
scrape_meta_button = tk.Button(root, text="Scrape Meta Descriptions", command=scrape_meta_descriptions_gui)
scrape_meta_button.grid(row=0, column=2, padx=10, pady=5)
scrape_404_button = tk.Button(root, text="Scrape 404 Errors", command=scrape_404_errors_gui)
scrape_404_button.grid(row=1, column=2, padx=10, pady=5)

# Folder selection buttons
folder_label = tk.Label(root, text="No folder selected.")
folder_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
select_folder_button = tk.Button(root, text="Select Folder", command=select_folder_gui)
select_folder_button.grid(row=2, column=0, padx=10, pady=5, sticky="w")
create_folder_button = tk.Button(root, text="Create Folder", command=create_new_folder_gui)
create_folder_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Output text area for status and results
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80)
output_text.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_scrape, bg="red", fg="white")
stop_button.grid(row=6, column=0, padx=10, pady=5, sticky="w")

# Quit button
quit_button = tk.Button(root, text="Quit", command=quit_app, bg="red", fg="white")
quit_button.grid(row=6, column=1, padx=10, pady=5, sticky="w")

# Start the GUI loop
root.mainloop()