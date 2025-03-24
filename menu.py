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
bg_image = Image.open("images/restobg3.png")  # Replace with your own path
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

# Positioning for menu items
y_position = 180
text_x = screen_width * 0.25  # Adjust text position
button_x = screen_width * 0.25  # Align button under text
image_x = screen_width * 0.7  # Place images on the right
line_width = screen_width * 0.5  # Half screen width
start_x = (screen_width - line_width) // 2 + 10  # Add 10px padding
end_x = start_x + line_width - 20  # Add 10px padding on both sides

image_refs = []  # Keep references to images

for item in menu_items:
    order_id, dish_name, price, description, image_path = item
    wrapped_description = "\n".join(textwrap.wrap(description, width=85))  # Increased wrap width to 85 chars per line
    text = f"#{order_id} {dish_name} - ${price}\n{wrapped_description}"

    # Display menu item text
    canvas.create_text(
        text_x, y_position,
        text=text,
        font=("Arial", 16),
        fill="white",
        anchor="w"
    )

    # Add to Cart Button with padding
    add_button = tk.Button(
        root,
        text="Add to Cart",
        font=("Arial", 10, "bold"),
        bg="orange",
        fg="black",
        padx=7, pady=7,  # Add 7px padding around the button
        command=lambda name=dish_name: add_to_cart(name)
    )
    canvas.create_window(
        button_x, y_position + 50,
        window=add_button,
        anchor="w",
        width=120, height=30
    )

    # Separator line with padding
    canvas.create_line(
        start_x, y_position + 80, end_x, y_position + 80,
        fill="white", width=2
    )

    # Load item-specific image
    try:
        if os.path.exists(image_path):
            item_image = Image.open(image_path).resize((80, 80), Image.LANCZOS)
        else:
            print(f"Image not found for {dish_name}, using default image.")
            item_image = Image.open("images/default.jpg").resize((80, 80), Image.LANCZOS)

        item_photo = ImageTk.PhotoImage(item_image)
        image_refs.append(item_photo)  # Keep a reference

        # Place image with **equal spacing above & below the line**
        canvas.create_image(
            image_x, y_position,
            image=item_photo,
            anchor="w"
        )
    except Exception as e:
        print("Image load error:", e)

    y_position += 120  # Increase spacing for multi-line descriptions

# Back Button
exit_button = tk.Button(
    root, text="Back to Restaurant Selection",
    font=("Arial", 14), command=open_resto,
    bg="white", fg="black"
)
canvas.create_window(
    screen_width // 2, screen_height - 100,
    window=exit_button, width=300, height=40
)

# Run the Tkinter loop
root.mainloop()
# 