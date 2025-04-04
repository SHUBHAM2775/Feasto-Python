from dbconnect import get_restaurants, clear_cart  # Import the new clear_cart function
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess
import sys

# Clear cart every time resto.py is opened
clear_cart()  # Deletes all documents from the cart collection

# Fetch restaurant data
restaurants = get_restaurants()

if not restaurants:
    print("No restaurants found in the database.")  # Debugging line

# Initialize Tkinter
root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

# Background
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
bg_image = Image.open("images/restobg3.png").resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Replace the circle creation code with an image button
user_icon_size = 150  # Increased size
user_icon_x = user_icon_size // 2 + 20  # Adjusted x position
user_icon_y = user_icon_size // 2 + 20  # Adjusted y position

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

# Function to open user.py
def open_user():
    root.destroy()
    subprocess.Popen(["python", "user.py", "resto", table_number])

# Make the canvas clickable
user_canvas.bind("<Button-1>", lambda event: open_user())

# Dropdown
selected_restaurant = tk.StringVar()
selected_restaurant.set("Choose By Restaurant")

# Ensure restaurants are correctly passed as values
restaurant_names = list(restaurants.keys())
print("Dropdown Values:", restaurant_names)  # Debugging line

drop = ttk.Combobox(root, textvariable=selected_restaurant, values=restaurant_names, 
                    font=('Georgia', 18), justify="center", state="readonly")
drop.place(relx=0.5, y=50, anchor="center", width=300, height=40)

# Open Menu Function
def open_menu(restaurant_name=None):
    """Opens the menu.py script for the selected restaurant"""
    root.destroy()
    if restaurant_name is None:
        restaurant_name = selected_restaurant.get()

    if restaurant_name in restaurants:
        subprocess.Popen(["python", "menu.py", restaurant_name, table_number])

menu_button = tk.Button(root, text="View Menu", font=("Arial", 14), command=open_menu)
menu_button.place(relx=0.5, y=100, anchor="center", width=150, height=40)

# Display restaurant images
columns = 4
image_size = 200
gap = 50
label_gap = 15

x_start = (screen_width - (columns * (image_size + gap) - gap)) // 2
y_start = 200
x_pos, y_pos = x_start, y_start

image_refs = {}  # Dictionary to keep image references

for index, (name, data) in enumerate(restaurants.items()):
    image_path = data["image"]
    
    if os.path.exists(image_path):
        img = Image.open(image_path).resize((image_size, image_size))
    else:
        print(f"Image not found for {name}: {image_path}")  # Debugging line
        img = Image.new("RGB", (image_size, image_size), "gray")

    photo = ImageTk.PhotoImage(img)
    image_refs[name] = photo  # Keep reference to avoid garbage collection

    # Black background frame with white border
    frame = tk.Frame(root, width=image_size, height=image_size, bg="black", highlightbackground="white", highlightthickness=2)
    frame.place(x=x_pos, y=y_pos)

    # Image Label (Clickable)
    img_label = tk.Label(frame, image=photo, bg="black", cursor="hand2")
    img_label.image = photo
    img_label.place(relx=0.5, rely=0.5, anchor="center")

    # Bind the image to open menu.py when clicked
    img_label.bind("<Button-1>", lambda event, r=name: open_menu(r))
    
    x_pos += image_size + gap
    if (index + 1) % columns == 0:
        x_pos = x_start
        y_pos += image_size + gap + 50

# Near the top of the file, after imports
table_number = sys.argv[1] if len(sys.argv) > 1 else "N/A"

root.mainloop()
