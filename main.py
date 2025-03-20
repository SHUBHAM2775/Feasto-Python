import tkinter as tk
from PIL import Image, ImageTk
import time

def open_home():
    root.destroy()
    import home

root = tk.Tk()
root.title("Feasto")
root.state('zoomed')  # Fullscreen with minimize & close button

bg_image = Image.open("images/homescreen.png")
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# square_image = Image.open("images/homescreen.png")  
# square_image = square_image.resize((150, 150))
# square_photo = ImageTk.PhotoImage(square_image)
# square_label = tk.Label(root, image=square_photo, compound="center",font=("Arial", 16, "bold"), fg="white", bg="black", padx=10,pady=10)
# square_label.place(relx=0.5, rely=0.5, anchor="center")

root.after(3000, open_home)  # Wait for 3 seconds before opening home.py

root.mainloop()

