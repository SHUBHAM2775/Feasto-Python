import tkinter as tk
from PIL import Image, ImageTk
import sys
from dbconnect import get_menu_items

root = tk.Tk()

root.title("Feasto")
root.state('zoomed')  # Fullscreen with minimize & close button

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Open and resize the background image to fit the screen
bg_image = Image.open("images/restobg3.png")
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)  # ✅ FIXED: Use LANCZOS instead of ANTIALIAS
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(
    screen_width // 2, 100,
    text="Secure Checkout",
    font=("Georgia", 28, "bold"),
    fill="white"
)

canvas.create_text(
    screen_width // 2, 100,
    text="Secure Checkout",
    font=("Georgia", 28, "bold"),
    fill="white"
)

canvas.create_text(
    screen_width // 2, 100,
    text="Secure Checkout",
    font=("Georgia", 28, "bold"),
    fill="white"
)

root.mainloop()