import tkinter as tk
from tkinter import ttk
import json

class MainTab(ttk.Frame):
    def __init__(self, parent, overlay):
        super().__init__(parent)
        self.overlay = overlay

        # Create the Start button
        self.start_button = tk.Button(self, text="Start", command=self.start_overlay)
        self.start_button.pack(pady=10)

        # Create the Multi-image button
        self.multi_image_button = tk.Button(self, text="Multi-image", command=self.start_multi_image)
        self.multi_image_button.pack(pady=10)

        # Create the Coordinates button
        self.coordinates_button = tk.Button(self, text="Coordinates", command=self.show_coordinates)
        self.coordinates_button.pack(pady=10)

        # Create the Exit button
        self.exit_button = tk.Button(self, text="Exit", command=self.exit_program)
        self.exit_button.pack(side=tk.BOTTOM, pady=10)

    def start_overlay(self):
        settings = self.load_settings()
        if settings:
            self.overlay.square_size = settings['width']  # Set the overlay square size based on settings
            self.overlay.run()
        else:
            tk.messagebox.showerror("Error", "Failed to load settings.")

    def start_multi_image(self):
        settings = self.load_settings()
        if settings:
            self.overlay.square_size = settings['width']  # Set the overlay square size based on settings
            self.overlay.run_multi_image()
        else:
            tk.messagebox.showerror("Error", "Failed to load settings.")

    def show_coordinates(self):
        pass  # Placeholder for future functionality

    def exit_program(self):
        self.quit()

    def load_settings(self):
        try:
            path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings\settings.json"
            with open(path, 'r') as json_file:
                settings = json.load(json_file)
            return settings
        except Exception as e:
            print(f"Failed to load settings: {e}")
            return None