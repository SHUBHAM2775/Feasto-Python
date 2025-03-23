from dbconnect import get_restaurants
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess

# Fetch restaurant data
restaurants = get_restaurants()

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

# Dropdown
selected_restaurant = tk.StringVar()
selected_restaurant.set("Choose By Restaurant")

drop = ttk.Combobox(root, textvariable=selected_restaurant, 
                    values=list(restaurants.keys()), 
                    font=('Georgia', 18), justify="center", state="readonly")
drop.place(relx=0.5, y=50, anchor="center", width=300, height=40)

# Open Menu Function
def open_menu():
    restaurant_name = selected_restaurant.get()
    if restaurant_name in restaurants:
        root.destroy()
        menu_items = restaurants[restaurant_name]["menu"]
        subprocess.Popen(["python", "menu.py", restaurant_name] + menu_items)

menu_button = tk.Button(root, text="View Menu", font=("Arial", 14), command=open_menu)
menu_button.place(relx=0.5, y=100, anchor="center", width=150, height=40)

# Grid Configurations
grid_size = 4  # Number of columns
image_size = min(screen_width // (grid_size + 1), 250)  # Dynamic image size (max 250px)
padding_x = (screen_width - (grid_size * image_size)) // (grid_size + 1)  # Equal spacing
padding_y = 50  # Vertical spacing between rows

# Starting positions
x_start, y_start = padding_x, 200
x_pos, y_pos = x_start, y_start

# Restaurant Images Grid
for idx, (name, data) in enumerate(restaurants.items()):
    image_path = data["image"]
    
    # Load image or placeholder
    img = Image.open(image_path).resize((image_size, image_size)) if os.path.exists(image_path) else Image.new("RGB", (image_size, image_size), "gray")
    photo = ImageTk.PhotoImage(img)

    # Create bordered square grid
    frame = tk.Frame(root, width=image_size, height=image_size, bg="white", highlightbackground="black", highlightthickness=2)
    frame.place(x=x_pos, y=y_pos)

    # Place image inside the frame
    img_label = tk.Label(frame, image=photo, bg="white")
    img_label.image = photo  # Keep a reference
    img_label.place(relx=0.5, rely=0.5, anchor="center")

    # Label for restaurant name
    label = tk.Label(root, text=name, font=("Arial", 14), bg="white")
    label.place(x=x_pos + (image_size // 2), y=y_pos + image_size + 10, anchor="center")

    # Move to next grid position
    x_pos += image_size + padding_x
    if (idx + 1) % grid_size == 0:  # Move to next row after 4 images
        x_pos = x_start
        y_pos += image_size + padding_y

root.mainloop()
