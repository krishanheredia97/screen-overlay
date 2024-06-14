import tkinter as tk
from tkinter import ttk
from tabs.settings_tab import SettingsTab
from tabs.main_tab import MainTab
from tabs.overlay import Overlay
import json

class MainDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Dashboard")

        # Create a Notebook widget
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')

        # Initialize Overlay
        self.overlay = Overlay(self, main_tab=None)

        # Add the Main tab first
        self.main_tab = MainTab(notebook, self.overlay)
        self.overlay.main_tab = self.main_tab
        notebook.add(self.main_tab, text="Main")

        # Add the Settings tab
        settings_tab = SettingsTab(notebook)
        notebook.add(settings_tab, text="Settings")

        # Display current settings
        self.settings_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.settings_label.pack(pady=10)

        self.update_dashboard_from_file()

    def update_dashboard_from_file(self):
        try:
            path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings\settings.json"
            with open(path, 'r') as json_file:
                settings = json.load(json_file)
            self.update_dashboard(settings['window'], settings['width'], settings['height'])
            self.main_tab.lens_label.config(width=settings['width'], height=settings['height'])
            self.main_tab.zoom_label.config(width=settings['width'] * 3, height=settings['height'] * 3)
        except Exception as e:
            print(f"Failed to load settings: {e}")

    def update_dashboard(self, window_name, width, height):
        self.settings_label.config(text=f"Current Settings: {window_name} ({width}x{height})")

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()
