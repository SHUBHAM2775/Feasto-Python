import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import get_menu_items
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

def open_checkout():
    root.destroy()
    import checkout

# Dummy cart action
def add_to_cart(item_name):
    print(f"Added to cart: {item_name}")

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
bg_image = Image.open("images/restobg3.png")  
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create background canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.place(relwidth=1, relheight=1)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Title
canvas.create_text(
    screen_width // 2, 80,
    text=f"{restaurant_name} Menu",
    font=("Arial", 28, "bold"),
    fill="white"
)

# ---------------- SCROLLABLE TRANSPARENT MENU ----------------
frame_container = tk.Frame(root)
frame_container.place(relx=0.5, rely=0.5, anchor="center", width=screen_width * 0.8, height=screen_height * 0.7)

# Create a Canvas for scrolling (no background to appear "transparent")
scroll_canvas = tk.Canvas(frame_container, highlightthickness=0, bd=0) 
scroll_canvas.pack(side="left", fill="both", expand=True)

# Add a Scrollbar
scrollbar = tk.Scrollbar(frame_container, orient="vertical", command=scroll_canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure scrolling
scroll_canvas.configure(yscrollcommand=scrollbar.set)
scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

# Inner frame to hold menu items (match background with the canvas)
menu_frame = tk.Frame(scroll_canvas, bg="black")  # Make bg same as the canvas
scroll_window = scroll_canvas.create_window((0, 0), window=menu_frame, anchor="nw", width=screen_width * 0.75)

# ---------------- POPULATING MENU ITEMS ----------------
y_position = 20  # Start position inside menu frame
image_refs = []  # Keep references to images

for item in menu_items:
    order_id, dish_name, price, description, image_path = item
    wrapped_description = "\n".join(textwrap.wrap(description, width=75))
    text = f"#{order_id} {dish_name} - ${price}\n{wrapped_description}"

    # Display menu item text
    tk.Label(
        menu_frame,
        text=text,
        font=("Arial", 16),
        fg="white",
        bg="black",  # Set to match background
        anchor="w",
        justify="left"
    ).grid(row=y_position, column=0, padx=20, pady=10, sticky="w")

    # Add to Cart Button
    add_button = tk.Button(
        menu_frame,
        text="Add to Cart",
        font=("Arial", 10, "bold"),
        bg="orange",
        fg="black",
        padx=7, pady=7,
        command=lambda name=dish_name: add_to_cart(name)
    )
    add_button.grid(row=y_position, column=1, padx=20, pady=10, sticky="w")

    # Load item-specific image
    try:
        if os.path.exists(image_path):
            item_image = Image.open(image_path).resize((80, 80), Image.LANCZOS)
        else:
            print(f"Image not found for {dish_name}, using default image.")
            item_image = Image.open("images/default.jpg").resize((80, 80), Image.LANCZOS)

        item_photo = ImageTk.PhotoImage(item_image)
        image_refs.append(item_photo)  # Keep reference

        # Display image
        tk.Label(menu_frame, image=item_photo, bg="black").grid(row=y_position, column=2, padx=20, pady=10)

    except Exception as e:
        print("Image load error:", e)

    y_position += 1  # Move to the next row

# Update scroll region when new items are added
menu_frame.update_idletasks()
scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

# Enable scrolling with the mouse wheel
def on_mouse_wheel(event):
    scroll_canvas.yview_scroll(-1 * (event.delta // 120), "units")

root.bind_all("<MouseWheel>", on_mouse_wheel)

# ---------------- BUTTONS ----------------
exit_button = tk.Button(
    root, text="Back to Restaurant Selection",
    font=("Arial", 14), command=open_resto,
    bg="orange", fg="black"
)

checkout = tk.Button(
    root, text="Checkout",
    font=("Arial", 14), command=open_checkout,
    bg="orange", fg="black"
)


total_width = (2 * 300) + 50  # total_width = (2 * button_width) + button_gap
start_x = (screen_width - total_width) // 2

canvas.create_window(
    start_x + 100, screen_height - 100,
    window=checkout, width=300, height=40
)

canvas.create_window(
    #start_x + button_width + button_gap
    start_x + 300 + 200, screen_height - 100,
    window=exit_button, width=300, height=40
)

# Run the Tkinter loop
root.mainloop()
