from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from dbconnect import db
import subprocess
import sys

# Get table number from command line arguments
table_number = sys.argv[1] if len(sys.argv) > 1 else "N/A"

def create_payment_button(window, text, x, y):
    return Button(window, 
                 text=text,
                 font=("Arial", 22, "bold"),
                 bg="white",
                 fg="#333333",
                 width=15,
                 height=2,
                 relief="raised",
                 borderwidth=3,
                 cursor="hand2",
                 activebackground="#f0f0f0")

def handle_payment(method):
    # Here you can add the logic for each payment method
    print(f"Processing {method} payment...")
    # Add your payment processing logic here
    # After processing, you can open the confirmation screen
    root.destroy()
    # import confirmation  # You can import your confirmation screen here

root = tk.Tk()
root.title("Feasto: Payment Options")
root.state('zoomed')

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Background setup
bg_image = Image.open("images/restobg3.png")
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# After canvas creation and before title
# Add user profile button
user_icon_size = 150
user_icon_x = user_icon_size // 2 + 20
user_icon_y = user_icon_size // 2 + 20

# Load and resize the user icon image
try:
    user_icon = Image.open("images/user.jpg").resize((user_icon_size, user_icon_size))
    user_photo = ImageTk.PhotoImage(user_icon)
except:
    print("User icon image not found, creating placeholder")
    user_icon = Image.new("RGB", (user_icon_size, user_icon_size), "gray")
    user_photo = ImageTk.PhotoImage(user_icon)

# Create label for the user icon
user_label = tk.Label(root, image=user_photo, cursor="hand2", bg="black")
user_label.image = user_photo
user_label.place(x=20, y=20)

def open_user():
    root.destroy()
    subprocess.Popen(["python", "user.py", "pay", table_number])

user_label.bind("<Button-1>", lambda event: open_user())

# Title
canvas.create_text(755, 80, text="Select Payment Method", 
                  font=("Arial", 35, "bold"), fill="white")

# Create semi-transparent rectangle
canvas.create_rectangle(250, 150, 1300, 600,
                       fill="grey", 
                       stipple='gray50')

# Payment method buttons with improved design
upi_btn = create_payment_button(root, "UPI Payment", 0, 0)
upi_btn.configure(command=lambda: handle_payment("UPI"))
upi_btn.place(x=775, y=250, anchor="center")

card_btn = create_payment_button(root, "Card Payment", 0, 0)
card_btn.configure(command=lambda: handle_payment("Card"))
card_btn.place(x=775, y=375, anchor="center")

cash_btn = create_payment_button(root, "Cash Payment", 0, 0)
cash_btn.configure(command=lambda: handle_payment("Cash"))
cash_btn.place(x=775, y=500, anchor="center")


root.mainloop()
