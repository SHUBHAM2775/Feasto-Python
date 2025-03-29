from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from dbconnect import get_latest_user, get_user_by_credentials
import sys
import subprocess

# Get the previous page from command line argument
previous_page = sys.argv[1] if len(sys.argv) > 1 else "bill"  # Default to bill.py if no argument
table_number = sys.argv[2] if len(sys.argv) > 2 else "N/A"    # Get table number from command line
restaurant_name = sys.argv[5] if len(sys.argv) > 5 else "N/A"  # Get restaurant name for checkout

root = tk.Tk()
root.title("Feasto")
root.state('zoomed')    

# Get logged-in user credentials from temporary file
try:
    with open("current_user.txt", "r") as f:
        user_name, mobile_number, table_number = f.read().strip().split(",")
    user_details = get_user_by_credentials(user_name, mobile_number)
    if not user_details:
        user_details = {"name": user_name, "mobile": mobile_number, "feasto_points": 0}
    user_details["table_number"] = table_number
except:
    user_details = {"name": "N/A", "mobile": "N/A", "table_number": "N/A", "feasto_points": 0}

# Create canvas
canvas = tk.Canvas(root, highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

# Load background image and set it as full-screen background
bg_image = Image.open("images/homebg.png")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Add image to canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(765, 275, text="User Profile Details", font=("Arial", 40, "bold"), fill="white")

canvas.create_text(600, 400, text="Name", font=("Arial", 20, "bold"), fill="white")
canvas.create_text(600, 475, text="Phone", font=("Arial", 20, "bold"), fill="white") 
canvas.create_text(600, 550, text="Table Number", font=("Arial", 20, "bold"), fill="white")
canvas.create_text(600, 625, text="Feasto Points: ", font=("Arial", 20, "bold"), fill="white")

# Display user details
canvas.create_text(900, 400, text=user_details["name"], font=("Arial", 20), fill="white")
canvas.create_text(900, 475, text=user_details["mobile"], font=("Arial", 20), fill="white")
canvas.create_text(900, 550, text=user_details["table_number"], font=("Arial", 20), fill="white")
canvas.create_text(900, 625, text=str(user_details.get("feasto_points", 0)), font=("Arial", 20), fill="white")

def go_back():
    """Return to the previous page based on where we came from"""
    root.destroy()
    if previous_page == "bill":
        subprocess.Popen(["python", "bill.py", table_number, user_details["name"], user_details["mobile"]])
    elif previous_page == "menu":
        subprocess.Popen(["python", "resto.py", table_number, user_details["name"], user_details["mobile"]])
    elif previous_page == "checkout":
        subprocess.Popen(["python", "checkout.py", restaurant_name, table_number, user_details["name"], user_details["mobile"]])
    elif previous_page == "pay":
        subprocess.Popen(["python", "pay.py", table_number, user_details["name"], user_details["mobile"]])
    elif previous_page == "resto":
        subprocess.Popen(["python", "resto.py", table_number, user_details["name"], user_details["mobile"]])
    else:
        subprocess.Popen(["python", "bill.py", table_number, user_details["name"], user_details["mobile"]])  # Default fallback

# Create a back button
back_button = tk.Button(root, text="Back", 
                       font=('Arial', 16), 
                       bg="yellow", 
                       fg="black", 
                       command=go_back,
                       width=10)
back_button.place(relx=0.5, rely=0.8, anchor="center")

root.mainloop()