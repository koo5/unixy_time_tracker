#!/usr/bin/env python3
import threading
import tkinter as tk
from datetime import datetime
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Countup Timer")
        
        self.maximize_window_compatible()

        self.start_time = datetime.now()
        self.running = True  # Keep track of whether the timer is running
        self.paused = False  # Additional state to handle the pause correctly
        self.previous_second = 0  # To keep track of the last spoken second

        self.label = tk.Label(self.root, text="", font=("Helvetica", 48))
        self.label.pack(expand=True)

        # Ensure the root window can capture key events
        self.root.focus_set()
        self.root.bind('<Escape>', self.toggle_counting)  # Bind Escape key to toggle counting
        self.speaks=[]
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
            self.root.geometry(f"{width}x{height}+100+0")

    def toggle_counting(self, event=None):
        if self.running:
            self.running = False
            self.paused = True
            self.speak_elapsed_time_with_millis()
        else:
            if self.paused:
                self.paused = False
                self.running = True
                self.start_time = datetime.now() - self.elapsed  # Reset start time to account for paused duration
                self.update_clock()
            else:
                self.root.destroy()  # Exit app if Escape is pressed again after resuming

    def speak_elapsed_time(self, seconds):
        # Speak the elapsed time if a new second has passed
        if seconds != self.previous_second:
            thread = threading.Thread(target=self.speak_elapsed_time_thread, args=(seconds,))
            thread.start()
            self.speaks.append(thread)
            
            self.previous_second = seconds
    
    def speak_elapsed_time_thread(self, seconds):
        os.system(f'espeak "{seconds} seconds"')
        self.speaks.remove(threading.current_thread())

    def speak_elapsed_time_with_millis(self):
        seconds = self.elapsed.seconds
        millis = self.elapsed.microseconds // 1000
        for t in self.speaks:
        	t.join()
        os.system(f'espeak "{seconds} seconds, {millis} milliseconds"&')


    def update_clock(self):
        if self.running:
            now = datetime.now()
            self.elapsed = now - self.start_time
            seconds = self.elapsed.seconds
            # Format elapsed time to include hours, minutes, seconds, and tenths of seconds
            elapsed_str = '{:02d}:{:02d}:{:02d}.{:03d}'.format(
                seconds // 3600,
                (seconds // 60) % 60,
                seconds % 60,
                self.elapsed.microseconds // 1000)
            self.label.config(text=elapsed_str)
            self.speak_elapsed_time(seconds)
            self.root.after(100, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
