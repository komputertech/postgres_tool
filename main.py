import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import psycopg2 as postgres_driver


def get_value():
    value = [
        entry_host.get(),
        entry_database.get(),
        entry_login.get(),
        entry_password.get(),
        entry_command.get()
    ]
    return value


def get_data(value_host,
             value_database,
             value_login,
             value_password,
             value_command):
    conn = None
    data = []
    try:
        conn = postgres_driver.connect(
            host=value_host,
            database=value_database,
            user=value_login,
            password=value_password
        )
        cur = conn.cursor()
        cur.execute(value_command)
        result_set = cur.fetchall()
        for row in result_set:
            line = " ".join([str(element) for element in row])
            data.append(line)
        cur.close()
    except (Exception, postgres_driver.DatabaseError) as error:
        # send error to text widget
        data.append(str(error))
    finally:
        if conn is not None:
            conn.close()
        return data


def button_action():
    value = get_value()
    data = get_data(*value)
    text_data.delete("1.0", "end")
    for element in data:
        text_data.insert("end", element + "\n")


root = tk.Tk()
root.title("Postgres database tool")
root.geometry("640x480")

grid_layout = ttk.Frame(root)

label_host = ttk.Labelframe(grid_layout, text="Host:")
entry_host = ttk.Entry(label_host)
entry_host.insert("0", "localhost")
entry_host.pack()
label_host.grid(row=0, column=0)

label_database = ttk.Labelframe(grid_layout, text="Database:")
entry_database = ttk.Entry(label_database)
entry_database.pack()
label_database.grid(row=0, column=1)

label_login = ttk.Labelframe(grid_layout, text="Login:")
entry_login = ttk.Entry(label_login)
entry_login.pack()
label_login.grid(row=0, column=2)

label_password = ttk.Labelframe(grid_layout, text="Password:")
entry_password = ttk.Entry(label_password)
entry_password.pack()
label_password.grid(row=0, column=3)

button_done = ttk.Button(grid_layout, text='Run command', command=lambda: button_action())
button_done.grid(row=0, column=4, sticky="s")

grid_layout.pack(expand=False)

label_command = ttk.Labelframe(root, text="Command:")
entry_command = ttk.Entry(label_command)
entry_command.insert("0", "SELECT * FROM [table_name];")
entry_command.pack(fill="x")
label_command.pack(fill="x", expand=False)

text_data = scrolledtext.ScrolledText(root)
text_data.pack(anchor="center", fill="both", expand=True)

root.mainloop()
