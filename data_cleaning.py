import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import csv
import os
import pandas as pd

def create_new_button(event, original_button, initial_positions):
    # Get the button's current position relative to the root window
    current_x = event.widget.winfo_rootx()
    current_y = event.widget.winfo_rooty()

    # Get the canvas's bounding box relative to the root window
    canvas_x = canvas.winfo_rootx()
    canvas_y = canvas.winfo_rooty()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Check if the button is dropped inside the canvas
    if canvas_x <= current_x <= canvas_x + canvas_width and canvas_y <= current_y <= canvas_y + canvas_height:
        # If dropped inside the canvas, create a new button at the same position on the canvas
        new_button = tk.Button(canvas, text= event.widget.cget("text"))
        new_button.place(x=current_x - canvas_x, y=current_y - canvas_y)
        new_button.bind("<ButtonPress-1>", on_button_press)
        new_button.bind("<B1-Motion>", on_button_motion)
        new_button.bind("<ButtonRelease-1>", lambda event, button=new_button: create_new_button(event, button, initial_positions))
    
    # Check if the button is dropped inside the canvas
    if canvas_x <= current_x <= canvas_x + canvas_width and canvas_y <= current_y <= canvas_y + canvas_height:
        if event.widget.cget("text") == "MYSQL":
            # If dropped inside the canvas and the button is "MYSQL", create a new form
            form_window = tk.Toplevel(root)
            form_window.title("MySQL Configuration")
            form_window.geometry("300x200")

            # Create labels and entry fields for username, password, hostname, and database name
            username_label = tk.Label(form_window, text="Username:")
            username_label.pack()
            username_entry = tk.Entry(form_window)
            username_entry.pack()

            password_label = tk.Label(form_window, text="Password:")
            password_label.pack()
            password_entry = tk.Entry(form_window, show="*")
            password_entry.pack()

            hostname_label = tk.Label(form_window, text="Hostname:")
            hostname_label.pack()
            hostname_entry = tk.Entry(form_window)
            hostname_entry.pack()

            db_name_label = tk.Label(form_window, text="Database Name:")
            db_name_label.pack()
            db_name_entry = tk.Entry(form_window)
            db_name_entry.pack()

            def submit_form():
                # Callback function for the "Submit" button in the form
                username = username_entry.get()
                password = password_entry.get()
                hostname = hostname_entry.get()
                db_name = db_name_entry.get()

                # Call the establish_mysql_connection() function with the provided credentials
                connection = establish_mysql_connection(username, password, hostname, db_name)

                if connection:
                    # Fetch tables from the database
                    tables = fetch_tables_from_database(connection,save_directory)
                    connection.close()

                    if tables:
                        # Display the tables in the text area
                        textArea.delete(1.0, tk.END)  # Clear existing content
                        textArea.insert(tk.END, "Tables in the database:\n")
                        # for table in tables:
                        textArea.insert(tk.END, f"{tables}\n")
                        messagebox.showinfo("Success", "MySQL connection successful.\nTables fetched and displayed.")
                    else:
                        messagebox.showinfo("Success", "MySQL connection successful.\nNo tables found in the database.")
                else:
                    messagebox.showerror("Error", "Invalid credentials. MySQL connection failed.")

            submit_button = tk.Button(form_window, text="Submit", command=submit_form)
            submit_button.pack()

        else:
            # If dropped inside the canvas, create a new button at the same position on the canvas
            # new_button = tk.Button(canvas, text=event.widget.cget("text"))
            # new_button.place(x=current_x - canvas_x, y=current_y - canvas_y)
            # new_button.bind("<ButtonPress-1>", on_button_press)
            # new_button.bind("<B1-Motion>", on_button_motion)
            # new_button.bind("<ButtonRelease-1>", lambda event, button=new_button: create_new_button(event, button, initial_positions))
             # If dropped inside the canvas, create a new button at the same position on the canvas
            new_button = tk.Button(canvas, text=event.widget.cget("text"))
            new_button.place(x=current_x - canvas_x, y=current_y - canvas_y)
            new_button.bind("<ButtonPress-1>", on_button_press)
            new_button.bind("<B1-Motion>", on_button_motion)
            new_button.bind("<ButtonRelease-1>", lambda event, button=new_button: create_new_button(event, button, initial_positions))

            # If the dropped button is a CSV file, create a new button for it
            if event.widget.cget("text") == "table_data.csv":
                new_button.config(command=lambda: open_csv_file(new_button.cget("text")))

            # Reset the original button's position to its initial stage
            original_button.place(x=initial_positions[original_button]["x"], y=initial_positions[original_button]["y"])
            original_button.data = None



    # Reset the original button's position to its initial stage
    original_button.place(x=initial_positions[original_button]["x"], y=initial_positions[original_button]["y"])
    original_button.data = None


def remove_duplicates_and_save():
    # Load and read the data file (CSV in this example)
    try:
        data = pd.read_csv("C:/images/table_data.csv")  # Replace "path/to/your/data/file.csv" with the actual file path
    except FileNotFoundError:
        textArea.insert(END, "Error: Data file not found!\n")
        return

    # Remove duplicates from the DataFrame
    cleaned_data = data.drop_duplicates()

    # Save the cleaned data to a new CSV file
    new_csv_file = "C:/images/cleaned_data.csv"  # Replace "path/to/your/new/cleaned_data.csv" with the desired file path
    cleaned_data.to_csv(new_csv_file)

    textArea.insert(END, f"Duplicate rows removed. Cleaned data saved to {new_csv_file}\n")


def perform_data_cleaning():
    # Your data cleaning logic goes here
    # For example, perform data cleaning operations on the fetched data and save the cleaned data to a new CSV file.
    # You can use the fetched data from the previous MySQL query or fetch it again if needed.

    # Call the remove_duplicates_and_save function to perform data cleaning and save cleaned data
    remove_duplicates_and_save()

    # Optionally, create a new button on the canvas representing the cleaned CSV file
    new_button = tk.Button(canvas, text="cleaned_data.csv")
    new_button.place(x=100, y=100)
    new_button.bind("<ButtonPress-1>", on_button_press)
    new_button.bind("<B1-Motion>", on_button_motion)
    new_button.bind("<ButtonRelease-1>", lambda event, button=new_button: create_new_button(event, button,initial_positions))

def open_csv_file(filename):
    try:
        os.startfile("C:/images/"+filename)  # Open the file in the default application (e.g., Excel)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening file: {str(e)}")

def establish_mysql_connection(username, password, host, db_name):
    # Function to establish the MySQL connection with the provided credentials
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=db_name
        )
        if connection.is_connected():
            return connection
        else:
            messagebox.showerror("Error", "MySQL connection failed.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error occurred: {str(e)}")


save_directory = "C:/images/"

def fetch_tables_from_database(connection,save_path):
    # Function to fetch tables from the database and return a list of table names
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT firstName,lastName,age FROM employeedb.empapp_person;")
        # tables = [table[0] for table in cursor.fetchall()]
        table_data = cursor.fetchall()
         # Get column names from the cursor description
        column_names = [column[0] for column in cursor.description]

        csv_filename = os.path.join(save_path, "table_data.csv")
        # Save the table data into a CSV file
        # csv_filename = "table_data.csv"
        with open(csv_filename, "w", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
             # Write the column names as the first row
            csv_writer.writerow(column_names)
            # Write the data rows
            csv_writer.writerows(table_data)
            #csv_writer.writerows(table_data)
            # for row in table_data:
            #     csv_writer.writerow(row)

        return csv_filename
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error occurred while fetching tables: {str(e)}")

def configurations():
        textArea.insert(END, "Host Name:\n")
        textArea.insert(END, "Password:\n")
        textArea.insert(END, "Database Name:\n")

# Initialize the initial_positions dictionary before calling create_new_buttons function
initial_positions = {}

def create_new_buttons(button_num):
    for widget in left_frame.winfo_children():
        widget.destroy()
        widgetText1 = ""
        widgetText2 = ""
        widgetText3 = ""

    if button_num == 1:
        new_button1 = tk.Button(left_frame, text="MYSQL", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"))
        new_button1.place(x=0,y=10)
        widgetText1 = "MYSQL"

        new_button2 = tk.Button(left_frame, text="FTP/SFTP", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"))
        new_button2.place(x=0,y=70)
        widgetText2 = "FTP/SFTP"

        new_button3 = tk.Button(left_frame, text="Amazon AWS", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"))
        new_button3.place(x=0,y=140)
        widgetText3 = "Amazon AWS"

    elif button_num == 2:
        new_button1 = tk.Button(left_frame, text="Remove Duplication", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"),command=perform_data_cleaning)
        new_button1.place(x=0,y=10)
        widgetText1 = "Remove Duplication"

        new_button2 = tk.Button(left_frame, text="Remove N/A", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"))
        new_button2.place(x=0,y=70)
        widgetText2 = "Remove N/A"

        new_button3 = tk.Button(left_frame, text="Proper Type casting", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"))
        new_button3.place(x=0,y=140)
        widgetText3 = "Proper Type casting"

    elif button_num == 3:
        new_button1 = tk.Button(left_frame, text="MySQL", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"))
        new_button1.place(x=0,y=10)
        widgetText1 = "MySQL"

        new_button2 = tk.Button(left_frame, text="PostgreSQL", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"))
        new_button2.place(x=0,y=70)
        widgetText2 = "PostgreSQL"

        new_button3 = tk.Button(left_frame, text="MongoDB", width=20, relief='solid',
                                activeforeground='white', activebackground='dark blue', bd=2,
                                bg='dark blue', fg='white', font=("Consolas", 12, "bold"))
        new_button3.place(x=0,y=140)
        widgetText3 = "MongoDB"
        
    # Store the initial positions of both buttons in a dictionary
    initial_positions = {
        new_button1: {"x": 0, "y": 10, "text": widgetText1},
        new_button2: {"x": 0, "y": 70, "text": widgetText2},
        new_button3: {"x": 0, "y": 140, "text": widgetText3},
    }

    new_button1.bind("<ButtonPress-1>", on_button_press)
    new_button1.bind("<B1-Motion>", on_button_motion)
    new_button1.bind("<ButtonRelease-1>", lambda event, button=new_button1: create_new_button(event, button, initial_positions))

    new_button2.bind("<ButtonPress-1>", on_button_press)
    new_button2.bind("<B1-Motion>", on_button_motion)
    new_button2.bind("<ButtonRelease-1>", lambda event, button=new_button2: create_new_button(event, button, initial_positions))

    new_button3.bind("<ButtonPress-1>", on_button_press)
    new_button3.bind("<B1-Motion>", on_button_motion)
    new_button3.bind("<ButtonRelease-1>", lambda event, button=new_button3: create_new_button(event, button, initial_positions))


def submit_cleaning():
    # Call the remove_duplicates_and_save function to perform data cleaning and save cleaned data
    remove_duplicates_and_save()

    # Optionally, create a new button on the canvas representing the cleaned CSV file
    new_button = tk.Button(canvas, text="cleaned_data.csv")
    new_button.place(x=100, y=100)
    new_button.bind("<ButtonPress-1>", on_button_press)
    new_button.bind("<B1-Motion>", on_button_motion)
    new_button.bind("<ButtonRelease-1>", lambda event, button=new_button: create_new_button(event, button, initial_positions))
    new_button.config(command=lambda: open_csv_file(new_button.cget("text")))  # Open the file when clicked

def create_submit_button():
    submit_button = tk.Button(canvas, text="Submit", bg="green", fg="white", font=("Consolas", 12, "bold"),
                              command=submit_cleaning)
    submit_button.place(x=50, y=300)



# def button_click(button_num):
#     print(f"Button {button_num} clicked.")
#     create_new_buttons(button_num)

def button_click(button_num):
    print(f"Button {button_num} clicked.")
    create_new_buttons(button_num)

    if button_num == 2:  # Only for "Data Cleaning" button
        create_submit_button()

root = tk.Tk()
root.title("Button and Canvas Example")
root.geometry("1200x800")
root.configure(background='sky blue')

# Create a frame for the top buttons
top_buttons_frame = tk.Frame(root, bg='white', width=500, height=40)
top_buttons_frame.pack(pady=10)

image1 = tk.PhotoImage(file = "C:/images/source.png")
image2 = tk.PhotoImage(file = "C:/images/cleaning.png")
image3 = tk.PhotoImage(file = "C:/images/sink.png")

# Create three buttons at the top (arranged horizontally)
button1 = tk.Button(top_buttons_frame, text="Data Source", command=lambda: button_click(1),
                    image=image1, bg='#ffffff', activebackground='#ffffff', bd=0)
button2 = tk.Button(top_buttons_frame, text="Data Cleaning", command=lambda: button_click(2),
                    image=image2, bg='#ffffff', activebackground='#ffffff', bd=0)
button3 = tk.Button(top_buttons_frame, text="Data Sink", command=lambda: button_click(3),
                    image=image3, bg='#ffffff', activebackground='#ffffff', bd=0)

button1.place(x=0, y=3)
button2.place(x=190, y=3)
button3.place(x=380, y=3)

# Create a canvas in the middle
canvas = tk.Canvas(root, width=500, height=400, bg="white")
canvas.pack(padx=10, pady=10)

left_frame = Frame(root, background='sky blue', height=200, width=200)
left_frame.place(x=50, y=150)

# Right Frame
rightFrame = Frame(root, padx=15, pady=15, background='sky blue')
rightFrame.place(x=950, y=50)

label = LabelFrame(rightFrame, text="Parameters",height=25, width=250, bg="sky blue", font='bold')
label.grid(row=0, column=0)

label1 = LabelFrame(label, text="Configuration",height=25, width=250, bg="sky blue", font='bold')
label1.grid(row=1, column=0)

# Create text widget and specify size.
textArea = Text(rightFrame, height = 20, width = 30)
textArea.grid(row=2, column=0)

# Bottom Frame
bottomFrame = Frame(root, padx=15, pady=15, height=10)
bottomFrame.place(x=400, y=480)

# Create the table with two columns (Name and Status)
table_columns = ("Progress", "Status")
tree = ttk.Treeview(bottomFrame, columns=table_columns, show="headings", height=5)

for col in table_columns:
    tree.heading(col, text=col)
tree.pack()

def create_table():
    table_data = [
        ("Task 1", "In Progress"),
        ("Task 2", "Completed"),
        ("Task 3", "Not Started"),
    ]
    for i, (name, status) in enumerate(table_data):
        tree.insert("", tk.END, values=(name, status))

create_table()

def on_button_press(event):
    # Store the widget type and its initial position
    widget_type = event.widget.winfo_class()
    widget_text = event.widget.cget("text")
    initial_x = event.x
    initial_y = event.y
    data = (widget_type, widget_text, initial_x, initial_y)
    event.widget.data = data

def on_button_motion(event):
    # Calculate the difference in position since drag start
    widget_type, widget_text, initial_x, initial_y = event.widget.data
    dx = event.x - initial_x
    dy = event.y - initial_y

    # Move the widget to the new position
    event.widget.place(x=event.widget.winfo_x() + dx, y=event.widget.winfo_y() + dy)

root.mainloop()
