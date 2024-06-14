import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class SettingsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create and place the size label and entry
        tk.Label(self, text="Size (WxH):").grid(row=0, column=0, padx=10, pady=10)
        self.size_entry = tk.Entry(self)
        self.size_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create and place the window label and entry
        tk.Label(self, text="Window Name:").grid(row=1, column=0, padx=10, pady=10)
        self.window_entry = tk.Entry(self)
        self.window_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create and place the save button
        save_button = tk.Button(self, text="Save", command=self.save_settings)
        save_button.grid(row=2, column=0, padx=10, pady=10)

        # Create and place the save as template button
        save_template_button = tk.Button(self, text="Save as Template", command=self.open_template_window)
        save_template_button.grid(row=2, column=1, padx=10, pady=10)

        # Create and place the see templates button
        see_templates_button = tk.Button(self, text="See Templates", command=self.see_templates)
        see_templates_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def save_settings(self):
        size = self.size_entry.get()
        window_name = self.window_entry.get()

        try:
            w, h = map(int, size.split('x'))  # Split and convert to integers
        except ValueError:
            messagebox.showerror("Input Error", "Size must be in the format WxH, e.g., 21x30")
            return

        # Define the path for the screenshot directory
        base_ss_dir = r"C:\Users\danie\PycharmProjects\screenshots\screenshots"
        ss_dir_path = os.path.join(base_ss_dir, window_name)
        os.makedirs(ss_dir_path, exist_ok=True)  # Ensure the directory exists

        settings = {
            "width": w,
            "height": h,
            "window": window_name,
            "ss_dir_path": ss_dir_path
        }

        # Define the path for the JSON file
        json_path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings\settings.json"

        with open(json_path, 'w') as json_file:
            json.dump(settings, json_file)

        messagebox.showinfo("Success", "Settings saved successfully!")
        self.update_main_dashboard()

    def open_template_window(self):
        template_window = tk.Toplevel(self)
        template_window.title("Save as Template")

        tk.Label(template_window, text="Template Name:").grid(row=0, column=0, padx=10, pady=10)
        template_name_entry = tk.Entry(template_window)
        template_name_entry.grid(row=0, column=1, padx=10, pady=10)

        def save_template():
            template_name = template_name_entry.get()
            if not template_name:
                messagebox.showerror("Input Error", "Template name cannot be empty")
                return

            size = self.size_entry.get()
            window_name = self.window_entry.get()

            try:
                w, h = map(int, size.split('x'))  # Split and convert to integers
            except ValueError:
                messagebox.showerror("Input Error", "Size must be in the format WxH, e.g., 21x30")
                return

            # Define the path for the screenshot directory
            base_ss_dir = r"C:\Users\danie\PycharmProjects\screenshots\screenshots"
            ss_dir_path = os.path.join(base_ss_dir, window_name)
            os.makedirs(ss_dir_path, exist_ok=True)  # Ensure the directory exists

            settings = {
                "width": w,
                "height": h,
                "window": window_name,
                "ss_dir_path": ss_dir_path
            }

            # Define the path for the template JSON file
            path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings"
            os.makedirs(path, exist_ok=True)  # Ensure the directory exists

            template_json_path = os.path.join(path, f"{template_name}.json")

            with open(template_json_path, 'w') as json_file:
                json.dump(settings, json_file)

            messagebox.showinfo("Success", f"Template '{template_name}' saved successfully!")

            # Copy the template JSON to settings.json
            settings_json_path = os.path.join(path, "settings.json")

            with open(settings_json_path, 'w') as json_file:
                json.dump(settings, json_file)

            self.update_main_dashboard()
            template_window.destroy()

        tk.Button(template_window, text="Save", command=save_template).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(template_window, text="Cancel", command=template_window.destroy).grid(row=1, column=1, padx=10, pady=10)

    def see_templates(self):
        templates_window = tk.Toplevel(self)
        templates_window.title("Templates")

        path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings"
        files = [f for f in os.listdir(path) if f.endswith('.json') and f != 'settings.json']

        row = 0
        for file in files:
            with open(os.path.join(path, file), 'r') as json_file:
                data = json.load(json_file)
                template_name = file.replace('.json', '')
                tk.Label(templates_window, text=f"{template_name}: {data['window']} ({data['width']}x{data['height']})").grid(row=row, column=0, padx=10, pady=5)
                check_button = tk.Button(templates_window, text="Select", command=lambda f=file: self.select_template(f))
                check_button.grid(row=row, column=1, padx=10, pady=5)
                row += 1

    def select_template(self, template_file):
        path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings"
        template_json_path = os.path.join(path, template_file)
        settings_json_path = os.path.join(path, "settings.json")

        with open(template_json_path, 'r') as json_file:
            settings = json.load(json_file)

        with open(settings_json_path, 'w') as json_file:
            json.dump(settings, json_file)

        messagebox.showinfo("Success", f"Settings changed to {template_file.replace('.json', '')}!")
        self.update_main_dashboard()

    def update_main_dashboard(self):
        try:
            path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings\settings.json"
            with open(path, 'r') as json_file:
                settings = json.load(json_file)
            self.master.update_dashboard(settings['window'], settings['width'], settings['height'])
        except Exception as e:
            print(f"Failed to update main dashboard: {e}")
