# Importing the necessary modules for this exercise. Tkinter will be used to build the GUI. Random will be used to
# choose a random word from the word list. PIL is used to display the hangman image.

import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Setting up the tkinter window.
window = Tk()
window.title("Hangman game")
window.geometry("800x800")

# Global variables that I'll use in the program
win_count = 0 # Hidden score of the user. Each +1 means the user has guessed one letter of the random word.
# To win, win_count must be equal to random word's length.
lives = 8 # Lives of the user. If lives = 0 then it is GAME OVER
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']  # List with ASCII uppercase letters.

# Opening the hangman images and creating a list of them for storage
# and displaying the first image in the window (this will be its default state).

hg_list = []
for i in range(1, 10):
    s = "hg" + str(i) + ".png" # Name of hangman images, goes from hg1.png to hg9.png
    image = Image.open(s)
    image = image.resize((250, 250), Image.ANTIALIAS) # Resizing the image to be bigger as it was too small.
    hg_list.append(ImageTk.PhotoImage(image))

hg_img = Label(window, image=hg_list[0]) # The actual variable that will contain the picture that is currently displayed
# on screen
hg_img.place(x=50, y=100)
img_nr = 0 # img_nr = 0 will be the default state of the hg image.

file = open(r'wordlist.txt', 'r') # Open the file wordlist.txt for reading
words = [] # List where all the words will be stored.
word = file.readline().strip().lower() # Reads the first line, removes whitespace at beginning/end and sets all
# characters to lowercase.

# Loop through each line, one at a time, and add each word to the 'words' list.
while word: # Note for this loop - I can include a 'difficulty' maybe later.
    if word.isalpha(): # I use .isalpha() because there are some words with special characters(too lazy to remove them)
        words.append(word)
    word = file.readline().strip().lower()

# Function returns a random word from the 'words' list.
def ranword():
   s = random.choice(words)
   return s

# Random chosen word using ranword() function. Felt that saving it in a variable will be more useful.
hgword = ranword()

# Create labels, append them to lbl_list, each label containing "_" character as text, then place them on the screen.
lbl_list = []
x_lbl = 150 # X coordinate of the leftmost "_" character.
for i in range(len(hgword)): # This loop creates a number of text labels with "_" according to the random word's length.
    lbl_list.append(Label(window, text='_', font=('Arial', 50, 'bold')))
    lbl_list[-1].place(x=x_lbl, y=400) # Displays the latest added label to the list on the screen.
    x_lbl += 50

# Creating starting x and y coordinate variable for buttons. Will be used to generate the buttons.
x_btn = 100
y_btn = 500

btn_lst = [] # Actual list containing each button.
# This loop creates a button for each letter, adds it to the 'button list' and then displays them on the screen.
for alpha in alphabet:
    btn_lst.append(Button(window, text=alpha, font=('Arial',25,'bold'),
                          command=lambda c=alpha.lower(): click_btn(c))) # Using lambda to store the button's letter
    # so I can send it to click_btn() function, which is called when the button is clicked.
    btn_lst[-1].place(x=x_btn,y=y_btn) # Displays the latest added buttons on the screen.
    x_btn += 65
    if x_btn > 650: # IF condition shapes the buttons in more than 1 row.
        y_btn += 90
        x_btn = 100

# The main function that the buttons will use. Will check if the clicked button's letter is in the random word, and
# increase 'win_count' if letter is in the word or decrease 'lives' if the letter isn't. Clicking on the button will
# also disable it.
def click_btn(let):
    global win_count
    global lives
    i = 0

    if let in hgword:       # Checks if clicked button's letter is in the random chosen word.
        for char in hgword: # Iterates through every character in the random chosen word
            if char == let: # Compares clicked button's letter (let) with current character from the random chosen
                # word (char) to find the location of the letter(s) in the word
                lbl_list[i].configure(text=let.upper()) # Swaps the "_" in the label with the clicked button's letter.
                win_count += 1
            i += 1 # i is used to access a label at a specific location.
            # Corresponds to the current location in the ran. chosen word.
        for btn in btn_lst: # Finds the clicked button based on its letter and disables it.
            if btn["text"].lower() == let:
                btn["state"] = DISABLED
        if win_count == len(hgword):    # Winning condition.
            if messagebox.askyesno(title="You won!", message="You won, do you want to retry?") == False:
                window.destroy() # Creates a pop up window that asks user if he wants to retry another game.
            else:                # If not, then it will close the program.
                new_game()  # Will start a new game if clicked 'Yes'
    else:   # If the clicked button's letter is not in the random chosen word.
        lives -= 1
        hg_place() # This function changes hangman image to the next one, according to how many lives the user has left.
        for btn in btn_lst: # Finds the clicked button based on its letter and disables it.
            if btn["text"].lower() == let:
                btn["state"] = DISABLED
        if lives == 0:   # Losing condition
            if messagebox.askyesno(title="You lost!", message="You lost, do you want to retry?") == False:
                window.destroy()
            else:
                new_game()

def hg_place(): # This function changes the hangman image to the next one every time it's called.
    global hg_list
    global hg_img
    global img_nr

    img_nr += 1
    if img_nr < 9: # img_nr was always going above 8 (max index) so I had to put something to limit it to max 8.
        hg_img.configure(image = hg_list[img_nr])

def new_game(): # So many global variables.. this looks terrible.
    global lives
    global win_count
    global hgword
    global lbl_list
    global btn_lst
    global x_lbl
    global hg_img
    global hg_list
    global img_nr

    for lbl in lbl_list: # 'Destroying' the old "_" characters.
        lbl.destroy()
    lbl_list.clear() # Clearing the list to add the new "_" characters based on new random word length.
    hgword = ranword() # Choosing new random word.
    x_lbl = 150 # I wasn't sure how to change the number of "_" labels, so I just re-create them everytime.
    for i in range(len(hgword)): # Adding the new "_" labels to the label list variable.
        lbl_list.append(Label(window, text='_', font=('Arial', 40, 'bold')))
        lbl_list[-1].place(x=x_lbl, y=400)
        x_lbl += 50
    for btn in btn_lst: # Resetting buttons to their default state.
        btn["state"] = NORMAL
    lives = 8 # Resetting lives, win_count and img_nr variables to their 'initial' states.
    win_count = 0
    img_nr = 0
    hg_img.configure(image = hg_list[img_nr]) # Resetting the hangman image to its first state.


print(hgword)
window.mainloop()
