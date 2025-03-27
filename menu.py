import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import get_menu_items, add_to_cart_db
import textwrap
import os

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
    import checkout  # Make sure checkout.py exists

# Function to add item to cart and update button text
def add_to_cart(order_id, dish_name, price, restaurant_name, button):
    try:
        add_to_cart_db(order_id, restaurant_name, dish_name, price, quantity=1)
        print(f"✅ Added to cart: {dish_name}")
        button.config(text="Added ✅", state="disabled", bg="white", fg="black")
    except Exception as e:
        print(f"❌ Failed to add to cart: {e}")

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

# Title Label
title_label = tk.Label(root, text=f"{restaurant_name} Menu", font=("Arial", 28, "bold"), fg="white", bg="black")
title_label.place(relx=0.5, rely=0.05, anchor="center")

# Scrollable Menu Frame
scroll_canvas = tk.Canvas(root, width=screen_width, height=screen_height - 200, bg="black", highlightthickness=0)
scroll_frame = tk.Frame(scroll_canvas, bg="black")
scrollbar = tk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)

scroll_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.place(relx=0.98, rely=0.15, relheight=0.75)  # Right-side scrollbar
scroll_canvas.place(relx=0.01, rely=0.15, relwidth=0.96, relheight=0.75)
scroll_window = scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=screen_width - 40)

# Store images to prevent garbage collection
image_refs = []
y_position = 20  # Start position inside the frame

for item in menu_items:
    order_id, dish_name, price, description, image_path = item
    wrapped_description = "\n".join(textwrap.wrap(description, width=75))
    text = f"#{order_id} {dish_name} - ${price}\n{wrapped_description}"

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
    text_label.pack(side="left", padx=10)

    # Add to Cart Button
    add_button = tk.Button(item_frame, text="Add to Cart", font=("Arial", 10, "bold"), bg="orange", fg="black", padx=7, pady=7)
    add_button.config(command=lambda oid=order_id, name=dish_name, pr=price, btn=add_button: add_to_cart(oid, name, pr, restaurant_name, btn))
    add_button.pack(side="right", padx=10)

# Update Scroll Region
scroll_frame.update_idletasks()
scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

# Checkout and Back Buttons (fixed at the bottom)
checkout_button = tk.Button(root, text="Checkout", font=("Arial", 14), command=open_checkout, bg="white", fg="black")
checkout_button.place(x=screen_width // 2 - 150, y=screen_height - 100, width=300, height=40)

exit_button = tk.Button(root, text="Back to Restaurant Selection", font=("Arial", 14), command=open_resto, bg="white", fg="black")
exit_button.place(x=screen_width // 2 - 150, y=screen_height - 50, width=300, height=40)

# Run the Tkinter loop
root.mainloop()
