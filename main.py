from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
           'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password = ""

    for letter in range(random.randint(8, 10)):
        password += random.choice(letters)

    for symbol in range(random.randint(4, 8)):
        password += random.choice(symbols)

    for num in range(random.randint(2, 4)):
        password += random.choice(numbers)

    password_shuffled = ''.join(random.sample(password, len(password)))
    password_entry.insert(0, password_shuffled)
    pyperclip.copy(password_shuffled)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = user_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        # confirmation
        # is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
        #                                                       f"\nPassword: {password} \n Is it ok to save?")
        # if is_ok:
        # with open("data.txt", "a") as f:
        #     f.write(f"{website} | {email} | {password}\n")

        try:
            with open("data.json") as json_data:
                data = json.load(json_data)
        except Exception as e:
            with open("data.json", "w") as json_data:
                json.dump(new_data, json_data, indent=4)
                print(e)
        else:
            data.update(new_data)

            with open("data.json", "w") as json_data:
                json.dump(data, json_data, indent=4)

        finally:
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")
            website_entry.focus()


# ---------------------------- FIND PASSWORD ----------------------------#
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as json_data:
            data = json.load(json_data)
    except FileNotFoundError:
        messagebox.showinfo(title="404 Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("My Password Manager")
window.minsize(width=300, height=300)
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
bg_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=bg_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=32)
website_entry.focus()
website_entry.grid(column=1, row=1)
user_entry = Entry(width=50)
user_entry.grid(column=1, row=2, columnspan=2)
user_entry.insert(0, "calmaxbenard@gmail.com")
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)
generate_button = Button(text="Generate Password", command=generate_password, width=13)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", width=42, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
