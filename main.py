from tkinter import *
from text_class import TextScrollCombo
from random_words import WordList
from tkinter import ttk
from ttkthemes import ThemedTk
import os

# TODO: Add high score file saving function
# TODO: look into highlighting and following the words
# TODO: Remove 1 from CPM when backspace is pressed
# TODO: Add difficulty control by controlling the lenght of the words. Probably, means editing the class file, and asking for user input
# TODO: The high score file should keep the history of the user with the date
# TODO: Look into themes?
# TODO: resolve the issue of having the delete button messing up with the words counter
# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 32, "bold")
NORMAL_FONT = ("Arial", 24, "normal")


# ---------------------------- FUNCTIONS ------------------------------- #

def start_countdown(event):
    global duration
    if duration == 60:
        count_down()


def count_down():
    global duration
    if duration > 0:
        duration -= 1
        timer_label.config(text=f"Time Remaining: {duration}")
        main_window.after(1000, count_down)
    else:
        timer_label.config(text="Time's Up!")
        typing_area.txt.config(state="disable")
        if correct_words_measured.get() > high_score_tracker("read"):
            high_score_tracker("update", new_score=correct_words_measured.get())
            high_score_label.config(text=f"User High Score: {correct_words_measured.get()}")
            print("It's updated")


def space_listener(event):
    global words_measured
    if event.keysym == "space":
        words_measured.set(words_measured.get() + 1)
        text = typing_area.txt.get("1.0", 'end-1c')
        text_list = text.split()
        test_list = sample_text.split()
        test_list_sliced = test_list[:words_measured.get()]
        for i in range(words_measured.get() - 1, words_measured.get()):
            if text_list[i] == test_list_sliced[i]:
                print(f"They match {text_list[i]}") # This line is to keep track of how the code is running
                correct_words_measured.set(correct_words_measured.get() + 1)
                words_label.config(text=f"{correct_words_measured.get()}: Words / Minute")
            else:
                # This line is to keep track of how the code is running
                print(f"They don't match {text_list[i]} and {test_list_sliced[i]}")


def char_listener(event):
    global char_measured
    pressed_key = event.keysym
    if len(pressed_key) == 1 and duration > 0:  # activate only when a letter is pressed, not space, shift, etc
        char_measured.set(char_measured.get() + 1)
        char_label.config(text=f"CPM: {char_measured.get()}")


def high_score_tracker(operation, new_score=0):  # High score tracker
    if operation == "read":
        with open("high_score.txt", mode="a+") as file:
            if os.path.getsize('high_score.txt') == 0:
                initialized_score = 0
                file.write(f"User's Highest Score: {initialized_score}")
                return initialized_score
            else:
                file.seek(0)  # Move the cursor back to the Start of the line
                data = file.readline()
                text = data.split()
                existing_score = int(text[-1])
                return existing_score
    elif operation == "update":
        with open("high_score.txt", mode="w") as file:
            file.write(f"User's Highest Score: {new_score}")
            return new_score


# ---------------------------- Variables Initialization ------------------------------- #
words = WordList()
sample_text = " ".join(words.generate())

# ---------------------------- GUI ------------------------------- #
# Window setup
main_window = ThemedTk(theme="Adapta")
main_window.geometry("962x601")
main_window.title("Wordy / Minute")
main_window.config(padx=5, pady=5)
photo = PhotoImage(file='./keyboard.png')
main_window.iconphoto(False, photo)

# Title
title = ttk.Label(text="Wordy Per Minute", font=TITLE_FONT)
title.grid(row=0, column=0, padx=5, pady=5, columnspan=4)

# High score Label and Variable
high_score_var = IntVar()
high_score_var.set(high_score_tracker("read"))
high_score_label = ttk.Label(text=f"User High Score: {high_score_var.get()}", font=NORMAL_FONT)
high_score_label.grid(row=1, column=0, padx=0)

# CPM Label and Variable
char_measured = IntVar()
char_measured.set(0)
char_label = ttk.Label(text=f"CPM: {char_measured.get()}", font=NORMAL_FONT)
char_label.grid(row=1, column=2, padx=0)

# WPM Label and variable
words_measured = IntVar()
words_measured.set(0)
correct_words_measured = IntVar()
correct_words_measured.set(0)
words_label = ttk.Label(text=f"{correct_words_measured.get()} : Words / Minute", font=NORMAL_FONT)
words_label.grid(row=1, column=3)

# Text Area
combo = TextScrollCombo(main_window)
combo.txt.insert(END, sample_text)
combo.grid(row=2, column=0, columnspan=4, pady=5, padx=15)
combo.config(width=900, height=200)
combo.txt.config(font=("consolas", 12), undo=True, wrap='word', state="disable")
combo.txt.config(borderwidth=3, relief="flat")

# Typing Area
typing_area = TextScrollCombo(main_window)
typing_area.grid(row=3, column=0, columnspan=4, pady=5, padx=15)
typing_area.config(width=900, height=200)
typing_area.txt.config(font=("consolas", 12), undo=True, wrap='word')
typing_area.txt.config(borderwidth=3, relief="flat")

# Timer
duration = 60
timer_label = ttk.Label(text=f"Time Remaining: {duration}", font=NORMAL_FONT)
timer_label.grid(row=4, column=0, columnspan=2)

# ---------------------------- Event Listener ------------------------------- #
main_window.bind("<KeyPress>", space_listener, add="+")
main_window.bind("<KeyPress>", start_countdown, add="+")
main_window.bind("<KeyPress>", char_listener, add="+")

main_window.mainloop()
