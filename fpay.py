from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from dbconnect import db, get_user_details_by_username, deduct_feasto_points
import subprocess
import sys

# Get table number from CLI arg (if any)
table_number = sys.argv[1] if len(sys.argv) > 1 else "N/A"

# Read username from file
with open("current_user.txt", "r") as f:
    user_line = f.readline().strip()
    username = user_line.split(",")[0]  # Format: SU,1234567890,35

root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Background setup
bg_image = Image.open("images/restobg3.png")
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Get cart and billing details
cart_items = db.cart.find()
item_amount = sum(item['quantity'] * item['price'] for item in cart_items)
gst_amount = item_amount * 0.05
total_amount = item_amount + gst_amount

# Get user details
user_details = get_user_details_by_username(username)
balance = user_details.get("feasto_points", 0)

# Discount options
discount_options = {
    "No Discount": (0, 0),
    "10% - 200 Points": (0.10, 200),
    "20% - 500 Points": (0.20, 500),
    "30% - 1000 Points": (0.30, 1000),
}

# ----- UI ELEMENTS -----

canvas.create_text(screen_width // 2, 100, text="Feasto Billing", font=("Arial", 36, "bold"), fill="white")
canvas.create_text(screen_width // 2, 200, text=f"Total Amount : ₹{total_amount:.2f}", font=("Arial", 22, "bold"), fill="white")
canvas.create_text(screen_width // 2, 250, text=f"Feasto Points : {balance:.2f}", font=("Arial", 20, "bold"), fill="white")

selected_discount = StringVar()
selected_discount.set("No Discount")

discount_label = Label(root, text="Select Discount:", font=("Arial", 18, "bold"), bg="#232323", fg="white")
discount_dropdown = ttk.Combobox(root, textvariable=selected_discount, values=list(discount_options.keys()),
                                 font=("Arial", 14), state="readonly", width=25)
apply_btn = Button(root, text="Apply Discount", font=("Arial", 14, "bold"),
                   bg="#0077cc", fg="white", command=lambda: apply_discount())

# Final amount label below apply discount
final_price_label = Label(root, text="", font=("Arial", 20, "bold"), bg="#232323", fg="white")

proceed_btn = Button(root, text="Proceed to Pay", font=("Arial", 16, "bold"),
                     bg="#28a745", fg="white", command=lambda: proceed_to_pay(), state="disabled")

# Go back button
go_back_btn = Button(root, text="Go Back", font=("Arial", 16, "bold"),
                     bg="#ff5c5c", fg="white", command=lambda: go_back(), state="normal")

# ----- LOGIC -----
discount_percent = 0
used_points = 0

def apply_discount():
    global discount_percent, used_points
    option = selected_discount.get()
    discount_percent, required_points = discount_options[option]

    if balance < required_points:
        messagebox.showerror("Insufficient Points", "You don't have enough Feasto Points for this discount!")
        final_price_label.config(text="")
        proceed_btn.config(state="disabled")
        discount_percent = 0
        used_points = 0
    else:
        discount_amount = total_amount * discount_percent
        final_price = total_amount - discount_amount
        used_points = required_points
        final_price_label.config(text=f"Final amount after {int(discount_percent * 100)}% discount: ₹{final_price:.2f}")
        proceed_btn.config(state="normal")

def proceed_to_pay():
    if used_points > 0:
        deduct_feasto_points(username, used_points)
    subprocess.Popen(["python", "pay.py"])
    root.destroy()

def go_back():
    subprocess.Popen(["python", "bill.py"])  # Launch pay.py
    root.destroy()

# ----- PLACE WIDGETS -----
canvas.create_window(screen_width // 2, 320, window=discount_label)
canvas.create_window(screen_width // 2, 375, window=discount_dropdown)
canvas.create_window(screen_width // 2, 445, window=apply_btn)
canvas.create_window(screen_width // 2, 500, window=final_price_label)  # Final amount message
canvas.create_window(screen_width // 2 - 150, screen_height - 100, anchor="center", window=go_back_btn)  # Go back button
canvas.create_window(screen_width // 2 + 150, screen_height - 100, anchor="center", window=proceed_btn)  # Proceed button

root.mainloop()
