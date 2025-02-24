import logging
from pynput import keyboard, mouse
import threading
import time
from collections import Counter
import PieGraph as Pg
import tkinter as tk
from tkinter import scrolledtext, ttk
import queue


logging.basicConfig(filename="interruptions.log", level=logging.INFO, format="%(asctime)s - %(message)s")


interruptions_count = 0

threshold = 10


event_counter = Counter({"Key Pressed": 0, "Mouse Clicked": 0, "Mouse Scrolled": 0})


log_queue = queue.Queue()


def log_interruption(event_type, event_details):
    global interruptions_count
    interruptions_count += 1
    event_counter[event_type] += 1
    logging.info(f"{event_type}: {event_details}")

    if interruptions_count > threshold:
        print("Pie chart created, you reached limit of interruption")
        Pg.create_pie_chart(event_counter)
        root.quit()

    root.after(0, update_event_counter_display)


def log_to_gui(message):
    log_textbox.config(state=tk.NORMAL)
    log_textbox.insert(tk.END, message + "\n")
    log_textbox.config(state=tk.DISABLED)
    log_textbox.yview(tk.END)


def update_event_counter_display():
    key_pressed_label.config(text=f"Key Pressed: {event_counter['Key Pressed']}")
    mouse_clicked_label.config(text=f"Mouse Clicked: {event_counter['Mouse Clicked']}")
    mouse_scrolled_label.config(text=f"Mouse Scrolled: {event_counter['Mouse Scrolled']}")


def on_press(key):
    try:
        log_interruption("Key Pressed", f"{key.char}")
    except AttributeError:
        log_interruption("Key Pressed", f"{key}")


def on_click(x, y, button, pressed):
    if pressed:
        log_interruption("Mouse Clicked", f"Button {button} at ({x}, {y})")


def on_scroll(x, y, dx, dy):
    log_interruption("Mouse Scrolled", f"Scrolled {'down' if dy < 0 else 'up'} at ({x}, {y})")


def monitor_log_file():
    try:
        with open("interruptions.log", "r") as file:
            file.seek(0, 2)
            while True:
                line = file.readline()
                if line:
                    log_queue.put(line.strip())
                else:
                    time.sleep(0.1)
    except Exception as e:
        print(f"Error in monitor_log_file: {e}")


def process_log_queue():
    while not log_queue.empty():
        log_to_gui(log_queue.get())
    root.after(100, process_log_queue)


def generate_pie_chart():
    try:
        root.quit()
        time.sleep(0.5)
        Pg.create_pie_chart(event_counter)
        print("Pie chart generated.")
    except Exception as e:
        print(f"Error in generate_pie_chart: {e}")



root = tk.Tk()
root.title("Interruptions Monitor")
root.geometry("1920x1080")
root.configure(bg="#336699")

title_label = tk.Label(root, text="Interruptions Monitor", font=("Helvetica", 40, "bold"), bg="#336699",
                       fg="white")
title_label.pack(pady=10)

log_textbox = scrolledtext.ScrolledText(root, width=100, height=15, state=tk.DISABLED, font=("Consolas", 20),
                                        bg="floralwhite")
log_textbox.pack(pady=10)

event_frame = tk.Frame(root, bg="#336699")
event_frame.pack(pady=10)

key_pressed_label = tk.Label(event_frame, text="Key Pressed: 0", font=("Helvetica", 25, "bold"), bg="#336699",
                             fg="white")
key_pressed_label.grid(row=0, column=0, padx=10, pady=5)

mouse_clicked_label = tk.Label(event_frame, text="Mouse Clicked: 0", font=("Helvetica", 25, "bold"), bg="#336699",
                               fg="white")
mouse_clicked_label.grid(row=0, column=1, padx=10, pady=5)

mouse_scrolled_label = tk.Label(event_frame, text="Mouse Scrolled: 0", font=("Helvetica", 25, "bold"), bg="#336699",
                                fg="white")
mouse_scrolled_label.grid(row=0, column=2, padx=10, pady=5)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14, "bold"), padding=10, background="#336699",
                foreground="#767676")


style.configure("TButton", font=("Helvetica", 40), padding=(4, 5), background="#336699", foreground="white",
                borderwidth=0)

generate_button = ttk.Button(root, text="Generate Graph", command=generate_pie_chart, style="TButton")
generate_button.pack(pady=20)


log_monitor_thread = threading.Thread(target=monitor_log_file)
log_monitor_thread.daemon = True
log_monitor_thread.start()


keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)


keyboard_listener.start()
mouse_listener.start()


root.after(100, process_log_queue)

root.mainloop()

