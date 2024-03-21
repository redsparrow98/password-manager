from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generate():
    """generates a password for the user"""

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', \
        'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', \
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',\
        'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # makes list for each element using list comprehension
    # we generate a random range for each element and chose a
    # random letter/symbol/num in the lists the amount of times
    # in the range and assign to the new lists
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    # combine all the lists above in to one
    password_list = password_letters + password_symbols + password_numbers
    # shuffle the items in the one combined list
    shuffle(password_list)
    # join all the elements from the final shuffled list
    password = "".join(password_list)

    # deletes any pre generated passwords instead of just adding
    pass_entry.delete(0, END)
    # writes out the password to the box
    pass_entry.insert(0, password)

# ---------------------------- PASSWORD FINDER ------------------------------- #

def find_password():
    """This function goes and finds the password for the website they have entered
    if there is no password for that website lets the user know"""
    # get the data they entered in order to search the data
    website = web_entry.get()

    try:
        # try opening the file for the passwords and getting the data
        # in the form of a list
        with open("data.json", "r", encoding= "uts-8") as data_file:
            data = json.load(data_file)

            # generate the email and password based on the website used to search
            email = data[website]["email"]
            password = data[website]["password"]

    except FileNotFoundError:
        # if the file doesn't exist write a pop up error saying you cant find any data
        messagebox.showerror(title="Error", message="No Data File Found")

    except KeyError:
        # if the website they are trying to use does not exist in the data
        # write error message
        messagebox.showerror(title="Error", message=f"No details for {website} exist")

    else:
        # if file exists and it contains the website info they are trying to use and
        # we have email and password generated write out a message with the details
        messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_pass():
    """-gets the values of the entry boxes
    -checks if the boxes are empty if ye it gives a warning to fill them out
    -if there is information in the boxes then asks if the user wants to save them
    -if user says yes, writes them in the data.text file
    -if no then we let them edit their entries
    -after the button has been clicked and information saved it deletes the entries
    in the website and password section"""
    # gets the values of the entries using the get()
    website = web_entry.get()
    email = em_usern_entry.get()
    password = pass_entry.get()

    new_data = {
        website : {
            "email" : email,
            "password" : password,
            }
        }

    # if the given fields are empty it comes up with an error
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please dont leave any fields empty!")
    else:
        try:
            # try opening a file and updating data that we want to put back in to the json.
            with open("data.json", "r", encoding= "uts-8") as data_file:
                # read old data and save to variable
                data = json.load(data_file)

        except FileNotFoundError:
            # in case file does not exist we create one and write the first entry(new_data)
            with open("data.json", "w", encoding= "uts-8") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            # update old data with the new data if the file exists already
            data.update(new_data)

            # then update the file with a new entry (data)
            with open("data.json", "w", encoding= "uts-8") as data_file:
            # save updated data in the json file
                json.dump(data, data_file, indent=4)
        finally:
            # delete the website and password sections after the add button has been pressed
            web_entry.delete(0, END)
            pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

# creating a window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# create canvas with logo
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)

em_usern_label = Label(text="Email/Username:")
em_usern_label.grid(column=0, row=2)

pass_label = Label(text="Password:")
pass_label.grid(column=0,row=3)

# input spaces (entry)
web_entry = Entry(width=24)
web_entry.grid(column=1, row=1)
web_entry.focus()

em_usern_entry = Entry(width=42)
em_usern_entry.grid(column=1, row=2, columnspan=2)
em_usern_entry.insert(0, "prosicnatalija98@gmail.com")

pass_entry = Entry(width=24)
pass_entry.grid(column=1, row=3)


# buttons
generate_pass_butt = Button(text="Generate Password",highlightthickness=0, command=password_generate)
generate_pass_butt.grid(column=2,row=3)

add_butt = Button(text="Add", width=39,highlightthickness=0, command=save_pass)
add_butt.grid(column=1, row=4, columnspan=2)

Search_butt = Button(text="Search", width=14, highlightthickness=0, command=find_password)
Search_butt.grid(column=2, row=1)

# main loop to keep window on
window.mainloop()
