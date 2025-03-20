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

menu = StringVar()
menu.set("Select A Restaurant")

drop = ttk.Combobox(root, textvariable=menu, values=["MC'Donalds","Burger-King"], font=('Georgia', 18), justify="center", state = "readonly")
drop.place(x=600, y=175, width=300, height=40)

mcd = Image.open("images/mcd.png").resize((500, 500))
mcd_photo = ImageTk.PhotoImage(mcd)
canvas.create_image(200, 250, image=mcd_photo, anchor="nw")

burger_king = Image.open("images/burger-king.jpg").resize((500, 500))
burger_king_photo = ImageTk.PhotoImage(burger_king)
canvas.create_image(800, 250, image=burger_king_photo, anchor="nw")
root.mainloop()


#Note :- Search bar ka kuch karo ya fir nikalo isse