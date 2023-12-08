import pymysql
from tkinter import *
from tkinter import ttk, simpledialog, messagebox
import tkinter as tk
from tkinter import Tk, Label, PhotoImage
import os 
import webbrowser
from tkinter import PhotoImage, Label, Entry, Button, W, ttk, Tk, NO
from DatabadeConnectionProvider import BaseDatabaseConnection
from Student_Database import StudentDatabaseConnection


db_connection = StudentDatabaseConnection()

# Validation and Registration of User
def register_user():
    user_information = username.get()
    password_information = password.get()

    # Check if either username or password is missing
    if (user_information == "" or user_information == " ") or (password_information == "" or password_information == " "):
        error_label = Label(register_window, bg='#FFFFFF', font=('Arial', 6), text="Please enter both username and password!")
        error_label.place(x=120, y=223)
        register_window.after(1500, error_label.destroy)
        return
    
    # Check which field is missing and display an error message     
    if not user_information or not password_information:
        if password_information:
            error_label = Label(register_window, bg='#FFFFFF', font=('Arial', 7), text="Please enter Username!")
            error_label.place(x=140, y=223)
            register_window.after(1500, error_label.destroy)
            return
        
        elif user_information:
            error_label = Label(register_window, bg='#FFFFFF', font=('Arial', 7), text="Please enter a Password!")
            error_label.place(x=140, y=223)
            register_window.after(1500, error_label.destroy)
            return

    try:
        # Check if the username already exists
        if db_connection.check_user_existence(user_information):
            error_label = Label(register_window, bg='#FFFFFF', font=('Arial', 7), text="Username already exists!")
            error_label.place(x=140, y=223)
            register_window.after(1500, error_label.destroy)
        else:
            # Register the user
            if db_connection.register_user(user_information, password_information):

                # Clear textfields after successful registration
                username_Entry.delete(0, END)
                password_Entry.delete(0, END)

                register_success_notif = Label(register_window, bg='#FFFFFF', font=('Arial', 7), text="Registration Successful!")
                register_success_notif.place(x=140, y=223)
                root.after(1500, register_success_notif.destroy)
            else:
                error_label = Label(register_window, bg='#FFFFFF', font=('Arial', 7), text="Error registering user!")
                error_label.place(x=140, y=223)
                register_window.after(1500, error_label.destroy)
    except Exception as e:
        print(f"Error: {e}")


# Register Window
def register():

    # Global variables to access them outside the function
    global register_window
    global username
    global password
    global username_Entry
    global password_Entry

    # Create a new window for registration
    register_window = Toplevel(password_window)
    register_window.title("Register")
    register_window.geometry("300x250")
    register_window.resizable(False, False)

    background_image = PhotoImage(file='images/Registration Design.png')
    register_window.image = background_image
    background_label = tk.Label(register_window, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # StringVar variables for username and password
    username = StringVar()
    password = StringVar()
    
    # Username textfield
    username_Entry = Entry(register_window, borderwidth = 0, width = 21, textvariable = username)
    username_Entry.place(x = 130, y = 105)

    # Password textfield
    password_Entry = Entry(register_window, borderwidth = 0, width = 21, textvariable = password)
    password_Entry.place(x = 130, y = 158)

    # Confirm button directing to the registration process
    Button(register_window, text="Confirm",
                            font = ('Helvetica', 11), 
                            fg='#FFFFFF', 
                            bg='#004aad', borderwidth = 0,
                            width = 7,command = register_user).place(x = 160, y = 193)
    
# Link to show Developers
def link():
    webbrowser.open("https://group11developers.weebly.com/")


# Password Window
def check_password(root):

    global password_window
    global usernameEntry
    global passwordEntry
    global username_verify
    global password_verify
    
    # Create a new window for Login
    password_window = Toplevel(root)
    password_window.title("PIN Verification")
    password_window.geometry("450x250")
    password_window.resizable(False, False)

    background_image = PhotoImage(file='images/ACP Login Design.png')
    password_window.image = background_image
    background_label = tk.Label(password_window, image = background_image)
    background_label.place(relwidth=1, relheight=1)

    username_verify = StringVar()
    password_verify = StringVar()

    usernameEntry = tk.Entry(password_window, textvariable = username_verify, width=16, borderwidth = 0, font=('Arial', 11))
    usernameEntry.place(x=82, y=105)

    passwordEntry = tk.Entry(password_window, textvariable = password_verify, width=16, borderwidth = 0, font=('Arial', 11), show="*")
    passwordEntry.place(x=82, y=159)

    # Directs user to Registration window
    registerBtn = tk.Button(password_window, 
                         width= 7,
                         text='Register', 
                         font=('Helvetica', 11), 
                         borderwidth=0, 
                         fg='#FFFFFF', 
                         bg='#004aad', 
                         command= register)
    
    registerBtn.place(x=150, y=194)

    # Password validation
    loginBtn = tk.Button(password_window, 
                         width= 7,
                         text='Login', 
                         font=('Helvetica', 11), 
                         borderwidth=0, 
                         fg='#FFFFFF', 
                         bg='#004aad', 
                         command = lambda: validate_password(password_window))
    
    loginBtn.place(x=80, y=194)
    
    # Developers link button
    linkButton = Button(password_window, width = 8,
                         font=('Helvetica', 10), 
                         borderwidth=0, 
                         fg='#FFFFFF', 
                         bg='#004aad',
                         text = "Developers", 
                         command = link)
    linkButton.place(x=270, y=30)

    
# Password Validation
def validate_password(password_window):
    username_login = username_verify.get()
    password_login = password_verify.get()

    if not username_login or not password_login:
        # Display a message if either username or password is missing
        UserPasswordDetectionLabel = Label(password_window, font=('Arial', 7), bg='#FFFFFF',text="*Please input both username and password.")
        UserPasswordDetectionLabel.place(x=65, y=225)
        root.after(1500, UserPasswordDetectionLabel.destroy)
    else:
        try:
            # Check if provided username and password in database
            query = "SELECT * FROM student_password WHERE username = %s AND password = %s"
            params = (username_login, password_login)
            result_cursor = db_connection.execute_query(query, params)
            result = result_cursor.fetchone()
            
            # DIrect to pragram's main functions if username and password is in database
            if  result:
                password_window.destroy()
                root.deiconify()
                registrationMain()

            else:
                UserPasswordDetectionLabel = Label(password_window, font=('Arial', 7), bg='#FFFFFF', text="*Incorrect username or password.")
                UserPasswordDetectionLabel.place(x=100, y=225)
                root.after(1500, UserPasswordDetectionLabel.destroy)

        except Exception as e:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

# Main Tkinter window
root = Tk()
root.configure(bg="#ADD8E6")
root.withdraw()

check_password(root)

# Configure settings for the main window
root.title("Student Registration System")
root.geometry("1200x800")
root.resizable(False, False)


# Table that displays data values and updates table after succesfull data alterations 
def registrationMain():

    def refreshTable():

        # Retrieve all data from the 'students' table
        query = "SELECT * FROM students"
        results_cursor = db_connection.execute_query(query)
        results = results_cursor.fetchall()

        # Clear existing data in the table
        for data in my_tree.get_children():
            my_tree.delete(data)

        # Insert new data into the treeview
        for record in results:
            my_tree.insert(parent='', index='end', iid=record[0], text="", values=record[:], tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))

        # Set column widths
        my_tree.column('#1', width=50)
        my_tree.column('#2', width=50)
        my_tree.column('#3', width=50)
        my_tree.column('#4', width=50)
        my_tree.column('#5', width=50)

        my_tree.place(x=473, y=253, width=652, height=351)

    # Placeholders
    ph1 = tk.StringVar()
    ph2 = tk.StringVar()
    ph3 = tk.StringVar()
    ph4 = tk.StringVar()
    ph5 = tk.StringVar()
    
    # Set placeholder values
    def setph(word, num):
        if num == 1:
            ph1.set(word)
        if num == 2:
            ph2.set(word)
        if num == 3:
            ph3.set(word)
        if num == 4:
            ph4.set(word)
        if num == 5:
            ph5.set(word)


     # Add and Stores the data inputs
    def add():

        # Get values from Input fields
        studid = str(studidEntry.get())
        fname = str(fnameEntry.get())
        lname = str(lnameEntry.get())
        address = str(addressEntry.get())
        course = str(courseEntry.get())

        #Check if textfields are empty
        if (studid == "" or studid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (
                address == "" or address == " ") or (course == "" or course == default_value):
            messagebox.showinfo("Error", "Please complete all required entries.")
            
            return
        else:
            
            # Allows the data to be stored in Database
            try:
                query = "INSERT INTO students VALUES (%s, %s, %s, %s, %s)"
                params = (studid, fname, lname, address, course)
                db_connection.execute_query(query, params)

                # Clear Entry widgets after successful insertion
                studidEntry.delete(0, END)
                fnameEntry.delete(0, END)
                lnameEntry.delete(0, END)
                addressEntry.delete(0, END)
                courseEntry.set(default_value)

            except:
                 messagebox.showinfo("Error", "Student ID already exist")
                 return
            
            refreshTable()
    
    # Deletes all stored data in database
    def reset():
        decision = messagebox.askquestion("Warning!!", "Delete all data?")
        if decision != "yes":
            return
        else:
            try:
                query = "DELETE FROM students"
                db_connection.execute_query(query)
            except:
                messagebox.showinfo("Error", "Sorry an error occured")
                return

            refreshTable()

    # Delete Specific Row of data in database
    def delete():

        # Ask for confirmation before deleting
        decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
        if decision != "yes":
            return
        else:
            # Get the selected data in the treeview
            selected_item = my_tree.selection()[0]
            deleteData = str(my_tree.item(selected_item)['values'][0])
            try:
                selected_item = my_tree.selection()[0]
                deleteData = str(my_tree.item(selected_item)['values'][0])
                query = "DELETE FROM students WHERE STUDID = %s"
                params = (deleteData,)
                db_connection.execute_query(query, params)
                
    
            except:
                messagebox.showinfo("Error", "Sorry an error occured")
                return
            
            refreshTable()
    
    # Allows specified row of data the be displayed in text fileds
    def select():
        try:

            # Get the selected data in the treeview
            selected_item = my_tree.selection()[0]
            studid = str(my_tree.item(selected_item)['values'][0])
            fname = str(my_tree.item(selected_item)['values'][1])
            lname = str(my_tree.item(selected_item)['values'][2])
            address = str(my_tree.item(selected_item)['values'][3])
            phone = str(my_tree.item(selected_item)['values'][4])

            # Display selcted row of data to the input fields using setph function
            setph(studid, 1)
            setph(fname, 2)
            setph(lname, 3)
            setph(address, 4)
            setph(phone, 5)
        except:
            messagebox.showinfo("Error", "Please select a data row")

    # User inputs an existing data in texfield and this function searches and displays related data
    def search():

        # Get values from input fields
        studid = str(studidEntry.get())
        fname = str(fnameEntry.get())
        lname = str(lnameEntry.get())
        address = str(addressEntry.get())
        course = str(courseEntry.get())

        # Searching data
        query = "SELECT * FROM students WHERE STUDID=%s OR FNAME=%s OR LNAME=%s OR ADDRESS=%s OR COURSE=%s"
        params = (studid, fname, lname, address, course)
        results_cursor = db_connection.execute_query(query, params)
                

        try:
            # Fetch all results from the cursor
            results = results_cursor.fetchall()
            
            # Iterate through the first result and set placeholder values
            for num in range(0, 5):
                setph(results[0][num], (num + 1))

        except:
            messagebox.showinfo("Error", "No data found")

    # Alter existing data
    def update():
        selectedStudid = ""

        # Attempt to get the selected item from the treeview
        try:
            selected_item = my_tree.selection()[0]
            selectedStudid = str(my_tree.item(selected_item)['values'][0])
        except:
            messagebox.showinfo("Error", "Please select a data row")

        # Get values from input fields
        studid = str(studidEntry.get())
        fname = str(fnameEntry.get())
        lname = str(lnameEntry.get())
        address = str(addressEntry.get())
        course = str(courseEntry.get())

        if (studid == "" or studid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (
                address == "" or address == " ") or (course == "" or course == default_value):
            messagebox.showinfo("Error", "Please fill up the blank entry")
            return
        else:
            try:
                query = "UPDATE students SET STUDID=%s, FNAME=%s, LNAME=%s, ADDRESS=%s, COURSE=%s WHERE STUDID=%s"
                params = (studid, fname, lname, address, course, selectedStudid)
                db_connection.execute_query(query, params)

                # Clear Entry widgets after successful update
                studidEntry.delete(0, END)
                fnameEntry.delete(0, END)
                lnameEntry.delete(0, END)
                addressEntry.delete(0, END)
                courseEntry.set(default_value)

            except:
                messagebox.showinfo("Error", "Student ID already exist")
                return

        refreshTable()


    background_image = PhotoImage(file='images/DesignForMain.png')

    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    root.image = background_image
    my_tree = ttk.Treeview(root)

    # Input fields
    studidEntry = Entry(root, borderwidth=0, width=33, font = ('Arial', 15), textvariable = ph1)
    fnameEntry = Entry(root, borderwidth=0, width=33, font = ('Arial', 15), textvariable = ph2)
    lnameEntry = Entry(root, borderwidth=0, width=33, font = ('Arial', 15), textvariable = ph3)
    addressEntry = Entry(root, borderwidth=0, width=33, font = ('Arial', 15), textvariable = ph4)

    # Combobox for selecting the course
    courseOptions = ["BS Information Technology", "BS Computer Science"]
    courseEntry = ttk.Combobox(root, width=31, font=('Arial', 15), textvariable = ph5, values = courseOptions)
    default_value = "Choose Course"
    courseEntry.set(default_value)
    courseEntry.config(state="readonly")

    # Input fields Placements    
    studidEntry.place(x=80,y=264)
    fnameEntry.place(x=80,y=340)
    lnameEntry.place(x=80,y=417)
    addressEntry.place(x=80,y=493)
    courseEntry.place(x=80,y=569)

    # Function Buttons
    addBtn = Button(
        root, text="Add", padx=20, pady=10, width=8,
        bd=5, font=('Helvitica', 15), bg="#42a2c2", command=add)
    updateBtn = Button(
        root, text="Update", padx=20, pady=10, width=8,
        bd=5, font=('Helvitica', 15), bg="#42a2c2", command=update)
    deleteBtn = Button(
        root, text="Delete", padx=20, pady=10, width=8,
        bd=5, font=('Helvitica', 15), bg="#42a2c2", command=delete)
    searchBtn = Button(
        root, text="Search", padx=20, pady=10, width=8,
        bd=5, font=('Helvitica', 15), bg="#42a2c2", command=search)
    resetBtn = Button(
        root, text="Reset", padx=20, pady=10, width=8,
            bd=5, font=('Helvitica', 15), bg="#42a2c2", command=reset)
    selectBtn = Button(
        root, text="Select", padx=20, pady=10, width=8,
        bd=5, font=('Helvitica', 15), bg="#42a2c2", command=select)
    
    # Navigation to show all students of a certain course
    showBSIT_Btn = Button(
        root, text="BSIT Students", padx=20, pady=10, width=8,
        bd=5, font=('Helvitica', 15), bg="#42a2c2", command = show_BSIT_students)
    
    showBSCS_Btn = Button(
        root, text="BSCS Students", padx=20, pady=10, width=8,
        bd=5, font=('Helvitica', 15), bg="#42a2c2", command = show_BSCS_students)

    # Function Buttons Placements
    addBtn.place(x=80, y=643)
    updateBtn.place(x=260, y=643)
    deleteBtn.place(x=438, y=643)
    searchBtn.place(x=617, y=643)
    resetBtn.place(x=795, y=643)
    selectBtn.place(x=974, y=643)

    showBSCS_Btn.place(x=970, y = 105)
    showBSIT_Btn.place(x=820, y = 105)


    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial Bold', 15))

    # Columns for the Treeview
    my_tree['columns'] = ("Stud ID", "Firstname", "Lastname", "Address", "Course")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Stud ID", anchor=W, width=170)
    my_tree.column("Firstname", anchor=W, width=150)
    my_tree.column("Lastname", anchor=W, width=150)
    my_tree.column("Address", anchor=W, width=165)
    my_tree.column("Course", anchor=W, width=150)
    
    # Headings for each column
    my_tree.heading("Stud ID", text="Student ID", anchor=W)
    my_tree.heading("Firstname", text="Firstname", anchor=W)
    my_tree.heading("Lastname", text="Lastname", anchor=W)
    my_tree.heading("Address", text="Address", anchor=W)
    my_tree.heading("Course", text="Course", anchor=W)

    refreshTable()

# Display information of all BSIT students to the table
def show_BSIT_students(): 

    # Function to refresh the size and placing of the table
    def RefreshTableSizeAndPlacing():
        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
        my_tree.column('#1', width=50)  
        my_tree.column('#2', width=50) 
        my_tree.column('#3', width=50) 
        my_tree.column('#4', width=50) 
        my_tree.place(x=75, y=285, width=1051, height=437)

    # Set background image
    background_image = PhotoImage(file='images/BSIT.png')
    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    root.image = background_image

    # Create table
    my_tree = ttk.Treeview(root)

    
    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)

        # Read data from the database
        for array in read():
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

        RefreshTableSizeAndPlacing()

     # Back button 
    backBtn = Button(
        bd=5, text= "←" ,font=('Bold', 20), bg="#008FBF", fg = '#FFFFFF', borderwidth= 0, command = registrationMain)
    backBtn.place(x=15,y=21)

    def read():
        query = "SELECT * FROM students where COURSE = 'BS Information Technology'"
        results_cursor = db_connection.execute_query(query)
        results = results_cursor.fetchall()
        return results

    addressEntry = Entry(root, borderwidth=0, width=16, font = ('Arial', 15))
    addressEntry.place(x=92,y=221)

    # Function to perform search based on address
    def search(event=None):
        address = str(addressEntry.get())

        # Search for BSIT students with a specific address
        query = "SELECT * FROM students WHERE COURSE LIKE 'BS Information Technology' AND ADDRESS LIKE %s"
        results_cursor = db_connection.execute_query(query, (f'%{address}%',))
        results = results_cursor.fetchall() 

        for data in my_tree.get_children():
            my_tree.delete(data)
        
        # Insert search results into the table
        for array in results:
            my_tree.insert(parent='', index='end', iid=array, text="", values=array, tag="orow")

        RefreshTableSizeAndPlacing()
    
    # Bind the search function to the KeyRelease event of the addressEntry
    addressEntry.bind("<KeyRelease>", search)
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial Bold', 15))

    # Define columns of the table
    my_tree['columns'] = ("Stud ID", "Firstname", "Lastname", "Address")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Stud ID", anchor=W, width=170)
    my_tree.column("Firstname", anchor=W, width=150)
    my_tree.column("Lastname", anchor=W, width=150)
    my_tree.column("Address", anchor=W, width=165)

    my_tree.heading("Stud ID", text="Student ID", anchor=W)
    my_tree.heading("Firstname", text="Firstname", anchor=W)
    my_tree.heading("Lastname", text="Lastname", anchor=W)
    my_tree.heading("Address", text="Address", anchor=W)
    
    refreshTable()

# Display information of all BSCS students to the table
def show_BSCS_students(): 

    def RefreshTableSizeAndPlacing():
        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
        my_tree.column('#1', width=50)  
        my_tree.column('#2', width=50) 
        my_tree.column('#3', width=50) 
        my_tree.column('#4', width=50) 
        my_tree.place(x=75, y=285, width=1051, height=437)

    background_image = PhotoImage(file='images/BSCS.png')
    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    root.image = background_image

    my_tree = ttk.Treeview(root)

    def refreshTable():
        for data in my_tree.get_children():
            my_tree.delete(data)

        for array in read():
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

        RefreshTableSizeAndPlacing()

    backBtn = Button(
        bd=5, text= "←" ,font=('Bold', 20), bg="#008FBF", fg = '#FFFFFF', borderwidth= 0, command = registrationMain)
    backBtn.place(x=15,y=21)

    def read():
        query = "SELECT * FROM students where COURSE = 'BS Computer Science'"
        results_cursor = db_connection.execute_query(query)
        results = results_cursor.fetchall()
        return results

    addressEntry = Entry(root, borderwidth=0, width=16, font = ('Arial', 15))
    addressEntry.place(x=92,y=221)

    def search(event=None):
        address = str(addressEntry.get())

        query = "SELECT * FROM students WHERE COURSE LIKE 'BS Computer Science' AND ADDRESS LIKE %s"
        results_cursor = db_connection.execute_query(query, (f'%{address}%',))
        results = results_cursor.fetchall() 

        for data in my_tree.get_children():
            my_tree.delete(data)

        for array in results:
            my_tree.insert(parent='', index='end', iid=array, text="", values=array, tag="orow")

        RefreshTableSizeAndPlacing()

    addressEntry.bind("<KeyRelease>", search)

    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial Bold', 15))

    my_tree['columns'] = ("Stud ID", "Firstname", "Lastname", "Address")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Stud ID", anchor=W, width=170)
    my_tree.column("Firstname", anchor=W, width=150)
    my_tree.column("Lastname", anchor=W, width=150)
    my_tree.column("Address", anchor=W, width=165)

    my_tree.heading("Stud ID", text="Student ID", anchor=W)
    my_tree.heading("Firstname", text="Firstname", anchor=W)
    my_tree.heading("Lastname", text="Lastname", anchor=W)
    my_tree.heading("Address", text="Address", anchor=W)
    
    refreshTable()
    
root.mainloop()      
