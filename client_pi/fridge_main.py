import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import fridge_db
from socket_client import send_file



########## global ##########

themeColor = "#f6ddd9"
server_ip = "10.10.15.103"
server_port = 12309
fridge_db.db_file = "./ingredients.db"
tree = None



##########  funtion  ##########

def display_treeview_content(tree, name_str, num_int):
    fridge_df = fridge_db.read_ingredients_table()

    fridge_lst = fridge_df.loc[fridge_df["name"] == name_str, "num"].tolist()

    if (len(fridge_lst) > 0) and (fridge_lst[0] + num_int < 0):
        messagebox.showinfo("갯수 오류", "냉장고에 있는 수보다 더 많이 뺄 수 없습니다.")
        return

    fridge_df = fridge_db.insert_oneline([name_str, num_int])
    print(fridge_df)

    # Tree view item clear
    for item in tree.get_children():
        tree.delete(item)

    # Define the column headings
    for column in fridge_df.columns:
        tree.heading(column, text=column)
        tree.column(column, anchor='center')

    # Insert the data into the Treeview
    for _, row in fridge_df.iterrows():
        tree.insert("", "end", values=list(row))



##########  main ##########
##### window #####
root = tk.Tk()
root.title("pi fridge manager")
root.resizable(False, False)
root.configure(bg=themeColor)
win_width = 960
win_height = 640
root_size_text = str(win_width) + "x" + str(win_height)
root.geometry(root_size_text)


##### DB #####
fridge_db.db_file = "./ingredients.db"
fridge_db.create_ingredients_table()

fridge_df = fridge_db.read_ingredients_table()


##### table #####
# Create a Treeview widget
tree = ttk.Treeview(root)
style = ttk.Style()
style.configure("Treeview.Heading", background=themeColor)

# Define the columns
tree["columns"] = list(fridge_df.columns)
tree["show"] = "headings"  # Hide the first empty column

# Define the column headings
for column in fridge_df.columns:
    tree.heading(column, text=column)
    tree.column(column, anchor='center')

# Insert the data into the Treeview
for index, row in fridge_df.iterrows():
    tree.insert("", "end", values=list(row))


##### label #####
fridge_label = tk.Label(
    root,
    text="냉장고 재료",
    bg=themeColor,
    font=("Helvetica", 20)
)


##### string box #####
name_str = tk.StringVar()
name_txtbox = ttk.Entry(root, width=20, textvariable=name_str)
num_int = tk.IntVar()
num_txtbox = ttk.Entry(root, width=10, textvariable=num_int)


##### button #####
insertDB_btn = tk.Button(
    root,
    text="insert",
    command=lambda: display_treeview_content(tree, name_str.get(), num_int.get())
)
send_btn = tk.Button(
    root,
    text="send\nto server",
    command=lambda: send_file(server_ip=server_ip,
                              server_port=server_port,
                              file_path=fridge_db.db_file)
)


##### place and packing #####

tree.place(x=20, y=20, width=900//2, height=530)
send_btn.place(x=20, y=570, width=900//2)

fridge_label.place(x=650, y=180)
name_txtbox.place(x=550, y=380)
num_txtbox.place(x=800, y=380)
insertDB_btn.place(x=690, y=480)

root.mainloop()
