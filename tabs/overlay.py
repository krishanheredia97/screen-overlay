import tkinter as tk
from PIL import Image, ImageTk, PngImagePlugin
from pynput import mouse, keyboard
import pyautogui
import os
import random
import string
import json
import threading
import time


class Overlay:
    def __init__(self, parent, main_tab, screenshot_tab, settings):
        self.parent = parent
        self.main_tab = main_tab
        self.screenshot_tab = screenshot_tab
        self.overlay_root = None
        self.canvas = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.settings = settings
        self.width = settings['width']
        self.height = settings['height']
        self.multi_image_mode = False
        self.shutdown_timer = None

    def create_overlay(self):
        self.overlay_root = tk.Toplevel(self.parent)
        self.overlay_root.attributes("-fullscreen", True)
        self.overlay_root.attributes("-topmost", True)
        self.overlay_root.attributes("-alpha", 0.2)
        self.overlay_root.configure(bg='black')

        self.canvas = tk.Canvas(self.overlay_root, bg='gray', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Motion>", self.tk_on_move)
        self.canvas.bind("<Button-1>", self.tk_on_click)

    def run(self):
        self.create_overlay()
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.mouse_listener.start()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        self.start_shutdown_timer()

    def run_multi_image(self):
        self.multi_image_mode = True
        self.run()

    def on_move(self, x, y):
        if self.canvas is not None:
            self.canvas.delete("all")
            self.canvas.create_rectangle(x - self.width // 2, y - self.height // 2,
                                         x + self.width // 2, y + self.height // 2,
                                         outline='red', width=2)

    def tk_on_move(self, event):
        self.on_move(event.x, event.y)

    def on_click(self, x, y, button, pressed):
        if pressed:
            left = x - self.width // 2 + 1
            top = y - self.height // 2 + 1
            right = x + self.width // 2 - 1
            bottom = y + self.height // 2 - 1

            print(f"Coordinates: Top: {top}, Right: {right}, Left: {left}, Bottom: {bottom}")

            screenshot = pyautogui.screenshot(region=(left, top, self.width - 2, self.height - 2))

            if self.multi_image_mode:
                self.save_screenshot(screenshot)
            else:
                self.overlay_root.withdraw()
                screenshot.save('temp_screenshot.png')
                self.save_coordinates_metadata('temp_screenshot.png', left, top, right, bottom)
                self.update_screenshot('temp_screenshot.png')
                if self.mouse_listener:
                    self.mouse_listener.stop()
                if self.keyboard_listener:
                    self.keyboard_listener.stop()
                self.stop_shutdown_timer()

    def tk_on_click(self, event):
        self.on_click(event.x, event.y, None, True)

    def on_key_press(self, key):
        if key == keyboard.Key.tab:
            self.exit_program()

    def save_screenshot(self, screenshot):
        ss_dir_path = self.settings["ss_dir_path"]
        os.makedirs(ss_dir_path, exist_ok=True)
        filename = ''.join(random.choices(string.ascii_letters, k=5)) + ".png"
        img_path = os.path.join(ss_dir_path, filename)
        screenshot.save(img_path)
        print(f"Screenshot saved as {filename}")

    def discard_screenshot(self):
        if os.path.exists('temp_screenshot.png'):
            os.remove('temp_screenshot.png')
        print("Screenshot discarded")
        self.reset_view()

    def reset_view(self):
        self.screenshot_tab.lens_label.config(image='')
        self.screenshot_tab.zoom_label.config(image='')
        self.screenshot_tab.save_button.pack_forget()
        self.screenshot_tab.discard_button.pack_forget()

    def update_screenshot(self, path):
        img = Image.open(path)
        img_tk = ImageTk.PhotoImage(img)

        self.screenshot_tab.lens_label.config(image=img_tk)
        self.screenshot_tab.lens_label.image = img_tk

        zoomed_img = img.resize((self.width * 3, self.height * 3), Image.NEAREST)
        zoomed_img_tk = ImageTk.PhotoImage(zoomed_img)

        self.screenshot_tab.zoom_label.config(image=zoomed_img_tk)
        self.screenshot_tab.zoom_label.image = zoomed_img_tk

        self.show_save_discard_buttons()
        self.parent.notebook.select(self.screenshot_tab)

    def show_save_discard_buttons(self):
        self.screenshot_tab.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.screenshot_tab.discard_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def save_coordinates_metadata(self, path, left, top, right, bottom):
        img = Image.open(path)
        meta = PngImagePlugin.PngInfo()
        meta.add_text("coordinates", f"{left},{top},{right},{bottom}")
        img.save(path, pnginfo=meta)
        print(f"Coordinates saved in metadata: coordinates")

    def start_shutdown_timer(self):
        self.shutdown_timer = threading.Timer(60, self.exit_program)
        self.shutdown_timer.start()

    def stop_shutdown_timer(self):
        if self.shutdown_timer:
            self.shutdown_timer.cancel()

    def exit_program(self):
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.stop_shutdown_timer()
        if self.overlay_root:
            self.overlay_root.destroy()
        self.parent.quit()
