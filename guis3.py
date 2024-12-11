import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()

# Set the title of the window
root.title("Simple App")

# Define the function to add text from the entry field to the listbox
def add_to_list(event=None, entry_widget=None, listbox_widget=None):
    if entry_widget and listbox_widget:
        text = entry_widget.get()  # Get the text from the specified entry widget
        if text:  # If the text is not empty
            listbox_widget.insert(tk.END, text)  # Insert the text at the end of the specified listbox
            entry_widget.delete(0, tk.END)  # Clear the text in the entry widget

# Configure the root window to make it responsive
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# Create the first frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)  # Place the frame in the main window and make it responsive

# Configure the first frame to make it responsive
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)

# Create an entry widget for user input in the first frame
entry = ttk.Entry(frame)
entry.grid(row=0, column=0, sticky="ew")  # Place the entry widget in the frame

entry.bind("<Return>", lambda event: add_to_list(event, entry, text_list))

# Create a button that triggers the add_to_list function in the first frame
entry_btn = ttk.Button(frame, text='Add', command=lambda: add_to_list(None, entry, text_list))
entry_btn.grid(row=0, column=1)  # Place the button next to the entry widget

# Create a listbox to display the list of items added in the first frame
text_list = tk.Listbox(frame)
text_list.grid(row=1, column=0, columnspan=2, sticky="nsew")  # Span the listbox across two columns and make it sticky

# Create the second frame
frame2 = tk.Frame(root)
frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)  # Place the frame in the main window and make it responsive

# Configure the second frame to make it responsive
frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(1, weight=1)

# Create an entry widget for user input in the second frame
entry2 = tk.Entry(frame2)
entry2.grid(row=0, column=0, sticky="ew")  # Place the entry widget in the frame

entry2.bind("<Return>", lambda event: add_to_list(event, entry2, text_list2))

# Create a button that triggers the add_to_list function in the second frame
entry_btn2 = tk.Button(frame2, text='Add', command=lambda: add_to_list(None, entry2, text_list2))
entry_btn2.grid(row=0, column=1)  # Place the button next to the entry widget

# Create a listbox to display the list of items added in the second frame
text_list2 = tk.Listbox(frame2)
text_list2.grid(row=1, column=0, columnspan=2, sticky="nsew")  # Span the listbox across two columns and make it sticky

# Run the Tkinter event loop
root.mainloop()
