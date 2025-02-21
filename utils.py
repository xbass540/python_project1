import os
import tkinter as tk
from tkinter import filedialog

def ensure_https(url):
    """Ensure the URL starts with 'https://' or 'http://'."""
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url

def select_folder():
    """Open a dialog to select an existing folder."""
    folder = filedialog.askdirectory(title="Select Existing Folder for CSV Export")
    return folder

def create_new_folder():
    """Open a dialog to create a new folder."""
    folder = filedialog.asksaveasfilename(
        title="Create New Folder for CSV Export",
        initialfile="",
        filetypes=[("Folder", "*.folder")],
        defaultextension=".folder",
    )
    if folder:
        folder_path = os.path.splitext(folder)[0]  # Remove the dummy extension
        os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
        return folder_path
    return None