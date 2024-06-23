import tkinter as tk
from tkinter import ttk
import json
from tabs.settings_tab import SettingsTab
from tabs.main_tab import MainTab
from tabs.screenshot_tab import ScreenshotTab
from tabs.overlay import Overlay

def load_settings():
    try:
        path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings\settings.json"
        with open(path, 'r') as json_file:
            settings = json.load(json_file)
        return settings
    except Exception as e:
        print(f"Failed to load settings: {e}")
        return None

class MainDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Dashboard")

        # Load settings
        self.settings = load_settings()

        # Create a Notebook widget
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs first
        self.main_tab = MainTab(self.notebook, None)  # Pass None for overlay initially
        self.screenshot_tab = ScreenshotTab(self.notebook)  # Don't pass overlay here

        # Initialize Overlay with all necessary parameters
        self.overlay = Overlay(self, self.main_tab, self.screenshot_tab, self.settings)

        # Update tabs with the correct overlay instance
        self.main_tab.overlay = self.overlay
        self.screenshot_tab.set_overlay(self.overlay)  # Use the new set_overlay method

        # Add tabs to notebook
        self.notebook.add(self.main_tab, text="Main")
        self.notebook.add(self.screenshot_tab, text="Screenshot")

        # Add the Settings tab
        settings_tab = SettingsTab(self.notebook)
        self.notebook.add(settings_tab, text="Settings")

        # Display current settings
        self.settings_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.settings_label.pack(pady=10)

        self.update_dashboard_from_settings()

    def update_dashboard_from_settings(self):
        if self.settings:
            self.update_dashboard(
                self.settings['window'],
                self.settings['width'],
                self.settings['height']
            )

    def update_dashboard(self, window_name, width, height):
        self.settings_label.config(text=f"Current Settings: {window_name} ({width}x{height})")

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()
