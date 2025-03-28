from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from dbconnect import db  # Import the database connection

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


canvas.create_text(755, 80, text="Payment", font=("Arial", 35, "bold"), fill="white")
# Create semi-transparent rectangle - made taller to fit all elements
canvas.create_rectangle(250, 150, 1300, 750,  # Shifted up from 200, 800
                       fill="grey", 
                       stipple='gray50')

# Centered title with more space
canvas.create_text(775, 200, text="Bill details", font=("Arial", 30, "bold"), fill="#ffffff")
canvas.create_line(300, 250, 1250, 250, fill="white", width=2)

# Calculate item_amount from cart collection
cart_items = db.cart.find()
item_amount = sum(item['quantity'] * item['price'] for item in cart_items)
gst_amount = item_amount * 0.18  # Assuming 18% GST

# Better spacing for bill items
canvas.create_text(500, 330, text=f"Item amount : ₹{item_amount:.2f}", font=("Arial", 20), fill="white")
canvas.create_text(500, 410, text=f"GST amount : ₹{gst_amount:.2f}", font=("Arial", 20), fill="white")

# Divider line with more space
canvas.create_line(300, 470, 1250, 470, fill="white", width=2)

total_amount = item_amount + gst_amount
# Total amount with better positioning
canvas.create_text(500, 530, text=f"Total amount : ₹{total_amount:.2f}", font=("Arial", 20, "bold"), fill="white")

# Payment method section with better spacing
canvas.create_text(500, 610, text="Pay By: ", font=("Arial", 20), fill="white")

# Adjusted button positions with better spacing
upi = Button(root, text="UPI", font=("Arial", 20), bg="white", fg="black", width=10, height=1)
upi.place(x=600, y=650)

card = Button(root, text="Card", font=("Arial", 20), bg="white", fg="black", width=10, height=1)
card.place(x=800, y=650)

cash = Button(root, text="Cash", font=("Arial", 20), bg="white", fg="black", width=10, height=1)
cash.place(x=1000, y=650)


root.mainloop()