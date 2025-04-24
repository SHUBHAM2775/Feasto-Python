import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import sys


def open_card_payment_window():
    win = tk.Tk()
    win.title("Feasto: Card Payment")
    win.state('zoomed')

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Load background image
    try:
        bg_image = Image.open("images/restobg3.png")
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
    except Exception as e:
        messagebox.showerror("Error", f"Background image not found: {e}")
        win.destroy()
        return

    canvas = tk.Canvas(win, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Title
    canvas.create_text(screen_width // 2, 80, text="Enter Card Details",
                       font=("Arial", 35, "bold"), fill="white")

    # Grey semi-transparent box
    canvas.create_rectangle(400, 150, 1100, 600,
                            fill="grey", stipple='gray50')

    # Labels and Entry fields
    labels = ["Card Number:", "Card Holder Name:", "Expiry Date (MM/YY):", "CVV:"]
    entries = []

    for i, label_text in enumerate(labels):
        label = tk.Label(win, text=label_text, font=("Arial", 16), bg="grey")
        label.place(x=450, y=200 + i * 80)
        entry = tk.Entry(win, font=("Arial", 16), width=30, show="*" if "CVV" in label_text else "")
        entry.place(x=700, y=200 + i * 80)
        entries.append(entry)

    # Submit button
    def submit_card_details():
        card_number = entries[0].get().strip()
        card_holder = entries[1].get().strip()
        expiry_date = entries[2].get().strip()
        cvv = entries[3].get().strip()

        # Validate card number (16 digits, numeric only)
        if not (card_number.isdigit() and len(card_number) == 16):
            messagebox.showwarning("Input Error", "Card Number must be 16 digits.")
            return

        # Validate card holder name (alphabetic only)
        if not card_holder.replace(" ", "").isalpha():
            messagebox.showwarning("Input Error", "Card Holder Name must contain only letters.")
            return

        # Validate expiry date (MM/YY format)
        if not (len(expiry_date) == 5 and expiry_date[2] == '/' and expiry_date[:2].isdigit() and expiry_date[3:].isdigit()):
            messagebox.showwarning("Input Error", "Expiry Date must be in MM/YY format.")
            return

        month, year = expiry_date.split('/')
        if not (1 <= int(month) <= 12):
            messagebox.showwarning("Input Error", "Invalid month in Expiry Date.")
            return

        # Validate CVV (3 digits, numeric only)
        if not (cvv.isdigit() and len(cvv) == 3):
            messagebox.showwarning("Input Error", "CVV must be 3 digits.")
            return

        # If all validations pass
        messagebox.showinfo("Payment Successful", "Your card has been charged successfully.")
        win.destroy()

        # After processing, open the order status screen with table number
        try:
            with open("current_user.txt", "r") as f:
                user_info = f.read().strip().split(',')
                table_number = user_info[2]  # Table number is the third element
        except:
            table_number = "N/A"

        subprocess.Popen(["python", "order_status.py", table_number])

    submit_btn = tk.Button(win, text="Submit", font=("Arial", 16),
                           bg="#4CAF50", fg="white", command=submit_card_details,
                           cursor="hand2")
    submit_btn.place(x=700, y=520)

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
    win.bg_photo = bg_photo

    win.mainloop()


if __name__ == "__main__":
    open_card_payment_window()
