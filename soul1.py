import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="soulshare"
    )

# Registration function
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    contact_number = contact_entry.get()

    if username and password:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password, email, contact_number) VALUES (%s, %s, %s, %s)",
                       (username, password, email, contact_number))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "User registered successfully!")
        clear_fields()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Clear input fields
def clear_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)

# Function to donate a product
def donate_product():
    product_name = product_name_entry.get()
    quantity = quantity_entry.get()
    photo_path = photo_entry.get()

    if product_name and quantity.isdigit():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO products (name, quantity, photo, donor_id) VALUES (%s, %s, %s, %s)",
                       (product_name, quantity, photo_path, 1))  # Assume donor_id is 1 for simplicity
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Product donated successfully!")
        clear_product_fields()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields correctly.")

# Clear product fields
def clear_product_fields():
    product_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    photo_entry.delete(0, tk.END)

# Function to browse for photo
def browse_photo():
    filename = filedialog.askopenfilename()
    photo_entry.insert(0, filename)

# Create the main window
app = tk.Tk()
app.title("SoulShare App")

# Registration Section
tk.Label(app, text="Register").grid(row=0, column=0, columnspan=2)
tk.Label(app, text="Username").grid(row=1, column=0)
username_entry = tk.Entry(app)
username_entry.grid(row=1, column=1)

tk.Label(app, text="Password").grid(row=2, column=0)
password_entry = tk.Entry(app, show='*')
password_entry.grid(row=2, column=1)

tk.Label(app, text="Email").grid(row=3, column=0)
email_entry = tk.Entry(app)
email_entry.grid(row=3, column=1)

tk.Label(app, text="Contact Number").grid(row=4, column=0)
contact_entry = tk.Entry(app)
contact_entry.grid(row=4, column=1)

tk.Button(app, text="Register", command=register_user).grid(row=5, column=0, columnspan=2)

# Donation Section
tk.Label(app, text="Donate Product").grid(row=6, column=0, columnspan=2)
tk.Label(app, text="Product Name").grid(row=7, column=0)
product_name_entry = tk.Entry(app)
product_name_entry.grid(row=7, column=1)

tk.Label(app, text="Quantity").grid(row=8, column=0)
quantity_entry = tk.Entry(app)
quantity_entry.grid(row=8, column=1)

tk.Label(app, text="Photo").grid(row=9, column=0)
photo_entry = tk.Entry(app)
photo_entry.grid(row=9, column=1)
tk.Button(app, text="Browse", command=browse_photo).grid(row=9, column=2)

tk.Button(app, text="Donate", command=donate_product).grid(row=10, column=0, columnspan=2)

app.mainloop()
