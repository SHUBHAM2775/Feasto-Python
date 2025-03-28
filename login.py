import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from dbconnect import get_all_user_entries  # Import the database function

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

canvas.create_text(screen_width/2, 100, text="Login", font=("Arial", 28, "bold"), fill="white")

# Create entry fields with white background
username_label = canvas.create_text(screen_width/2 - 100, 200, text="Username:", font=("Arial", 14), fill="white")
username_entry = Entry(root, font=("Arial", 12))
username_window = canvas.create_window(screen_width/2 + 50, 200, window=username_entry, width=200)

phone_label = canvas.create_text(screen_width/2 - 100, 250, text="Phone Number:", font=("Arial", 14), fill="white")
phone_entry = Entry(root, font=("Arial", 12))
phone_window = canvas.create_window(screen_width/2 + 70, 250, window=phone_entry, width=200)

def verify_login():
    username = username_entry.get()
    phone = phone_entry.get()
    
    # Get all users from database
    users = get_all_user_entries()
    
    # Check if user exists
    for user in users:
        if user['name'] == username and user['mobile'] == phone:
            messagebox.showinfo("Success", "Login Successful!")
            root.destroy()  # Close login window
            return
    
    messagebox.showerror("Error", "Invalid username or phone number")

# Create login button
login_button = tk.Button(root, text="Login", command=verify_login, font=("Arial", 12), bg="#4CAF50", fg="white")
login_button_window = canvas.create_window(screen_width/2, 300, window=login_button)

root.mainloop()
