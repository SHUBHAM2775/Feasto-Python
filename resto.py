import tkinter as tk
from tkinter import StringVar
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Feasto")
root.state('zoomed')  # Fullscreen mode

def clear_placeholder(event):
    if event.widget.get() == "Search for a dish":
        event.widget.delete(0, tk.END)

# Get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize the background image
bg_image = Image.open("images/restobg3.png").resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

# Create canvas and add background
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Search bar
search_bar = tk.Entry(root, width=70, font=('Arial', 16), bg="grey", fg="black")
search_bar.insert(0, "Search for a dish")
search_bar.bind("<FocusIn>", clear_placeholder)
search_bar.place(x=350, y=100)

# Dropdown menu (Centered on screen + Centered Text)
menu = StringVar()
menu.set("Select A Restaurant")

drop = ttk.Combobox(root, textvariable=menu, values=["Resto1","Resto2"], font=('Georgia', 18), justify="center", state = "readonly")
drop.place(x=600, y=200, width=300, height=40)

test = tk.Entry(root,text="Enter Table Number",width=35, font=('Arial', 16), bg="grey", fg="black")
test.place(x=600, y=300)

root.mainloop()
