from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from dbconnect import db, get_latest_user  # Import the database connection and get_latest_user function
from dbconnect import get_user_details

import subprocess
import sys

# Get table number from command line arguments BEFORE using it
table_number = sys.argv[1] if len(sys.argv) > 1 else "N/A"



def payment_options():
    root.destroy()  # Close current window
    subprocess.Popen(["python", "pay.py", table_number])

root = tk.Tk()
root.title("Feasto: Payment")
root.state('zoomed')  # Fullscreen with minimize & close button

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Open and resize the background image to fit the screen
bg_image = Image.open("images/restobg3.png")
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# After canvas creation and before Payment title
# Add user profile button
user_icon_size = 150
user_icon_x = user_icon_size // 2 + 20
user_icon_y = user_icon_size // 2 + 20

# Load and resize the user icon image
try:
    user_icon = Image.open("images/user.png").resize((user_icon_size, user_icon_size))
    user_photo = ImageTk.PhotoImage(user_icon)
except:
    print("User icon image not found, creating placeholder")
    user_icon = Image.new("RGB", (user_icon_size, user_icon_size), "gray")
    user_photo = ImageTk.PhotoImage(user_icon)

# Create a canvas for the user icon
user_canvas = tk.Canvas(root, width=user_icon_size, height=user_icon_size, 
                       bg="black", highlightthickness=0)
user_canvas.place(x=20, y=20)

# Add the image to the canvas
user_canvas.create_image(user_icon_size//2, user_icon_size//2, 
                        image=user_photo, anchor="center")
user_canvas.config(cursor="hand2")

def open_user():
    root.destroy()
    subprocess.Popen(["python", "user.py", "bill", table_number])

# Make the canvas clickable
user_canvas.bind("<Button-1>", lambda event: open_user())

canvas.create_text(755, 80, text="Payment", font=("Arial", 35, "bold"), fill="white")
# Create semi-transparent rectangle - made taller to fit all elements
canvas.create_rectangle(250, 200, 1300, 700,
                       fill="grey", 
                       stipple='gray50')

# Get user details from current_user.txt
try:
    with open("current_user.txt", "r") as f:
        user_name, mobile_number, table_number = f.read().strip().split(",")
except:
    user_name = "N/A"
    mobile_number = "N/A"

# Create a circle with table number in top right corner
circle_x = 1200  # X position of circle center
circle_y = 250   # Y position of circle center
circle_radius = 40  # Radius of the circle

# Create circle with a nice contrasting color
canvas.create_oval(
    circle_x - circle_radius, 
    circle_y - circle_radius,
    circle_x + circle_radius, 
    circle_y + circle_radius,
    fill="#4CAF50",
    outline="white",
    width=2
)

# Add table number text in circle
canvas.create_text(
    circle_x,
    circle_y,
    text=f"#{table_number}",
    font=("Arial", 20, "bold"),
    fill="white"
)

# Centered title with customer name
canvas.create_text(775, 250, text=f"Bill Details for {user_name}", font=("Arial", 30, "bold"), fill="#ffffff")

# Single separator line after title
canvas.create_line(300, 300, 1250, 300, fill="white", width=2)

# Calculate item_amount from cart collection
cart_items = db.cart.find()
item_amount = sum(item['quantity'] * item['price'] for item in cart_items)
gst_amount = item_amount * 0.05  # Assuming 5% GST

# Bill items section with tighter spacing
canvas.create_text(500, 350, text=f"Item amount : ₹{item_amount:.2f}", font=("Arial", 20), fill="white", anchor="w")
canvas.create_text(500, 400, text=f"GST amount : ₹{gst_amount:.2f}", font=("Arial", 20), fill="white", anchor="w")

# Divider line for total
canvas.create_line(300, 450, 1250, 450, fill="white", width=2)

total_amount = item_amount + gst_amount
# Total amount
canvas.create_text(500, 500, text=f"Total amount : ₹{total_amount:.2f}", font=("Arial", 22, "bold"), fill="white", anchor="w")

# Fetch user's details (including Feasto Points)
user_details = get_user_details()
balance = user_details.get("feasto_points", 0) 

# Display the Feasto points balance below the total amount
canvas.create_text(500, 550, text=f"Feasto Points : ₹{balance:.2f}", font=("Arial", 20, "bold"), fill="white", anchor="w")

# Pay button with adjusted position
pay_FP = Button(root, text="Pay Using FP", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white", 
                   width=15, height=1, command=payment_options)
pay_FP.place(x=600, y=625, anchor="center")

pay_button = Button(root, text="Pay", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white", 
                   width=15, height=1, command=payment_options)
pay_button.place(x=950, y=625, anchor="center")



root.mainloop()