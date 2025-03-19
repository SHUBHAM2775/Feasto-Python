from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.title("Feasto")
root.state('zoomed')

def clear_placeholder(event):
    if event.widget.get() in ["Enter Table Number", "Enter Your Name", "Enter Mobile Number"]:
        event.widget.delete(0, tk.END)
        
def open_resto():
    root.destroy()
    import resto

bg_image = Image.open("images/restobg2.png")
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Vertical Line
line_x = 400  
canvas.create_line(line_x, 0, line_x, root.winfo_screenheight(), fill="white", width=2)

table = tk.Entry(root,width=35, font=('Arial', 16), bg="grey", fg="black")
table.insert(0, "Enter Table Number")  # Placeholder text
table.bind("<FocusIn>", clear_placeholder)  # Clears text on click
table.place(x=600, y=300)

name = tk.Entry(root,width=35, font=('Arial', 16), bg="grey", fg="black")
name.insert(0, "Enter Your Name")  # Placeholder text
name.bind("<FocusIn>", clear_placeholder)  # Clears text on click
name.place(x=600, y=400)


mobile = tk.Entry(root,width=35, font=('Arial', 16), bg="grey", fg="black")
mobile.insert(0, "Enter Mobile Number")  # Placeholder text
mobile.bind("<FocusIn>", clear_placeholder)  # Clears text on click
mobile.place(x=600, y=500)

submit = tk.Button(root, text="Submit", font=('Arial', 16), bg="yellow", fg="black", command=open_resto,width=10)
submit.place(x=750, y=575)
root.mainloop()