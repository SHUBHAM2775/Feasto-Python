import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import get_menu_items

root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

def open_resto():
    root.destroy()
    import resto

# Default values for testing
if len(sys.argv) < 2:
    restaurant_name = "Test Restaurant"
    menu_items = [
        (1, "Burger", 5.99, "Juicy grilled beef burger"),
        (2, "Pizza", 8.99, "Cheesy Margherita pizza"),
        (3, "Pasta", 6.49, "Creamy Alfredo pasta"),
    ]  # Example items for testing
else:
    restaurant_name = sys.argv[1]
    menu_items = get_menu_items(restaurant_name)  # Fetch from MongoDB

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize background image while keeping aspect ratio
bg_image = Image.open("images/restobg3.png")
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas for background and text
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

# Place the background image
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Title Label (Transparent Effect)
canvas.create_text(
    screen_width // 2, 100,
    text=f"{restaurant_name} Menu",
    font=("Arial", 24, "bold"),
    fill="white"
)

# Display menu items with separator lines
y_position = 200
line_width = screen_width // 2  # Half of the screen width
start_x = (screen_width - line_width) // 2  # Center the line

for item in menu_items:
    order_id, dish_name, price, description = item
    text = f"#{order_id} {dish_name} - ${price}\n{description}"

    # Draw transparent text
    canvas.create_text(
        screen_width * 0.3, y_position,
        text=text,
        font=("Arial", 16),
        fill="white",
        anchor="w"
    )

    # Separator line
    canvas.create_line(start_x, y_position + 20, start_x + line_width, y_position + 20, fill="white", width=2)

    y_position += 80  # Increase spacing for next item

exit = tk.Button(root, text="Back to Restaurant Selection", font=("Arial", 14), command=open_resto)
exit.place(relx=0.5, y=screen_height-100, anchor="center", width=300, height=40)

root.mainloop()
# 