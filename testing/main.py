import tkinter as tk
from PIL import ImageGrab, ImageTk
import win32gui
import win32con
import time


def show_window_screenshot(handle):
    # Bring the window to the foreground
    win32gui.ShowWindow(handle, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(handle)

    # Wait for 2 seconds to ensure the window is visible
    time.sleep(2)

    # Get the bounding box of the window using the handle
    def get_window_rect(handle):
        rect = win32gui.GetWindowRect(handle)
        return rect

    bbox = get_window_rect(handle)

    # Capture the screenshot
    screenshot = ImageGrab.grab(bbox)

    # Create a Tkinter window to display the screenshot
    root = tk.Tk()
    root.title(f"Screenshot of Window Handle: {handle}")

    # Convert the screenshot to a format Tkinter can display
    img = ImageTk.PhotoImage(screenshot)

    # Create a label widget to hold the image
    label = tk.Label(root, image=img)
    label.pack()

    # Run the Tkinter event loop
    root.mainloop()


# Specify the window handle (as an integer)
window_handle = 197994  # Replace this with the actual window handle
show_window_screenshot(window_handle)
