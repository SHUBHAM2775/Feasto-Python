import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import db, get_user_details_by_username, deduct_feasto_points, add_feasto_points
import subprocess
import time
from datetime import datetime, timedelta
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Get table number from CLI arg (if any)
table_number = sys.argv[1] if len(sys.argv) > 1 else "N/A"

# Read username from file
with open("current_user.txt", "r") as f:
    user_line = f.readline().strip()
    username = user_line.split(",")[0]  # Format: SU,1234567890,35

# Get user information from current_user.txt
try:
    with open("current_user.txt", "r") as f:
        user_info = f.read().strip().split(',')
        user_name = user_info[0]
        table_number = user_info[2]  # Table number is the third element
except:
    user_name = "Guest User"
    table_number = "N/A"

# Initialize Tkinter
root = tk.Tk()
root.title("Feasto: Order Status")
root.state('zoomed')  # Fullscreen mode

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize background image
bg_image = Image.open("images/restobg3.png").resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

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
    subprocess.Popen(["python", "user.py", "status", table_number])

# Make the canvas clickable
user_canvas.bind("<Button-1>", lambda event: open_user())

# Display "Order Status" title
canvas.create_text(
    screen_width // 2, 80,
    text="Order Status",
    font=("Georgia", 28, "bold"),
    fill="white"
)

# Create semi-transparent rectangle for status information
status_rect = canvas.create_rectangle(
    screen_width * 0.2, screen_height * 0.3,
    screen_width * 0.8, screen_height * 0.7,
    fill="black",
    stipple="gray50"
)

# Display Table Number
canvas.create_text(
    screen_width // 2, screen_height * 0.35,
    text=f"Table Number: {table_number}",
    font=("Arial", 24),
    fill="white"
)

# Display User Name
canvas.create_text(
    screen_width // 2, screen_height * 0.45,
    text=f"Order for: {user_name}",
    font=("Arial", 24),
    fill="white"
)

# Initialize countdown variables
initial_time = 1  # minutes
countdown_time = initial_time * 60  # convert to seconds
countdown_label = canvas.create_text(
    screen_width // 2, screen_height * 0.55,
    text="",
    font=("Arial", 24),
    fill="white"
)

def update_countdown():
    global countdown_time
    if countdown_time > 0:
        minutes = countdown_time // 60
        seconds = countdown_time % 60
        canvas.itemconfig(countdown_label, 
                         text=f"Estimated Time: {minutes:02d}:{seconds:02d}",
                         fill="yellow")
        countdown_time -= 1
        root.after(1000, update_countdown)
    else:
        canvas.itemconfig(countdown_label, 
                         text="Your order is ready!",
                         fill="yellow")

# Start the countdown
update_countdown()

# Fetch cart items from the database
cart_items = db.cart.find()
item_amount = sum(item['quantity'] * item['price'] for item in cart_items)
gst_amount = item_amount * 0.05
total_amount = item_amount + gst_amount

# Calculate Feasto Points based on Total Amount
if total_amount < 200:
    earned_points = 10
elif total_amount < 500:
    earned_points = 30
elif total_amount < 1000:
    earned_points = 60
else:
    earned_points = 100

# Add Feasto Points to current user
add_feasto_points(user_name, earned_points)

# Display Earned Points
canvas.create_text(
    screen_width // 2, screen_height * 0.65,
    text=f"You earned {earned_points} Feasto Points!",
    font=("Arial", 22, "bold"),
    fill="lightgreen"
)

root.mainloop()
