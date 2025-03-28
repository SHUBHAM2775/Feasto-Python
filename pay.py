from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from dbconnect import db

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

# Back button
back_btn = Button(root, 
                 text="← Back",
                 font=("Arial", 16),
                 bg="#ff4444",
                 fg="white",
                 command=lambda: [root.destroy(), __import__('payment')],
                 cursor="hand2")
back_btn.place(x=50, y=50)

root.mainloop()
