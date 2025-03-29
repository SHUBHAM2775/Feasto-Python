from PIL import Image, ImageTk
import tkinter as tk
from dbconnect import insert_user_entry, verify_user  # Import database functions

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

def login():
    """Verifies user credentials and opens restaurant selection page."""
    if not validate_input():
        return
    
    user_name = name.get().strip()
    mobile_number = mobile.get().strip()
    table_number = table.get().strip()

    # Verify user credentials (only name and mobile)
    if verify_user(user_name, mobile_number):
        print(f"✅ Login successful: {user_name}, {mobile_number}")
        # Store credentials in temporary file
        with open("current_user.txt", "w") as f:
            f.write(f"{user_name},{mobile_number},{table_number}")
        # Pass table number as command line argument
        root.destroy()
        import subprocess
        subprocess.Popen(["python", "resto.py", table_number])
    else:
        error_label.config(text="⚠️ Invalid credentials! Please try again or Sign up.")

def signup():
    """Saves new user data and clears the form."""
    if not validate_input():
        return
    
    user_name = name.get().strip()
    mobile_number = mobile.get().strip()
    table_number = table.get().strip()

    # Check if user already exists (only check name and mobile)
    if verify_user(user_name, mobile_number):
        error_label.config(text="⚠️ User already exists! Please login instead.")
        return

    # Save to database without table number
    insert_user_entry(user_name, mobile_number)
    print(f"✅ New user registered: {user_name}, {mobile_number}")

    # Clear all fields
    table.delete(0, tk.END)
    table.insert(0, "Enter Table Number")
    name.delete(0, tk.END)
    name.insert(0, "Enter Your Name")
    mobile.delete(0, tk.END)
    mobile.insert(0, "Enter Mobile Number")

    # Show success message
    error_label.config(text="✅ Signup successful! Please login to proceed.", fg="green")

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

# Login and Signup Buttons
login_btn = tk.Button(root, text="Login", font=('Arial', 16), bg="yellow", fg="black", command=login, width=10)
login_btn.place(relx=0.4, rely=0.7, anchor="center")

signup_btn = tk.Button(root, text="Signup", font=('Arial', 16), bg="yellow", fg="black", command=signup, width=10)
signup_btn.place(relx=0.6, rely=0.7, anchor="center")

root.mainloop()
