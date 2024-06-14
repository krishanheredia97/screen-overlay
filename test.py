import sys
import cv2
import numpy as np
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QTimer
from pynput import mouse
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setMouseTracking(True)
        self.resize(800, 600)  # Adjust the size as necessary
        self.square_size = 20
        self.mouse_x = 0
        self.mouse_y = 0

        # Timer to update the position
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(10)  # Update every 10ms

    def update_position(self):
        self.move(self.mouse_x - self.square_size // 2, self.mouse_y - self.square_size // 2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(0, 255, 0, 128), 2, Qt.SolidLine))
        painter.drawRect(0, 0, self.square_size, self.square_size)


def on_move(x, y):
    global overlay
    overlay.mouse_x = x
    overlay.mouse_y = y


def on_click(x, y, button, pressed):
    if pressed:
        screenshot = pyautogui.screenshot(region=(
        x - overlay.square_size // 2 + 2, y - overlay.square_size // 2 + 2, overlay.square_size - 4,
        overlay.square_size - 4))
        screenshot.save('screenshot_temp.png')
        print(
            f"Screenshot taken for region: ({x - overlay.square_size // 2}, {y - overlay.square_size // 2}, {overlay.square_size}, {overlay.square_size})")

        # Update the Tkinter window with the screenshot
        update_screenshot()

        # Stop the overlay application
        QApplication.quit()


def update_screenshot():
    img = Image.open('screenshot_temp.png')
    img_tk = ImageTk.PhotoImage(img)
    screenshot_label.config(image=img_tk)
    screenshot_label.image = img_tk


def save_screenshot():
    img = Image.open('screenshot_temp.png')
    img.save('screenshot.png')
    print("Screenshot saved as screenshot.png")
    root.destroy()


def discard_screenshot():
    print("Screenshot discarded")
    root.destroy()


def run_overlay():
    global overlay
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()

    # Set up the mouse listeners
    listener_move = mouse.Listener(on_move=on_move)
    listener_click = mouse.Listener(on_click=on_click)
    listener_move.start()
    listener_click.start()

    app.exec_()

    listener_move.stop()
    listener_click.stop()


def main():
    global root, screenshot_label

    # Start the overlay in a separate thread
    overlay_thread = Thread(target=run_overlay)
    overlay_thread.start()

    # Set up the Tkinter window
    root = tk.Tk()
    root.title("Screenshot Preview")

    # Create an empty black image
    empty_img = Image.new('RGB', (20, 20), color='black')
    empty_img_tk = ImageTk.PhotoImage(empty_img)

    screenshot_label = tk.Label(root, image=empty_img_tk)
    screenshot_label.image = empty_img_tk
    screenshot_label.pack()

    save_button = tk.Button(root, text="Save", command=save_screenshot)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    discard_button = tk.Button(root, text="Discard", command=discard_screenshot)
    discard_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
