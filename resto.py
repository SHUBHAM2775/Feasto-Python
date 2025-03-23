from dbconnect import get_restaurants
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess

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
def open_menu():
    restaurant_name = selected_restaurant.get()
    if restaurant_name in restaurants:
        root.destroy()
        subprocess.Popen(["python", "menu.py", restaurant_name])

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

for index, (name, data) in enumerate(restaurants.items()):
    image_path = data["image"]
    
    if os.path.exists(image_path):
        img = Image.open(image_path).resize((image_size, image_size))
    else:
        print(f"Image not found for {name}: {image_path}")  # Debugging line
        img = Image.new("RGB", (image_size, image_size), "gray")

    photo = ImageTk.PhotoImage(img)

    frame = tk.Frame(root, width=image_size, height=image_size, highlightbackground="black", highlightthickness=2)
    frame.place(x=x_pos, y=y_pos)

    img_label = tk.Label(frame, image=photo)
    img_label.image = photo
    img_label.place(relx=0.5, rely=0.5, anchor="center")

    label = tk.Label(root, text=name, font=("Arial", 14), fg="black", bg="white")
    label.place(x=x_pos + (image_size // 2), y=y_pos + image_size + label_gap, anchor="center")

    x_pos += image_size + gap
    if (index + 1) % columns == 0:
        x_pos = x_start
        y_pos += image_size + gap + 50
        

        

root.mainloop()
