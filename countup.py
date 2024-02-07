#!/usr/bin/env python3

import tkinter as tk
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Since Start")
        
        self.maximize_window_compatible()

        self.start_time = datetime.now()
        self.running = True  # Keep track of whether the timer is running
        self.paused = False  # Additional state to handle the pause correctly

        self.label = tk.Label(self.root, text="", font=("Helvetica", 48))
        self.label.pack(expand=True)

        # Ensure the root window can capture key events
        self.root.focus_set()
        self.root.bind('<Escape>', self.toggle_counting)  # Bind Escape key to toggle counting

        self.update_clock()

    def maximize_window_compatible(self):
        try:
            self.root.state('zoomed')  # This works on Windows
        except tk.TclError:
            self.root.attributes('-zoomed', True)  # For Linux
        except:
            # Fallback method: manually setting window size to screen size
            width = self.root.winfo_screenwidth()
            height = self.root.winfo_screenheight()
            self.root.geometry(f"{width}x{height}+0+0")

    def toggle_counting(self, event=None):
        if self.running:
            self.running = False
            self.paused = True
        else:
            if self.paused:
                self.paused = False
                self.running = True
                self.start_time = datetime.now() - self.elapsed  # Reset start time to account for paused duration
                self.update_clock()
            else:
                self.root.destroy()  # Exit app if Escape is pressed again after resuming

    def update_clock(self):
        if self.running:
            now = datetime.now()
            self.elapsed = now - self.start_time
            # Format elapsed time to include hours, minutes, seconds, and tenths of seconds
            elapsed_str = '{:02d}:{:02d}:{:02d}.{:02d}'.format(
                self.elapsed.seconds // 3600,
                (self.elapsed.seconds // 60) % 60,
                self.elapsed.seconds % 60,
                self.elapsed.microseconds // 10000)
            self.label.config(text=elapsed_str)
            self.root.after(55, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()