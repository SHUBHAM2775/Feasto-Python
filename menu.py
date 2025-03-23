import tkinter as tk
import sys
from PIL import Image, ImageTk

# Get restaurant name and menu items from command-line arguments
restaurant_name = sys.argv[1]
menu_items = sys.argv[2:]

# Create menu window
root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

# Function to open home.py
def open_home():
    root.destroy()
    import resto

# Get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and display background
bg_image = Image.open("images/restobg3.png").resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Menu title
title_label = tk.Label(root, text=f"{restaurant_name} Menu", font=("Arial", 20, "bold"), bg="white")
canvas.create_window(screen_width // 2, 50, window=title_label, anchor="center")

# Display menu items
y_position = 150
for item in menu_items:
    menu_label = tk.Label(root, text=f"• {item}", font=("Arial", 16), bg="white")
    canvas.create_window(screen_width // 2, y_position, window=menu_label, anchor="center")
    y_position += 40  # Spacing between items

exit = tk.Button(root, text="Back to Selection", font=("Arial", 14), command=open_home)
exit.place(relx=0.5, rely=0.9, anchor="center", width=150, height=40)

root.mainloop()
