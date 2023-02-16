import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import urllib.request
import os

class ImageDownloader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Prefix dropdown menu
        self.prefix_label = tk.Label(self, text="Select prefix:")
        self.prefix_label.pack()
        self.prefix_var = tk.StringVar(value="CH")
        self.prefix_dropdown = ttk.Combobox(self, textvariable=self.prefix_var, values=["CH", "TB", "DK","LC"])
        self.prefix_dropdown.pack()

        # Image URL label and entry box
        self.url_label = tk.Label(self, text="Enter image URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self)
        self.url_entry.pack()

        # Output folder label and browse button
        self.output_label = tk.Label(self, text="Select output folder:")
        self.output_label.pack()
        self.output_folder = tk.StringVar(value="")
        self.output_entry = tk.Entry(self, textvariable=self.output_folder)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.browse_button = tk.Button(self, text="Browse", command=self.select_output_folder)
        self.browse_button.pack(side=tk.LEFT)

        # Download button
        self.download_button = tk.Button(self, text="Download", command=self.download_image)
        self.download_button.pack()

    def select_output_folder(self):
        # Show file dialog to select output folder
        folder_path = filedialog.askdirectory()
        self.output_folder.set(folder_path)

    def download_image(self):
        # Retrieve image from URL
        url = self.url_entry.get()
        with urllib.request.urlopen(url) as u:
            img_data = u.read()

        # Find next sequential suffix number
        prefix = self.prefix_var.get()
        output_path = self.output_folder.get()
        max_num = 0
        for filename in os.listdir(output_path):
            if filename.endswith(".jpg") and filename.startswith(prefix):
                num = int(filename.split("_")[1].split(".")[0])
                max_num = max(max_num, num)
        suffix = str(max_num + 1).zfill(3)

        # Save image to file
        filename = "{}_{}.jpg".format(prefix, suffix)
        filepath = os.path.join(output_path, filename)
        with open(filepath, "wb") as f:
            f.write(img_data)

        # Reset URL entry box
        self.url_entry.delete(0, tk.END)

# Create Tkinter window and run app
root = tk.Tk()
app = ImageDownloader(master=root)
app.mainloop()
