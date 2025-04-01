import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import get_restaurants, get_cart_items, update_cart_quantity  # Import cart functions
import subprocess

# Get table number from command line arguments
table_number = sys.argv[2] if len(sys.argv) > 2 else "N/A"  # Since restaurant name is argv[1]

# Initialize Tkinter
root = tk.Tk()
root.title("Feasto")
root.state('zoomed')  # Fullscreen mode

def open_bill():
    root.destroy()
    subprocess.Popen(["python", "bill.py", table_number])

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

# After canvas creation and before "Secure Checkout" title
# Add user profile button
user_icon_size = 150
user_icon_x = user_icon_size // 2 + 20
user_icon_y = user_icon_size // 2 + 20

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

def open_user():
    root.destroy()
    import subprocess
    subprocess.Popen(["python", "user.py", "checkout", table_number])

# Make the canvas clickable
user_canvas.bind("<Button-1>", lambda event: open_user())

# Display "Secure Checkout" title
canvas.create_text(
    screen_width // 2, 80,
    text="Secure Checkout",
    font=("Georgia", 28, "bold"),
    fill="white"
)

# Display Restaurant Name
canvas.create_text(
    screen_width // 4, 155,
    text=f"{restaurant_name}",
    font=("Georgia", 24, "bold"),
    fill="orange"
)

# **Display Cart Items**
y_position = 230  # Start listing items below the restaurant name
line_width = screen_width * 0.4
start_x = (screen_width - line_width) // 2
end_x = start_x + line_width

# Dictionary to store label references for quantity updates
quantity_labels = {}
item_frames = {}
canvas_items = {}  # Store canvas items for removal

# Proper Alignment Positions
dish_x = screen_width * 0.35  # Dish name position
button_x = screen_width * 0.55  # Align buttons in one column

def update_quantity_label(dish_name, new_quantity):
    """Update the quantity display dynamically or remove the item."""
    if new_quantity > 0:
        quantity_labels[dish_name].config(text=str(new_quantity))
    else:
        # Remove all widgets and canvas items for this dish
        for widget in item_frames[dish_name].values():
            if isinstance(widget, tk.Widget):
                widget.destroy()
        
        # Remove canvas items (rectangle and text)
        for item_id in canvas_items[dish_name]:
            canvas.delete(item_id)
        
        # Clean up references
        del item_frames[dish_name]
        del quantity_labels[dish_name]
        del canvas_items[dish_name]
        
        # Check if cart is empty after removal
        if not item_frames:
            canvas.create_text(
                screen_width // 2, y_position,
                text="Your cart is empty",
                font=("Arial", 18),
                fill="red"
            )

def increase_quantity(dish_name):
    """Increase item quantity in MongoDB and update UI."""
    new_quantity = update_cart_quantity(restaurant_name, dish_name, 1)
    update_quantity_label(dish_name, new_quantity)

def decrease_quantity(dish_name):
    """Decrease item quantity in MongoDB and update UI."""
    new_quantity = update_cart_quantity(restaurant_name, dish_name, -1)
    update_quantity_label(dish_name, new_quantity)

if cart_items:
    # Calculate number of items and split into two columns if needed
    num_items = len(cart_items)
    items_per_column = (num_items + 1) // 2  # Round up for odd number of items
    
    # Calculate column widths and starting positions
    column_width = screen_width * 0.25
    left_start_x = screen_width * 0.15
    right_start_x = screen_width * 0.60
    
    # Display items in two columns
    for index, (dish_name, quantity) in enumerate(cart_items):
        # Determine which column this item belongs to
        if index < items_per_column:
            current_x = left_start_x
            current_y = y_position + (index * 60)
        else:
            current_x = right_start_x
            current_y = y_position + ((index - items_per_column) * 60)
        
        # Create a semi-transparent black rectangle for the background
        rect_id = canvas.create_rectangle(
            current_x, current_y,
            current_x + column_width, current_y + 50,
            fill="black",
            stipple="gray50"
        )

        # Dish name
        text_id = canvas.create_text(
            current_x + 15, current_y + 25,
            text=dish_name,
            font=("Arial", 16),
            fill="white",
            anchor="w"
        )

        # Store canvas items for this dish
        canvas_items[dish_name] = [rect_id, text_id]

        # Create a frame for quantity controls
        control_frame = tk.Frame(root, bg="black")
        control_frame.place(x=current_x + column_width, y=current_y + 10)

        # "-" Button
        minus_button = tk.Button(control_frame, text="-", font=("Arial", 12, "bold"), 
                               bg="red", fg="white",
                               command=lambda name=dish_name: decrease_quantity(name), 
                               width=3)
        minus_button.pack(side="left", padx=5)

        # Quantity Label
        quantity_label = tk.Label(control_frame, text=str(quantity), 
                                font=("Arial", 16), fg="white", 
                                bg="black", width=3)
        quantity_label.pack(side="left", padx=5)
        quantity_labels[dish_name] = quantity_label

        # "+" Button
        plus_button = tk.Button(control_frame, text="+", font=("Arial", 12, "bold"), 
                              bg="green", fg="white",
                              command=lambda name=dish_name: increase_quantity(name), 
                              width=3)
        plus_button.pack(side="left", padx=5)

        # Store the widgets for potential removal
        item_frames[dish_name] = {
            'minus': minus_button,
            'plus': plus_button,
            'quantity': quantity_label,
            'frame': control_frame
        }
else:
    canvas.create_text(
        screen_width // 2, y_position,
        text="Your cart is empty",
        font=("Arial", 18),
        fill="red"
    )
    
    
proceed_button = tk.Button(root, text="Proceed to Payment", font=("Arial", 16), bg="green", fg="white", command=open_bill)
proceed_button.place(x=700 ,y=750, width=screen_width * 0.2, height=50)

root.mainloop()
