import tkinter as tk
from tkinter import ttk
import json
from PIL import Image, ImageTk

class MainTab(ttk.Frame):
    def __init__(self, parent, overlay):
        super().__init__(parent)
        self.overlay = overlay

        # Load current settings from settings.json
        settings = self.load_settings()
        if not settings:
            settings = {"width": 100, "height": 100}  # Default size if settings can't be loaded

        self.width = settings["width"]
        self.height = settings["height"]

        # Create the Start button
        self.start_button = tk.Button(self, text="Start", command=self.start_overlay)
        self.start_button.pack(pady=10)

        # Create and place the Lens section
        lens_label = tk.Label(self, text="Lens", font=("Helvetica", 12))
        lens_label.pack(pady=5)
        self.lens_label = tk.Label(self, width=self.width, height=self.height, bg='black')
        self.lens_label.pack(pady=5)
        self.lens_label.pack_propagate(False)  # Prevent the frame from resizing to fit the content

        # Add a dividing line
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)

        # Create and place the Zoom section
        zoom_label = tk.Label(self, text="Zoom", font=("Helvetica", 12))
        zoom_label.pack(pady=5)
        self.zoom_label = tk.Label(self, width=self.width * 3, height=self.height * 3, bg='black')
        self.zoom_label.pack(pady=5)
        self.zoom_label.pack_propagate(False)  # Prevent the frame from resizing to fit the content

        # Create Save and Discard buttons
        self.save_button = tk.Button(self, text="Save", command=self.overlay.save_screenshot)
        self.discard_button = tk.Button(self, text="Discard", command=self.overlay.discard_screenshot)

    def start_overlay(self):
        self.overlay.square_size = self.width  # Set the overlay square size based on settings
        self.overlay.run()

    def load_settings(self):
        try:
            path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings\settings.json"
            with open(path, 'r') as json_file:
                settings = json.load(json_file)
            return settings
        except Exception as e:
            print(f"Failed to load settings: {e}")
            return None
