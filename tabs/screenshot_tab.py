import tkinter as tk
from tkinter import ttk
import json
from PIL import Image, ImageTk


class ScreenshotTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.overlay = None

        # Create and place the Lens section
        self.lens_label = tk.Label(self)
        self.lens_label.pack(pady=5)

        # Add a dividing line
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)

        # Create and place the Zoom section
        self.zoom_label = tk.Label(self)
        self.zoom_label.pack(pady=5)

        # Create a frame for buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        # Save and Discard buttons will be created when set_overlay is called

    def set_overlay(self, overlay):
        self.overlay = overlay
        self.create_buttons()

    def create_buttons(self):
        # Create Save and Discard buttons
        self.save_button = tk.Button(self.button_frame, text="Save", command=self.overlay.save_screenshot)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.discard_button = tk.Button(self.button_frame, text="Discard", command=self.overlay.discard_screenshot)
        self.discard_button.pack(side=tk.RIGHT, padx=5)

    def load_settings(self):
        try:
            path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings\settings.json"
            with open(path, 'r') as json_file:
                settings = json.load(json_file)
            return settings
        except Exception as e:
            print(f"Failed to load settings: {e}")
            return None