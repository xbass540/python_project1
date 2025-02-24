import tkinter as tk
from tkinter import ttk

class CrawlProgressBar:
    def __init__(self, parent):
        """Creates a progress bar inside the given parent widget."""
        self.progress = ttk.Progressbar(parent, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(side=tk.LEFT, padx=10)  # Place it to the right of the Start button

    def update_progress(self, value):
        """Updates the progress bar value."""
        self.progress["value"] = value  # Set the progress value

    def reset_progress(self):
        """Resets the progress bar to 0."""
        self.progress["value"] = 0
