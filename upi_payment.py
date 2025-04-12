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

    # Load and resize UPI app logos
    def load_logo(path, size=(180, 180)):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    gpay_img = load_logo("images/gpay.png")
    phonepe_img = load_logo("images/phonepe.png")
    paytm_img = load_logo("images/paytm.png")

    # Function to open QR window and auto-redirect to order_status.py
    def open_qr_window(image_path, app_name):
        win.destroy()
        qr_win = tk.Tk()
        qr_win.title(f"{app_name} - Scan to Pay")
        qr_win.state('zoomed')
        qr_win.configure(bg="white")

        screen_width = qr_win.winfo_screenwidth()
        screen_height = qr_win.winfo_screenheight()

        try:
            qr_img = Image.open(image_path)
            qr_img = qr_img.resize((400, 400), Image.LANCZOS)
            qr_photo = ImageTk.PhotoImage(qr_img)

            tk.Label(qr_win, image=qr_photo, bg="white").pack(pady=50)
            tk.Label(qr_win, text=f"Scan using {app_name}", font=("Arial", 28, "bold"), bg="white").pack()

            qr_win.qr_photo = qr_photo  # Keep reference

            # Redirect after 5 seconds
            def go_to_order_status():
                qr_win.destroy()
                python = sys.executable
                script_path = os.path.join(os.path.dirname(__file__), "order_status.py")
                subprocess.Popen([python, script_path])

            qr_win.after(5000, go_to_order_status)
            qr_win.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Could not load QR image:\n{str(e)}")

    # Selection handler
    def select_upi_app(app_name):
        if app_name == "Google Pay":
            open_qr_window("images/gpayScanner.png", app_name)
        elif app_name == "PhonePe":
            open_qr_window("images/phonepeQR.png", app_name)
        elif app_name == "Paytm":
            open_qr_window("images/paytmQR.png", app_name)

    # Coordinates for horizontal alignment
    center_y = 300
    spacing = 240
    start_x = screen_width // 2 - spacing

    gpay_btn = tk.Button(win, image=gpay_img, bg="white", borderwidth=2,
                         command=lambda: select_upi_app("Google Pay"),
                         cursor="hand2")
    gpay_btn.place(x=start_x, y=center_y)

    phonepe_btn = tk.Button(win, image=phonepe_img, bg="white", borderwidth=2,
                            command=lambda: select_upi_app("PhonePe"),
                            cursor="hand2")
    phonepe_btn.place(x=start_x + spacing, y=center_y)

    paytm_btn = tk.Button(win, image=paytm_img, bg="white", borderwidth=2,
                          command=lambda: select_upi_app("Paytm"),
                          cursor="hand2")
    paytm_btn.place(x=start_x + spacing * 2, y=center_y)

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
