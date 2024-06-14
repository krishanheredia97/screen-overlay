import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pynput import mouse
import pyautogui
import os
import random
import string
import json

class Overlay:
    def __init__(self, parent, main_tab):
        self.parent = parent
        self.main_tab = main_tab
        self.square_size = 20
        self.overlay_root = None
        self.canvas = None
        self.listener = None

    def create_overlay(self):
        self.overlay_root = tk.Toplevel(self.parent)
        self.overlay_root.attributes("-fullscreen", True)
        self.overlay_root.attributes("-alpha", 0.3)
        self.overlay_root.attributes("-topmost", True)
        self.overlay_root.configure(bg='black')

        self.canvas = tk.Canvas(self.overlay_root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Motion>", self.tk_on_move)
        self.canvas.bind("<Button-1>", self.tk_on_click)

    def run(self):
        self.create_overlay()
        self.listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.listener.start()

    def on_move(self, x, y):
        if self.canvas is not None:
            self.canvas.delete("all")
            self.canvas.create_rectangle(x - self.square_size // 2, y - self.square_size // 2,
                                         x + self.square_size // 2, y + self.square_size // 2,
                                         outline='green', width=2)

    def tk_on_move(self, event):
        self.on_move(event.x, event.y)

    def on_click(self, x, y, button, pressed):
        if pressed:
            screenshot = pyautogui.screenshot(region=(
                x - self.square_size // 2, y - self.square_size // 2, self.square_size, self.square_size))
            screenshot.save('screenshot_temp.png')
            self.update_screenshot('screenshot_temp.png')
            self.overlay_root.withdraw()  # Hide the overlay after taking a screenshot
            if self.listener:
                self.listener.stop()

    def tk_on_click(self, event):
        self.on_click(event.x, event.y, None, True)

    def update_screenshot(self, path):
        img = Image.open(path)
        img_tk = ImageTk.PhotoImage(img)

        self.main_tab.lens_label.config(image=img_tk)
        self.main_tab.lens_label.image = img_tk

        zoomed_img = img.resize((self.square_size * 3, self.square_size * 3), Image.NEAREST)
        zoomed_img_tk = ImageTk.PhotoImage(zoomed_img)

        self.main_tab.zoom_label.config(image=zoomed_img_tk)
        self.main_tab.zoom_label.image = zoomed_img_tk

        self.show_save_discard_buttons()

    def show_save_discard_buttons(self):
        self.main_tab.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.main_tab.discard_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def save_screenshot(self):
        settings = self.load_settings()
        if not settings:
            return

        ss_dir_path = settings["ss_dir_path"]
        os.makedirs(ss_dir_path, exist_ok=True)
        filename = ''.join(random.choices(string.ascii_letters, k=5)) + ".png"
        img_path = os.path.join(ss_dir_path, filename)

        img = Image.open('screenshot_temp.png')
        img.save(img_path)
        messagebox.showinfo("Success", f"Screenshot saved as {filename}")
        self.reset_view()

    def discard_screenshot(self):
        messagebox.showinfo("Info", "Screenshot discarded")
        self.reset_view()

    def reset_view(self):
        self.main_tab.lens_label.config(image='')
        self.main_tab.zoom_label.config(image='')
        self.main_tab.save_button.pack_forget()
        self.main_tab.discard_button.pack_forget()

    def load_settings(self):
        try:
            path = r"C:\Users\danie\PycharmProjects\screenshots\tk_settings\settings.json"
            with open(path, 'r') as json_file:
                settings = json.load(json_file)
            return settings
        except Exception as e:
            print(f"Failed to load settings: {e}")
            return None
