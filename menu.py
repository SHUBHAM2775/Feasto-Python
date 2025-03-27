import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import get_menu_items, add_to_cart_db  # Import Mongo insert function
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

# ✅ **Define Checkout Function**
def open_checkout():
    root.destroy()  # Close the current window
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
<<<<<<< HEAD
bg_image = Image.open("images/restobg3.png")
=======
bg_image = Image.open("images/restobg3.png")  
>>>>>>> menuscroll
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

<<<<<<< HEAD
# Positioning for menu items
y_position = 180
text_x = screen_width * 0.25
button_x = screen_width * 0.25
image_x = screen_width * 0.7
line_width = screen_width * 0.5
start_x = (screen_width - line_width) // 2 + 10
end_x = start_x + line_width - 20

image_refs = []
=======
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
>>>>>>> menuscroll

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
        padx=7, pady=7
    )

    # Button command with reference to the button itself
    add_button.config(command=lambda oid=order_id, name=dish_name, pr=price, btn=add_button: add_to_cart(oid, name, pr, restaurant_name, btn))

    canvas.create_window(
        button_x, y_position + 50,
        window=add_button,
        anchor="w",
        width=120, height=30
    )

    # Separator line
    canvas.create_line(
        start_x, y_position + 80, end_x, y_position + 80,
        fill="white", width=2
    )

    # Load and place image
    try:
        if os.path.exists(image_path):
            item_image = Image.open(image_path).resize((80, 80), Image.LANCZOS)
        else:
            print(f"Image not found for {dish_name}, using default image.")
            item_image = Image.open("images/default.jpg").resize((80, 80), Image.LANCZOS)

        item_photo = ImageTk.PhotoImage(item_image)
<<<<<<< HEAD
        image_refs.append(item_photo)
        canvas.create_image(image_x, y_position, image=item_photo, anchor="w")
=======
        image_refs.append(item_photo)  # Keep reference

        # Display image
        tk.Label(menu_frame, image=item_photo, bg="black").grid(row=y_position, column=2, padx=20, pady=10)
>>>>>>> menuscroll

    except Exception as e:
        print("Image load error:", e)

<<<<<<< HEAD
    y_position += 120

# ✅ **Checkout Button**
checkout_button = tk.Button(
    root, text="Checkout",
    font=("Arial", 14), command=open_checkout,
    bg="white", fg="black"
)

# ✅ **Back Button**
=======
    y_position += 1  # Move to the next row

# Update scroll region when new items are added
menu_frame.update_idletasks()
scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

# Enable scrolling with the mouse wheel
def on_mouse_wheel(event):
    scroll_canvas.yview_scroll(-1 * (event.delta // 120), "units")

root.bind_all("<MouseWheel>", on_mouse_wheel)

# ---------------- BUTTONS ----------------
>>>>>>> menuscroll
exit_button = tk.Button(
    root, text="Back to Restaurant Selection",
    font=("Arial", 14), command=open_resto,
    bg="orange", fg="black"
)

<<<<<<< HEAD
# Place Buttons on Canvas
canvas.create_window(
    screen_width // 2, screen_height - 100,
    window=checkout_button, width=300, height=40
=======
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
>>>>>>> menuscroll
)

canvas.create_window(
    #start_x + button_width + button_gap
    start_x + 300 + 200, screen_height - 100,
    window=exit_button, width=300, height=40
)

# Run the Tkinter loop
root.mainloop()
