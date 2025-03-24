from PIL import Image, ImageTk
import tkinter as tk
from dbconnect import insert_user_entry  # Import database function

# Initialize Tkinter
root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

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

# Load background image
bg_image = Image.open("images/restobg2.png")
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Vertical Line
line_x = 400  
canvas.create_line(line_x, 0, line_x, root.winfo_screenheight(), fill="white", width=2)

# Entry Fields
table = tk.Entry(root, width=35, font=('Arial', 16), bg="grey", fg="black")
table.insert(0, "Enter Table Number")  
table.bind("<FocusIn>", clear_placeholder)  
table.place(x=600, y=300)

name = tk.Entry(root, width=35, font=('Arial', 16), bg="grey", fg="black")
name.insert(0, "Enter Your Name")  
name.bind("<FocusIn>", clear_placeholder)  
name.place(x=600, y=400)

mobile = tk.Entry(root, width=35, font=('Arial', 16), bg="grey", fg="black")
mobile.insert(0, "Enter Mobile Number")  
mobile.bind("<FocusIn>", clear_placeholder)  
mobile.place(x=600, y=500)

# Submit Button
submit = tk.Button(root, text="Submit", font=('Arial', 16), bg="yellow", fg="black", command=submit_entry, width=10)
submit.place(x=750, y=575)

root.mainloop()
