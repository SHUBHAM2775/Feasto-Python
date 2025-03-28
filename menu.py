import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys
import os
import textwrap
from dbconnect import get_menu_items, add_to_cart_db

# Initialize Tkinter
root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

# Function to go back to restaurant selection
def open_resto():
    root.destroy()
    import resto

# Function to open checkout
def open_checkout():
    root.destroy()
    import checkout  

# Function to add item to cart and update button text
def add_to_cart(order_id, dish_name, price, restaurant_name, button):
    try:
        add_to_cart_db(order_id, restaurant_name, dish_name, price, quantity=1)
        print(f"✅ Added to cart: {dish_name}")
        button.config(text="Added ✅", state="disabled", bg="white", fg="black")
        button.unbind("<Enter>")  
        button.unbind("<Leave>")
    except Exception as e:
        print(f"❌ Failed to add to cart: {e}")

# Button Hover Effects
def on_enter_checkout(e): checkout_button.config(bg="gray")
def on_leave_checkout(e): checkout_button.config(bg="black")

def on_enter_exit(e): exit_button.config(bg="gray")
def on_leave_exit(e): exit_button.config(bg="black")

def on_enter_add(e): e.widget.config(bg="darkorange")
def on_leave_add(e): e.widget.config(bg="orange")

# Get restaurant name and menu items
if len(sys.argv) < 2:
    restaurant_name = "Domino's"
    menu_items = [
        (4, "Cheese Pizza", 19, "Cheese, tomato, corn", "images/menu/cheese_pizza.jpg"),
        (5, "Paneer Pizza", 5, "Spicy paneer, bell peppers, mushroom, loads of cheese", "images/menu/paneer_pizza.jpg"),
        (6, "Veggie Supreme", 7, "Capsicum, onion, olives, cheese", "images/menu/veggie_supreme.jpg"),
    ]
else:
    restaurant_name = sys.argv[1]
    menu_items = get_menu_items(restaurant_name)

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and set background image
bg_image = Image.open("images/restobg3.png").resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create background label
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Title Label (Transparent Background)
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")
canvas.create_text(screen_width/2, 75, text=f"{restaurant_name} Menu", font=("Arial", 28, "bold"), fill="white")

# Scrollable Menu Frame
scroll_canvas = tk.Canvas(root, width=screen_width, height=screen_height - 200, highlightthickness=0, bg="black")
scroll_canvas.place(relx=0.01, rely=0.15, relwidth=0.96, relheight=0.75)

# Scrollbar
scrollbar = tk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
scrollbar.place(relx=0.98, rely=0.15, relheight=0.75)
scroll_canvas.configure(yscrollcommand=scrollbar.set)

# Scroll Frame
scroll_frame = tk.Frame(scroll_canvas, bg="black") 
scroll_window = scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=screen_width - 40)

# Store images to prevent garbage collection
image_refs = []
y_position = 20  

for item in menu_items:
    order_id, dish_name, price, description, image_path = item
    wrapped_description = "\n".join(textwrap.wrap(description, width=75))
    text = f" {dish_name} - ₹{price}\n {wrapped_description}"

    # Menu Item Frame
    item_frame = tk.Frame(scroll_frame, bg="black", padx=10, pady=10)
    item_frame.pack(fill="x", padx=20, pady=10)

    # Load and place image
    try:
        if os.path.exists(image_path):
            item_image = Image.open(image_path).resize((80, 80), Image.LANCZOS)
        else:
            print(f"Image not found for {dish_name}, using default image.")
            item_image = Image.open("images/default.jpg").resize((80, 80), Image.LANCZOS)

        item_photo = ImageTk.PhotoImage(item_image)
        image_refs.append(item_photo)

        image_label = tk.Label(item_frame, image=item_photo, bg="black")
        image_label.pack(side="left", padx=10)

    except Exception as e:
        print("Image load error:", e)

    # Menu Text Label
    text_label = tk.Label(item_frame, text=text, font=("Arial", 16), fg="white", bg="black", anchor="w", justify="left")
    text_label.pack(side="left", padx=10, expand=True, fill="both")

    # Add to Cart Button (Stylized)
    add_button = tk.Button(item_frame, text="Add to Cart", font=("Arial", 10, "bold"), bg="orange", fg="black", padx=12, pady=8, relief="ridge", borderwidth=2)
    add_button.config(command=lambda oid=order_id, name=dish_name, pr=price, btn=add_button: add_to_cart(oid, name, pr, restaurant_name, btn))
    add_button.pack(side="right", padx=10)

    # Add hover effects
    add_button.bind("<Enter>", on_enter_add)
    add_button.bind("<Leave>", on_leave_add)

# Update Scroll Region
scroll_frame.update_idletasks()
scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

# Bottom Buttons Frame (Side by Side)
bottom_frame = tk.Frame(root, bg="black")
bottom_frame.place(relx=0.5, rely=0.92, anchor="center")

# Checkout Button
checkout_button = tk.Button(bottom_frame, text="Checkout 🛒", font=("Arial", 14, "bold"), command=open_checkout, bg="#ff5f5f", fg="white", padx=20, pady=10, relief="ridge", borderwidth=2, width=15)
checkout_button.pack(side="left", padx=10)
checkout_button.bind("<Enter>", on_enter_checkout)
checkout_button.bind("<Leave>", on_leave_checkout)

# Back Button
exit_button = tk.Button(bottom_frame, text="⬅ Back", font=("Arial", 14, "bold"), command=open_resto, bg="#383838", fg="white", padx=20, pady=10, relief="ridge", borderwidth=2, width=15)
exit_button.pack(side="right", padx=10)
exit_button.bind("<Enter>", on_enter_exit)
exit_button.bind("<Leave>", on_leave_exit)

# Run the Tkinter loop
root.mainloop() 