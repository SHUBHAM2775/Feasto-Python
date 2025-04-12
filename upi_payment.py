import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import sys

def open_upi_payment_window():
    win = tk.Tk()
    win.title("Feasto: UPI Payment")
    win.state('zoomed')

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Load background image
    bg_image = Image.open("images/restobg3.png")
    bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(win, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Title
    canvas.create_text(screen_width // 2, 80, text="Select UPI App",
                       font=("Arial", 35, "bold"), fill="white")

    # Grey semi-transparent box
    canvas.create_rectangle(250, 150, 1300, 600,
                            fill="grey", stipple='gray50')

    # Load and resize UPI app logos
    def load_logo(path, size=(180, 180)):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    gpay_img = load_logo("gpay.webp")  # Updated filename
    phonepe_img = load_logo("phonepe.png")
    paytm_img = load_logo("paytm.png")

    # Selection handler
    def select_upi_app(app_name):
        messagebox.showinfo("Selected", f"{app_name} selected for UPI Payment.")
        win.destroy()

    # Image buttons
    gpay_btn = tk.Button(win, image=gpay_img, bg="white", borderwidth=2,
                         command=lambda: select_upi_app("Google Pay"),
                         cursor="hand2")
    gpay_btn.place(x=screen_width//2 - 250, y=250)

    phonepe_btn = tk.Button(win, image=phonepe_img, bg="white", borderwidth=2,
                            command=lambda: select_upi_app("PhonePe"),
                            cursor="hand2")
    phonepe_btn.place(x=screen_width//2 - 80, y=250)

    paytm_btn = tk.Button(win, image=paytm_img, bg="white", borderwidth=2,
                          command=lambda: select_upi_app("Paytm"),
                          cursor="hand2")
    paytm_btn.place(x=screen_width//2 + 100, y=250)

    # Back button
    def go_back_to_pay():
        win.destroy()
        python = sys.executable
        script_path = os.path.join(os.path.dirname(__file__), "pay.py")
        subprocess.Popen([python, script_path])

    back_btn = tk.Button(win, 
                         text="← Back",
                         font=("Arial", 16),
                         bg="#ff4444",
                         fg="white",
                         command=go_back_to_pay,
                         cursor="hand2")
    back_btn.place(x=50, y=50)

    # Keep reference to images
    win.gpay_img = gpay_img
    win.phonepe_img = phonepe_img
    win.paytm_img = paytm_img

    win.mainloop()

if __name__ == "__main__":
    open_upi_payment_window()
