import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk

# Database setup
conn = sqlite3.connect('app_data.db')
cursor = conn.cursor()

# Creating tables for users and products
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    email TEXT,
                    contact TEXT,
                    aadhar TEXT,
                    photo TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT,
                    photo TEXT,
                    quantity INTEGER,
                    email TEXT,
                    contact TEXT,
                    city TEXT,
                    district TEXT,
                    pincode TEXT)''')

conn.commit()

# Tkinter App
root = tk.Tk()
root.geometry("800x600")
root.title("SoulShare App")

# Clear Frame Function
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Login Page
def login_page():
    clear_frame()
    
    tk.Label(root, text="Login", font=("Arial", 20)).pack(pady=20)
    
    tk.Label(root, text="Username:").pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    
    tk.Label(root, text="Password:").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    
    def login():
        username = username_entry.get()
        password = password_entry.get()
        
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        
        if user:
            messagebox.showinfo("Success", "Login successful!")
            home_page()  # Proceed to the homepage after successful login
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    tk.Button(root, text="Login", command=login).pack(pady=20)
    tk.Button(root, text="Register", command=register_page).pack()

# Registration Page
def register_page():
    clear_frame()
    
    tk.Label(root, text="Register", font=("Arial", 20)).pack(pady=20)
    
    tk.Label(root, text="Username:").pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    
    tk.Label(root, text="Password:").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    
    tk.Label(root, text="Confirm Password:").pack()
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack(pady=5)
    
    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)
    
    tk.Label(root, text="Contact Number:").pack()
    contact_entry = tk.Entry(root)
    contact_entry.pack(pady=5)
    
    tk.Label(root, text="Aadhar Proof:").pack()
    aadhar_entry = tk.Entry(root)
    aadhar_entry.pack(pady=5)
    
    def register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        email = email_entry.get()
        contact = contact_entry.get()
        aadhar = aadhar_entry.get()
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        # Insert user data into the database
        cursor.execute('''INSERT INTO users (username, password, email, contact, aadhar, photo)
                          VALUES (?, ?, ?, ?, ?, ?)''', (username, password, email, contact, aadhar, "default.jpg"))
        conn.commit()
        
        messagebox.showinfo("Success", "Registration successful!")
        login_page()  # Redirect to login after registration
    
    tk.Button(root, text="Register", command=register).pack(pady=20)

# Homepage with Donate and Search Tab
def home_page():
    clear_frame()
    
    # Adding the "Donate" button at the top right
    donate_button = tk.Button(root, text="Donate Product", command=add_product)
    donate_button.pack(anchor='ne', padx=10, pady=10)
    
    tk.Label(root, text="Welcome to SoulShare", font=("Arial", 20)).pack(pady=20)
    
    # Search tab
    search_frame = tk.Frame(root)
    search_frame.pack(pady=10, padx=10, anchor='w')
    
    tk.Label(search_frame, text="Search for Products:").pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    def search_products():
        search_query = search_entry.get()
        display_products(search_query)
    
    tk.Button(search_frame, text="Search", command=search_products).pack(side=tk.LEFT, padx=10)
    
    # Display products initially (all products)
    display_products()

# Adding Product (Donate Page)
def add_product():
    clear_frame()
    
    tk.Label(root, text="Add a New Product", font=("Arial", 20)).pack(pady=20)
    
    tk.Label(root, text="Product Name:").pack()
    product_name_entry = tk.Entry(root)
    product_name_entry.pack(pady=5)
    
    tk.Label(root, text="Photo:").pack()
    photo_entry = tk.Entry(root)
    photo_entry.pack(pady=5)
    
    tk.Button(root, text="Browse", command=lambda: browse_image(photo_entry)).pack(pady=5)
    
    tk.Label(root, text="Quantity:").pack()
    quantity_entry = tk.Entry(root)
    quantity_entry.pack(pady=5)
    
    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)
    
    tk.Label(root, text="Contact Number:").pack()
    contact_entry = tk.Entry(root)
    contact_entry.pack(pady=5)
    
    tk.Label(root, text="City:").pack()
    city_entry = tk.Entry(root)
    city_entry.pack(pady=5)
    
    tk.Label(root, text="District:").pack()
    district_entry = tk.Entry(root)
    district_entry.pack(pady=5)
    
    tk.Label(root, text="Pincode:").pack()
    pincode_entry = tk.Entry(root)
    pincode_entry.pack(pady=5)
    
    def save_product():
        product_name = product_name_entry.get()
        photo = photo_entry.get()
        quantity = quantity_entry.get()
        email = email_entry.get()
        contact = contact_entry.get()
        city = city_entry.get()
        district = district_entry.get()
        pincode = pincode_entry.get()
        
        # Insert product data into the database
        cursor.execute('''INSERT INTO products (product_name, photo, quantity, email, contact, city, district, pincode)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (product_name, photo, quantity, email, contact, city, district, pincode))
        conn.commit()
        
        messagebox.showinfo("Success", "Product added successfully!")
        home_page()  # Redirect to homepage after adding the product
    
    tk.Button(root, text="Add Product", command=save_product).pack(pady=20)
    tk.Button(root, text="Back to Home", command=home_page).pack(pady=10)

# Browse Image Function
def browse_image(entry):
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    entry.delete(0, tk.END)  # Clear the entry
    entry.insert(0, filename)  # Insert the selected file path

# Display Products
def display_products(search_query=""):
    # Clear any previous product display
    for widget in root.pack_slaves():
        if isinstance(widget, tk.Frame) and widget != root.winfo_children()[1]:  # Exclude the search frame
            widget.destroy()
    
    product_frame = tk.Frame(root)
    product_frame.pack(pady=20)
    
    tk.Label(product_frame, text="Products").grid(row=0, column=0)
    tk.Label(product_frame, text="Quantity").grid(row=0, column=1)
    tk.Label(product_frame, text="Order").grid(row=0, column=2)
    
    # Fetch products from the database (filtered by search query)
    if search_query:
        cursor.execute("SELECT * FROM products WHERE product_name LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM products")
    
    products = cursor.fetchall()
    
    if products:
        for index, product in enumerate(products, start=1):
            tk.Label(product_frame, text=product[1]).grid(row=index, column=0)  # Product name
            
            # Add product image
            try:
                product_image = Image.open(product[2])  # Use Pillow to open the image
                product_image = product_image.resize((50, 50))  # Resize image if necessary
                product_image_tk = ImageTk.PhotoImage(product_image)  # Convert to PhotoImage for Tkinter
                image_label = tk.Label(product_frame, image=product_image_tk)
                image_label.image = product_image_tk  # Keep a reference to avoid garbage collection
                image_label.grid(row=index, column=1)  # Display image
            except Exception as e:
                print("Image load error:", e)
                tk.Label(product_frame, text="No Image").grid(row=index, column=1)  # Fallback if image fails
            
            order_button = tk.Button(product_frame, text="Order", command=lambda p=product: order_product(p))
            order_button.grid(row=index, column=2)  # Order button

# Order Product (Order Page)
def order_product(product):
    clear_frame()
    
    tk.Label(root, text="Order Product", font=("Arial", 20)).pack(pady=20)
    
    # Create a scrollable frame for the order details
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Display product details
    tk.Label(scrollable_frame, text="Product Name: " + product[1]).pack(pady=5)
    
    # Radio buttons for individual/organization
    user_type = tk.StringVar(value="individual")
    
    tk.Radiobutton(scrollable_frame, text="Individual", variable=user_type, value="individual", command=lambda: toggle_organization_fields(scrollable_frame)).pack(anchor=tk.W)
    tk.Radiobutton(scrollable_frame, text="Organization", variable=user_type, value="organization", command=lambda: toggle_organization_fields(scrollable_frame)).pack(anchor=tk.W)
    
    # Individual details
    tk.Label(scrollable_frame, text="Name:").pack()
    individual_name_entry = tk.Entry(scrollable_frame)
    individual_name_entry.pack(pady=5)
    
    tk.Label(scrollable_frame, text="City:").pack()
    city_entry = tk.Entry(scrollable_frame)
    city_entry.pack(pady=5)
    
    tk.Label(scrollable_frame, text="District:").pack()
    district_entry = tk.Entry(scrollable_frame)
    district_entry.pack(pady=5)
    
    tk.Label(scrollable_frame, text="Address:").pack()
    address_entry = tk.Entry(scrollable_frame)
    address_entry.pack(pady=5)
    
    tk.Label(scrollable_frame, text="Pincode:").pack()
    pincode_entry = tk.Entry(scrollable_frame)
    pincode_entry.pack(pady=5)
    
    tk.Label(scrollable_frame, text="Phone Number:").pack()
    phone_entry = tk.Entry(scrollable_frame)
    phone_entry.pack(pady=5)
    
    # Organization details (initially hidden)
    org_frame = tk.Frame(scrollable_frame)
    org_name_entry = tk.Entry(org_frame)
    org_place_entry = tk.Entry(org_frame)
    org_contact_entry = tk.Entry(org_frame)
    org_email_entry = tk.Entry(org_frame)
    
    def toggle_organization_fields(parent):
        for widget in org_frame.winfo_children():
            widget.pack_forget()  # Hide organization fields
        
        if user_type.get() == "organization":
            tk.Label(org_frame, text="Organization Name:").pack()
            org_name_entry.pack(pady=5)
            tk.Label(org_frame, text="Oraganization Place:").pack()
            org_place_entry.pack(pady=5)
            tk.Label(org_frame, text="Organization Contact Number:").pack()
            org_contact_entry.pack(pady=5)
            tk.Label(org_frame, text="Organization Email:").pack()
            org_email_entry.pack(pady=5)
            org_frame.pack()  # Show organization fields

    org_frame.pack()  # Pack the frame containing organization fields
    toggle_organization_fields(scrollable_frame)  # Initialize visibility based on the selected radio button
    
    def confirm_order():
        if user_type.get() == "individual":
            buyer_info = {
                "type": "individual",
                "name": individual_name_entry.get(),
                "city": city_entry.get(),
                "district": district_entry.get(),
                "address": address_entry.get(),
                "pincode": pincode_entry.get(),
                "phone": phone_entry.get(),
            }
        else:
            buyer_info = {
                "type": "organization",
                "org_name": org_name_entry.get(),
                "place": org_place_entry.get(),
                "contact": org_contact_entry.get(),
                "email": org_email_entry.get(),
            }
        
        # Process the order (you can add further logic to store orders in a database)
        print("Order Confirmed:", buyer_info)
        messagebox.showinfo("Order", "Order has been placed successfully!")
        home_page()  # Redirect to homepage after order

    tk.Button(scrollable_frame, text="Confirm Order", command=confirm_order).pack(pady=20)
    tk.Button(scrollable_frame, text="Back to Products", command=lambda: display_products()).pack(pady=5)

# Start with the login page
login_page()

# Run the Tkinter main loop
root.mainloop()

# Close the database connection when done
conn.close()
