#!/usr/bin/env python3


import tkinter as tk
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Since Start")
        
        self.maximize_window_compatible()

        self.start_time = datetime.now()

        self.label = tk.Label(self.root, text="", font=("Helvetica", 48))
        self.label.pack(expand=True)

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

    def update_clock(self):
        now = datetime.now()
        elapsed = now - self.start_time
        # Format elapsed time to include hours, minutes, seconds, and milliseconds
        elapsed_str = '{:02d}:{:02d}:{:02d}.{:01d}'.format(
            elapsed.seconds // 3600,
            (elapsed.seconds // 60) % 60,
            elapsed.seconds % 60,
            round(elapsed.microseconds // 100000, 1))
        self.label.config(text=elapsed_str)
        self.root.after(50, self.update_clock)  # Refresh more frequently for millisecond resolution

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
