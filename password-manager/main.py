from tkinter import *
from tkinter import messagebox, ttk, filedialog
import json
import random
import string
import pyperclip

from encryption import generate_key, encrypt_password, decrypt_password


BG = "#1e1e1e"
FG = "#ffffff"
ENTRY = "#2b2b2b"
BTN = "#3a3a3a"

AUTO_LOCK = 120000
CLIP_CLEAR = 15000

data_file = "password-manager/data.json"


def generate_password():

    letters = string.ascii_letters
    numbers = string.digits
    symbols = "!#$%&()*+"

    password = "".join(random.sample(
        random.choices(letters,k=8) +
        random.choices(numbers,k=2) +
        random.choices(symbols,k=2),
        12
    ))

    password_entry.delete(0,END)
    password_entry.insert(0,password)

    pyperclip.copy(password)
    window.after(CLIP_CLEAR, clear_clipboard)


def check_strength(event=None):

    p = password_entry.get()
    score = 0

    if len(p) >= 8: score+=1
    if any(c.isdigit() for c in p): score+=1
    if any(c.isupper() for c in p): score+=1
    if any(c in "!#$%&()*+" for c in p): score+=1

    if score<=1:
        strength.config(text="Weak",fg="red")
    elif score<=3:
        strength.config(text="Medium",fg="orange")
    else:
        strength.config(text="Strong",fg="green")


def clear_clipboard():
    pyperclip.copy("")


def save_password():

    site = website_entry.get()
    email = email_entry.get()
    pw = password_entry.get()

    if site=="" or pw=="":
        messagebox.showerror("Error","Fields empty")
        return

    enc = encrypt_password(pw,encryption_key)

    new = {site:{"email":email,"password":enc}}

    try:
        with open(data_file,"r") as f:
            data=json.load(f)
    except:
        data={}

    data.update(new)

    with open(data_file,"w") as f:
        json.dump(data,f,indent=4)

    load_table()


def load_table():

    for i in table.get_children():
        table.delete(i)

    try:
        with open(data_file) as f:
            data=json.load(f)
    except:
        return

    for site,v in data.items():
        table.insert("",END,values=(site,v["email"]))


def search_table(event=None):

    key = search_entry.get().lower()

    for i in table.get_children():
        table.delete(i)

    try:
        with open(data_file) as f:
            data=json.load(f)
    except:
        return

    for site,v in data.items():
        if key in site.lower():
            table.insert("",END,values=(site,v["email"]))


def show_selected():

    selected = table.focus()
    if not selected:
        return

    site = table.item(selected)["values"][0]

    with open(data_file) as f:
        data=json.load(f)

    enc=data[site]["password"]
    pw=decrypt_password(enc,encryption_key)

    password_entry.delete(0,END)
    password_entry.insert(0,pw)


def toggle_password():

    if password_entry.cget("show")=="":
        password_entry.config(show="*")
    else:
        password_entry.config(show="")


def export_vault():

    path = filedialog.asksaveasfilename(defaultextension=".json")

    if not path:
        return

    with open(data_file) as src:
        data=json.load(src)

    with open(path,"w") as dst:
        json.dump(data,dst,indent=4)

    messagebox.showinfo("Export","Vault exported")


def import_vault():

    path = filedialog.askopenfilename()

    if not path:
        return

    with open(path) as f:
        data=json.load(f)

    with open(data_file,"w") as f:
        json.dump(data,f,indent=4)

    load_table()


def reset_timer(event=None):

    global timer
    window.after_cancel(timer)
    timer=window.after(AUTO_LOCK,auto_lock)

def auto_lock():

    messagebox.showinfo("Locked","Session locked")
    window.destroy()
    restart()

def restart():
    import subprocess,sys
    subprocess.Popen([sys.executable,__file__])


def unlock():

    global encryption_key

    master=master_entry.get()

    if master=="":
        messagebox.showerror("Error","Enter password")
        return

    encryption_key=generate_key(master)

    login.destroy()
    create_ui()


def create_ui():

    global window, website_entry, email_entry, password_entry
    global table, search_entry, strength, timer

    window=Tk()
    window.title("Password Vault")
    window.config(bg=BG)

    sidebar=Frame(window,bg=BTN,width=150)
    sidebar.pack(side=LEFT,fill=Y)

    Button(sidebar,text="Add",bg=BTN,fg=FG,
           command=lambda:frame_add.tkraise()).pack(fill=X)

    Button(sidebar,text="Vault",bg=BTN,fg=FG,
           command=lambda:frame_vault.tkraise()).pack(fill=X)

    Button(sidebar,text="Export",bg=BTN,fg=FG,
           command=export_vault).pack(fill=X)

    Button(sidebar,text="Import",bg=BTN,fg=FG,
           command=import_vault).pack(fill=X)

    container=Frame(window,bg=BG)
    container.pack(side=RIGHT,expand=True,fill=BOTH)

    global frame_add, frame_vault
    frame_add=Frame(container,bg=BG)
    frame_vault=Frame(container,bg=BG)

    for f in (frame_add,frame_vault):
        f.place(relwidth=1,relheight=1)


    Label(frame_add,text="Website",bg=BG,fg=FG).grid(row=0,column=0)
    website_entry=Entry(frame_add,bg=ENTRY,fg=FG)
    website_entry.grid(row=0,column=1)

    Label(frame_add,text="Email",bg=BG,fg=FG).grid(row=1,column=0)
    email_entry=Entry(frame_add,bg=ENTRY,fg=FG)
    email_entry.grid(row=1,column=1)

    Label(frame_add,text="Password",bg=BG,fg=FG).grid(row=2,column=0)
    password_entry=Entry(frame_add,bg=ENTRY,fg=FG,show="*")
    password_entry.grid(row=2,column=1)

    password_entry.bind("<KeyRelease>",check_strength)

    Button(frame_add,text="Reveal",command=toggle_password).grid(row=2,column=2)

    Button(frame_add,text="Generate",command=generate_password).grid(row=3,column=1)

    Button(frame_add,text="Save",command=save_password).grid(row=4,column=1)

    strength=Label(frame_add,text="Strength",bg=BG,fg=FG)
    strength.grid(row=2,column=3)

    

    search_entry=Entry(frame_vault)
    search_entry.pack()

    search_entry.bind("<KeyRelease>",search_table)

    table=ttk.Treeview(frame_vault,columns=("site","email"),show="headings")
    table.heading("site",text="Website")
    table.heading("email",text="Email")

    table.pack(expand=True,fill=BOTH)

    Button(frame_vault,text="Show Password",command=show_selected).pack()

    frame_add.tkraise()

    load_table()

    timer=window.after(AUTO_LOCK,auto_lock)
    window.bind_all("<Key>",reset_timer)
    window.bind_all("<Motion>",reset_timer)

    window.mainloop()


login=Tk()
login.title("Unlock Vault")

Label(login,text="Master Password").pack()

master_entry=Entry(login,show="*")
master_entry.pack()

Button(login,text="Unlock",command=unlock).pack()

login.mainloop()