import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import textwrap
from dbconnect import get_menu_items, add_to_cart_db

# Initialize Tkinter
root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and set background image
bg_image = Image.open("images/restobg3.png").resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create main Canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Scrollable Frame with Background
scroll_canvas = tk.Canvas(canvas, width=screen_width - 40, height=screen_height, highlightthickness=0, bg="black")
scrollbar = tk.Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
scrollbar.pack(side="right", fill="y")
scroll_canvas.configure(yscrollcommand=scrollbar.set)

scroll_frame = tk.Frame(scroll_canvas, bg="black")
scroll_window = scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=screen_width - 40)
scroll_canvas.pack(side="left", fill="both", expand=True)

# Apply background to scrollable frame with reduced opacity
def set_background():
    bg_label = tk.Label(scroll_frame, image=bg_photo, bg="black")
    bg_label.place(relwidth=1, relheight=1)
    bg_label.lower()

# Function to enable scrolling with mouse wheel
def on_mouse_scroll(event):
    scroll_canvas.yview_scroll(-1 * (event.delta // 120), "units")

scroll_canvas.bind_all("<MouseWheel>", on_mouse_scroll)

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
        button.config(text="Added ✅", state="disabled", bg="gray", fg="white")
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

# Title Label
title_label = tk.Label(scroll_frame, text=f"{restaurant_name} Menu", font=("Arial", 28, "bold"), fg="white", bg="black", padx=10, pady=5)
title_label.pack(pady=20)

# Store images to prevent garbage collection
image_refs = []
for item in menu_items:
    order_id, dish_name, price, description, image_path = item
    wrapped_description = "\n".join(textwrap.wrap(description, width=75))
    text = f"#{order_id} {dish_name} - ${price}\n{wrapped_description}"

    item_frame = tk.Frame(scroll_frame, bg="black", padx=10, pady=10)
    item_frame.pack(fill="x", padx=20, pady=10)

    try:
        if os.path.exists(image_path):
            item_image = Image.open(image_path).resize((80, 80), Image.LANCZOS)
        else:
            item_image = Image.open("images/default.jpg").resize((80, 80), Image.LANCZOS)
        item_photo = ImageTk.PhotoImage(item_image)
        image_refs.append(item_photo)
        image_label = tk.Label(item_frame, image=item_photo, bg="black")
        image_label.pack(side="left", padx=10)
    except Exception as e:
        print("Image load error:", e)

    text_label = tk.Label(item_frame, text=text, font=("Arial", 16), fg="white", bg="black", anchor="w", justify="left")
    text_label.pack(side="left", padx=10, expand=True, fill="both")

    add_button = tk.Button(item_frame, text="Add to Cart", font=("Arial", 10, "bold"), bg="orange", fg="black", padx=12, pady=8, relief="ridge", borderwidth=2)
    add_button.config(command=lambda oid=order_id, name=dish_name, pr=price, btn=add_button: add_to_cart(oid, name, pr, restaurant_name, btn))
    add_button.pack(side="right", padx=10)

scroll_frame.update_idletasks()
scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

# Bottom Buttons
bottom_frame = tk.Frame(scroll_frame, bg="black")
bottom_frame.pack(pady=20)

checkout_button = tk.Button(bottom_frame, text="Checkout 🛒", font=("Arial", 14, "bold"), command=open_checkout, bg="#ff5f5f", fg="white", padx=20, pady=10, relief="ridge", borderwidth=2, width=15)
checkout_button.pack(side="left", padx=10)

exit_button = tk.Button(bottom_frame, text="⬅ Back", font=("Arial", 14, "bold"), command=open_resto, bg="#383838", fg="white", padx=20, pady=10, relief="ridge", borderwidth=2, width=15)
exit_button.pack(side="right", padx=10)

set_background()
root.mainloop()
