import tkinter as tk
from tkinter import *
from cryptography.fernet import Fernet
import random, string, os

# ---------- KEY ----------
def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as f:
            f.write(key)
    else:
        with open("key.key", "rb") as f:
            key = f.read()
    return key

key = load_key()
fernet = Fernet(key)

history = []

# ---------- STRENGTH ----------
def check_strength(password):
    score = 0
    if len(password) >= 6: score += 1
    if len(password) >= 10: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*" for c in password): score += 1

    if score <= 2: return "Weak ❌", "red"
    elif score <= 4: return "Medium ⚠️", "orange"
    else: return "Strong ✅", "green"

# ---------- LOGIN ----------
def login():
    if user_entry.get() == "komal" and pass_entry.get() == "1234":
        login_window.destroy()
        open_main()
    else:
        error_label.config(text="Wrong credentials ❌")

# ---------- MAIN APP ----------
def open_main():
    root = Tk()
    root.title("Pro Password Manager 🔐")
    root.geometry("520x600")
    root.configure(bg="#0a2342")

    # ---------- FUNCTIONS ----------
    def on_type(event):
        pwd = password_entry.get()
        if pwd:
            s,c = check_strength(pwd)
            result_label.config(text=s, fg=c)
            canvas.itemconfig(bar, fill=c)
        else:
            result_label.config(text="")
            canvas.itemconfig(bar, fill="grey")

    def generate():
        length = length_slider.get()
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = "".join(random.choice(chars) for _ in range(length))
        password_entry.delete(0, END)
        password_entry.insert(0, pwd)

    def save():
        pwd = password_entry.get()
        enc = fernet.encrypt(pwd.encode())
        with open("data.dat","ab") as f:
            f.write(enc+b"\n")
        history_box.insert(END, pwd)

    def load():
        history_box.delete(0, END)
        try:
            with open("data.dat","rb") as f:
                for line in f:
                    dec = fernet.decrypt(line.strip()).decode()
                    history_box.insert(END, dec)
        except:
            pass

    def copy():
        root.clipboard_clear()
        root.clipboard_append(password_entry.get())
        root.update()

    def clear():
        password_entry.delete(0, END)
        result_label.config(text="")
        canvas.itemconfig(bar, fill="grey")

    show = False
    def toggle():
        nonlocal show
        show = not show
        password_entry.config(show="" if show else "*")

    # ---------- UI ----------
    Label(root, text="Password Manager 🔐", font=("Arial",18,"bold"),
          fg="white", bg="#0a2342").pack(pady=10)

    password_entry = Entry(root, show="*", font=("Arial",14), width=25)
    password_entry.pack(pady=10)
    password_entry.bind("<KeyRelease>", on_type)

    result_label = Label(root, text="", font=("Arial",14), bg="#0a2342")
    result_label.pack()

    canvas = Canvas(root, width=200, height=20, bg="#0a2342", highlightthickness=0)
    canvas.pack(pady=5)
    bar = canvas.create_rectangle(0,0,200,20, fill="grey")

    length_slider = Scale(root, from_=6, to=20, orient=HORIZONTAL,
                          label="Password Length")
    length_slider.set(10)
    length_slider.pack()

    frame = Frame(root, bg="#0a2342")
    frame.pack(pady=10)

    Button(frame, text="Generate", bg="#3a86ff", fg="white", command=generate).grid(row=0,column=0,padx=5)
    Button(frame, text="Copy", bg="#8338ec", fg="white", command=copy).grid(row=0,column=1,padx=5)
    Button(frame, text="Clear", bg="#ef233c", fg="white", command=clear).grid(row=0,column=2,padx=5)
    Button(frame, text="Show/Hide", bg="#e36414", fg="white", command=toggle).grid(row=0,column=3,padx=5)

    Button(root, text="Save (Encrypted)", command=save, bg="#2a9d8f", fg="white").pack(pady=5)
    Button(root, text="Load Passwords", command=load, bg="#264653", fg="white").pack(pady=5)

    Label(root, text="History", fg="white", bg="#0a2342").pack()
    history_box = Listbox(root, width=40)
    history_box.pack(pady=10)

    root.mainloop()

# ---------- LOGIN UI ----------
login_window = Tk()
login_window.title("Login 🔐")
login_window.geometry("300x250")

Label(login_window, text="Username").pack()
user_entry = Entry(login_window)
user_entry.pack()

Label(login_window, text="Password").pack()
pass_entry = Entry(login_window, show="*")
pass_entry.pack()

Button(login_window, text="Login", command=login).pack(pady=10)

error_label = Label(login_window, text="", fg="red")
error_label.pack()

login_window.mainloop()