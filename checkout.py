import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import get_restaurants, get_cart_items, update_cart_quantity  # Import cart functions

# Initialize Tkinter
root = tk.Tk()
root.title("Feasto")
root.state('zoomed')  # Fullscreen mode

# Fetch restaurants
restaurants = get_restaurants()
restaurant_names = list(restaurants.keys())

# Check if a restaurant is provided via command-line arguments
if len(sys.argv) > 1:
    restaurant_name = sys.argv[1]  # Take name from command-line
else:
    restaurant_name = "Domino's"  # Default for testing

# Fetch cart items from MongoDB
cart_items = get_cart_items(restaurant_name)  # Fetch items from cart collection

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize background image
bg_image = Image.open("images/restobg3.png").resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Display "Secure Checkout" title
canvas.create_text(
    screen_width // 2, 100,
    text="Secure Checkout",
    font=("Georgia", 28, "bold"),
    fill="white"
)

# Display Restaurant Name
canvas.create_text(
    screen_width // 4, 175,  # Positioned below "Secure Checkout"
    text=f"{restaurant_name}",
    font=("Georgia", 24, "bold"),
    fill="yellow"
)

# **Display Cart Items**
y_position = 250  # Start listing items below the restaurant name
line_width = screen_width * 0.4
start_x = (screen_width - line_width) // 2
end_x = start_x + line_width

# Dictionary to store label references for quantity updates
quantity_labels = {}
item_frames = {}

# Proper Alignment Positions
dish_x = screen_width * 0.35  # Dish name position
button_x = screen_width * 0.55  # Align buttons in one column

def update_quantity_label(dish_name, new_quantity):
    """Update the quantity display dynamically or remove the item."""
    if new_quantity > 0:
        quantity_labels[dish_name].config(text=str(new_quantity))
    else:
        # Remove item from the screen
        item_frames[dish_name].destroy()
        del item_frames[dish_name]
        del quantity_labels[dish_name]

def increase_quantity(dish_name):
    """Increase item quantity in MongoDB and update UI."""
    new_quantity = update_cart_quantity(restaurant_name, dish_name, 1)
    update_quantity_label(dish_name, new_quantity)

def decrease_quantity(dish_name):
    """Decrease item quantity in MongoDB and update UI."""
    new_quantity = update_cart_quantity(restaurant_name, dish_name, -1)
    update_quantity_label(dish_name, new_quantity)

if cart_items:
    for dish_name, quantity in cart_items:
        # Create frame for each cart item
        item_frame = tk.Frame(root, bg="black")
        item_frame.place(x=start_x, y=y_position, width=screen_width * 0.5, height=50)

        # Dish name label (aligned to left)
        dish_label = tk.Label(item_frame, text=dish_name, font=("Arial", 16), fg="white", bg="black", anchor="w", width=30)
        dish_label.pack(side="left", padx=10)

        # "-" Button
        minus_button = tk.Button(item_frame, text="-", font=("Arial", 12, "bold"), bg="red", fg="white",
                                 command=lambda name=dish_name: decrease_quantity(name), width=3)
        minus_button.pack(side="left", padx=10)

        # Quantity Label (Centered between + and -)
        quantity_label = tk.Label(item_frame, text=str(quantity), font=("Arial", 16), fg="white", bg="black", width=5)
        quantity_label.pack(side="left", padx=10)
        quantity_labels[dish_name] = quantity_label

        # "+" Button
        plus_button = tk.Button(item_frame, text="+", font=("Arial", 12, "bold"), bg="green", fg="white",
                                command=lambda name=dish_name: increase_quantity(name), width=3)
        plus_button.pack(side="left", padx=10)

        item_frames[dish_name] = item_frame  # Store reference to remove later

        y_position += 60  # Move down for the next item
else:
    canvas.create_text(
        screen_width // 2, y_position,
        text="Your cart is empty",
        font=("Arial", 18),
        fill="red"
    )

root.mainloop()
