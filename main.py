import re
import random
import string
from tkinter import *
from tkinter.ttk import Progressbar

# ---------------- FUNCTIONS ---------------- #

def check_password_strength(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letter")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letter")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add number")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        suggestions.append("Add special character")

    return score, suggestions


def check():
    pwd = entry.get()
    score, suggestions = check_password_strength(pwd)

    if score == 5:
        strength = "Strong 💪"
        color = "#133F15"  # Green
    elif score >= 3:
        strength = "Medium ⚠️"
        color = "#91741B"  # Amber
    else:
        strength = "Weak ❌"
        color = "#5F0D07"  # Red

    result_label.config(text=strength, fg=color)
    progress['value'] = score * 20
    suggest_label.config(text="\n".join(suggestions))


def toggle_password():
    if entry.cget('show') == '*':
        entry.config(show='')
        show_btn.config(text='Hide')
    else:
        entry.config(show='*')
        show_btn.config(text='Show')


def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = ''.join(random.choice(chars) for _ in range(12))
    entry.delete(0, END)
    entry.insert(0, pwd)
    check()


def copy_password():
    root.clipboard_clear()
    root.clipboard_append(entry.get())


# ---------------- GUI SETUP ---------------- #

root = Tk()
root.title("Password Strength Checker")
root.geometry("450x480")
root.config(bg="#0a2342")  # Dark navy blue

# Fonts
title_font = ("Helvetica", 20, "bold")
button_font = ("Helvetica", 12, "bold")
label_font = ("Helvetica", 12)

# Title Label
title = Label(root, text="Password Strength Checker", font=title_font, fg="white", bg="#0a2342")
title.pack(pady=(20, 15))

# Frame for Entry and Show button
entry_frame = Frame(root, bg="#0a2342")
entry_frame.pack(pady=(0, 10))

entry = Entry(entry_frame, show="*", font=("Helvetica", 16), width=25, bd=3, relief=GROOVE)
entry.pack(side=LEFT, padx=(0, 10))

show_btn = Button(entry_frame, text="Show", command=toggle_password, font=button_font, bg="#005f73", fg="white", bd=0, padx=10)
show_btn.pack(side=LEFT)

# Check Strength Button
check_btn = Button(root, text="Check Strength", command=check, font=button_font, bg="#028090", fg="white", padx=15, pady=8, bd=0)
check_btn.pack(pady=10)

# Progress Bar
progress = Progressbar(root, length=350, mode='determinate')
progress.pack(pady=10)

# Result Label
result_label = Label(root, text="", font=("Helvetica", 16, "bold"), bg="#0a2342")
result_label.pack(pady=10)

# Suggestions Label
suggest_label = Label(root, text="", font=label_font, fg="#caf0f8", bg="#0a2342", justify=LEFT)
suggest_label.pack(pady=10)

# Frame for Generate and Copy buttons
btn_frame = Frame(root, bg="#07121f")
btn_frame.pack(pady=20)

generate_btn = Button(btn_frame, text="Generate Password", command=generate_password, font=button_font, bg="#05668d", fg="white", bd=0, padx=15, pady=8)
generate_btn.pack(side=LEFT, padx=10)

copy_btn = Button(btn_frame, text="Copy Password", command=copy_password, font=button_font, bg="#028090", fg="white", bd=0, padx=15, pady=8)
copy_btn.pack(side=LEFT, padx=10)

root.mainloop()