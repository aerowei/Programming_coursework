# Importing the necessary modules for this exercise. Tkinter will be used to build the GUI. Random will be used to
# choose a random word from the word list.

import random
from tkinter import *
from tkinter import messagebox

# Setting up the tkinter window.
window = Tk()
window.title("Hangman game")
window.geometry("800x800")

# Global variables that I'll use in the program
win_count = 0
lives = 8
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']  # List with ASCII uppercase letters.

# Creating a list of hangman images, and placing the first image.
hg_list = []
for i in range(1, 10):
    s = "hg" + str(i) + ".png"
    hg_list.append(PhotoImage(file=s))
hg_img = Label(window, image=hg_list[0])
hg_img.place(x=100, y=100)
img_nr = 0 # Indicate which picture number it is now.

# Open the file wordlist.txt for reading and read the first line, removing all the whitespaces at beginning and end and
# turning all characters to lowercase
file = open(r'wordlist.txt', 'r')
words = []
word = file.readline().strip().lower()

# Loop through each line, one at a time, and add each word to the 'words' list.
while word: # Note for this loop - I can include a 'difficulty' maybe later.
    if word.isalpha(): # I use .isalpha() because there are some words with special characters(too lazy to remove them)
        words.append(word)
    word = file.readline().strip().lower()

# Function returns a random word from the 'words' list. Will be used with the button 'try again' later in the code.
def ranword():
   s = random.choice(words)
   return s

# Random chosen word using ranword() function. Felt that saving it in a variable will be more useful.
hgword = ranword()

# Create labels and append them to lbl_list, each label containing "_" character as text, then place them on the screen.
lbl_list = []
x_lbl = 200
for i in range(len(hgword)):
    lbl_list.append(Label(window, text='_', font=('Arial', 40, 'bold')))
    lbl_list[-1].place(x=x_lbl, y=300)
    x_lbl += 50

# Create buttons
# List with each button's location. Scraped this idea for now as I think there's a nicer method for that.
# btn_loc = [['A',100,200],['B',120,200],['C',140,200],['D',160,200],['E',180,200],['F',200,200],['G',220,200],
#            ['H',240,200],['I',260,200],['J',280,200],['K',300,200],['L',320,200],['M',340,200],['N',370,200],
#             ['O',250,200],['P',250,200],['Q',250,200],['R',250,200],['S',250,200],['T',250,200],['U',250,200],
#              ['V',250,200],['W',250,200],['X',250,200],['Y',250,200],['Z',250,200]]

# Creating x and y coordinate variable for buttons. Will be used to determine their position.
x_btn = 300
y_btn = 400

btn_lst = [] # Actual list containing each button.
# This loop creates each button, adds it to the list and then places them on the screen.
for alpha in alphabet:
    btn_lst.append(Button(window, text=alpha, font=('Arial',15,'bold'),
                          command=lambda c=alpha.lower(): click_btn(c))) # Using c=alpha to store it for each iteration.
    btn_lst[-1].place(x=x_btn,y=y_btn)
    x_btn += 40
    if x_btn > 650:
        y_btn += 55
        x_btn = 300

# The main function that the buttons will use. Will check if the clicked button's letter is in the random word, and
# add win_count if letter is in the word or subtract lives if the letter isn't. Clicking on the button will also
# disable it.
def click_btn(let):
    i = 0
    global win_count
    global lives
    if let in hgword:       # Checks if letter is in the random chosen word.
        for elem in hgword: # Iterates through every character in the string (random chosen word)
            if elem == let:
                lbl_list[i].configure(text=let) # Swaps the text in the labels with "_" to corresponding letter.
                win_count += 1
            i += 1
        for btn in btn_lst: # Finds the button with the letter and disables it.
            if btn["text"].lower() == let:
                btn["state"] = DISABLED
        if win_count == len(hgword):    # Winning condition.
            messagebox.askyesno(title="You won!", message="You won, do you want to retry?")
            print('You win!')
            window.destroy()
    else:
        lives -= 1
        print(lives)
        hg_place()
        for btn in btn_lst:
            if btn["text"].lower() == let:
                btn["state"] = DISABLED
        if lives == 0:   # Losing condition
            if messagebox.askyesno(title="You lost!", message="You lost, do you want to retry?") == False:
                window.destroy()
            else:
                print("test")
           # print('You lose!')
          #  window.destroy()


def hg_place():
    global hg_list
    global hg_img
    global img_nr

    img_nr += 1
    if img_nr < 9:
        hg_img.configure(image = hg_list[img_nr])

def retry():
    global lives
    global win_count
    global hgword
    global lbl_list
    global btn_lst

    hgword = ranword()
    lives = 8
    win_count = 0
    i = 0
    for i in range (len(hgword)):
        lbl_list[i].configure(text="_")
    for btn in btn_lst:
        btn["state"] = NORMAL


print(hgword)
window.mainloop()
