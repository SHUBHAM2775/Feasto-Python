from PIL import Image, ImageTk
import tkinter as tk
from dbconnect import insert_user_entry  # Import database function

# Initialize Tkinter
root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

# Load background image and set it as full-screen background
bg_image = Image.open("images/homebg.png")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

def clear_placeholder(event):
    """Clears placeholder text when user clicks inside the entry field."""
    if event.widget.get() in ["Enter Table Number", "Enter Your Name", "Enter Mobile Number"]:
        event.widget.delete(0, tk.END)

def submit_entry():
    """Saves user data and moves to the restaurant selection page."""
    table_number = table.get().strip()
    user_name = name.get().strip()
    mobile_number = mobile.get().strip()

    # Validate inputs
    if not table_number or table_number == "Enter Table Number":
        print("⚠️ Please enter a valid table number!")
        return
    if not user_name or user_name == "Enter Your Name":
        print("⚠️ Please enter a valid name!")
        return
    if not mobile_number or mobile_number == "Enter Mobile Number":
        print("⚠️ Please enter a valid mobile number!")
        return

    # Save to database
    insert_user_entry(table_number, user_name, mobile_number)
    print(f"✅ Entry saved: {table_number}, {user_name}, {mobile_number}")

    # Open the restaurant selection page
    root.destroy()  
    import resto  

# Entry Fields

table = tk.Entry(root, width=35, font=('Arial', 16), bg="grey", fg="black")
table.insert(0, "Enter Table Number")  
table.bind("<FocusIn>", clear_placeholder)  
table.place(relx=0.5, rely=0.4, anchor="center")

name = tk.Entry(root, width=35, font=('Arial', 16), bg="grey", fg="black")
name.insert(0, "Enter Your Name")  
name.bind("<FocusIn>", clear_placeholder)  
name.place(relx=0.5, rely=0.5, anchor="center")

mobile = tk.Entry(root, width=35, font=('Arial', 16), bg="grey", fg="black")
mobile.insert(0, "Enter Mobile Number")  
mobile.bind("<FocusIn>", clear_placeholder)  
mobile.place(relx=0.5, rely=0.6, anchor="center")

# Submit Button
submit = tk.Button(root, text="Submit", font=('Arial', 16), bg="yellow", fg="black", command=submit_entry, width=10)
submit.place(relx=0.5, rely=0.7, anchor="center")

root.mainloop()
