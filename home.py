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

def validate_input():
    """Validates user inputs."""
    table_number = table.get().strip()
    user_name = name.get().strip()
    mobile_number = mobile.get().strip()

    # Validate table number (numeric only)
    if not table_number.isdigit():
        error_label.config(text="⚠️ Invalid Table Number! Must be numeric.")
        return False
    
    # Validate user name (alphabetic only)
    if not user_name.replace(" ", "").isalpha():
        error_label.config(text="⚠️ Invalid Name! Must contain only letters.")
        return False
    
    # Validate mobile number (exactly 10 digits)
    if not (mobile_number.isdigit() and len(mobile_number) == 10):
        error_label.config(text="⚠️ Invalid Mobile Number! Must be 10 digits.")
        return False
    
    error_label.config(text="")  # Clear error if validation passes
    return True

def submit_entry():
    """Saves user data and moves to the restaurant selection page."""
    if not validate_input():
        return
    
    table_number = table.get().strip()
    user_name = name.get().strip()
    mobile_number = mobile.get().strip()

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

# Error Label
error_label = tk.Label(root, text="", font=('Arial', 14), fg="red", bg="black")
error_label.place(relx=0.5, rely=0.65, anchor="center")

# Submit Button
submit = tk.Button(root, text="Submit", font=('Arial', 16), bg="yellow", fg="black", command=submit_entry, width=10)
submit.place(relx=0.5, rely=0.7, anchor="center")

root.mainloop()
