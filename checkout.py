import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import get_restaurants

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

# Get the screen width and height
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

# Display Restaurant Name from Database
canvas.create_text(
    screen_width // 4, 175,  # Positioned below "Secure Checkout"
    text=f"{restaurant_name}",
    font=("Georgia", 24, "bold"),
    fill="yellow"
)

root.mainloop()
