from tkinter import *
from text_class import TextScrollCombo
from random_words import WordList
from tkinter import ttk
from ttkthemes import ThemedTk
import os
from difficulty_dropdown import DifficultDropDown
from datetime import datetime

# TODO: resolve the issue of having the delete button messing up with the words counter
# TODO: resolve the issue of the timer starting automatically after restarting the game
# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 32, "bold")
NORMAL_FONT = ("Arial", 18, "normal")


# ---------------------------- FUNCTIONS ------------------------------- #

def start_countdown(event):
    if duration == 60 and len(event.keysym) == 1:
        print(event.keysym)
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
        typed_text = "" # This line is to ensure a new start after restarting
        test_list = []  # This line is to ensure a new start after restarting
        words_measured.set(words_measured.get() + 1)
        typed_text = typing_area.txt.get("1.0", 'end-1c')
        typed_text_list = typed_text.split()
        test_list = sample_text.split()
        test_list_sliced = test_list[:words_measured.get()]
        highlight_word(test_list_sliced[words_measured.get() -1])
        # print(f"words_measured: {words_measured.get()}")
        # print(f"typed_text_list: {typed_text_list}")
        # print(f"test_list_sliced: {test_list_sliced}")
        for i in range(words_measured.get() - 1, words_measured.get()):
            if typed_text_list[i] == test_list_sliced[i]:
                print(f"They match {typed_text_list[i]}") # This line is to keep track of how the code is running
                correct_words_measured.set(correct_words_measured.get() + 1)
                words_label.config(text=f"{correct_words_measured.get()}: Words / Minute")
            else:
                # This line is to keep track of how the code is running
                print(f"They don't match {typed_text_list[i]} and {test_list_sliced[i]}")


def char_listener(event):
    global char_measured
    pressed_key = event.keysym
    if len(pressed_key) == 1 and duration > 0:  # activate only when a letter is pressed, not space, shift, etc
        char_measured.set(char_measured.get() + 1)
        char_label.config(text=f"CPM: {char_measured.get()}")
    elif pressed_key == "BackSpace" and duration > 0 and char_measured.get() > 0:
        char_measured.set(char_measured.get() - 1)
        char_label.config(text=f"CPM: {char_measured.get()}")


def high_score_tracker(operation, new_score=0):  # High score tracker
    today = datetime.today().strftime('%d-%m-%Y')
    if operation == "read":
        with open("high_score.txt", mode="a+") as file:
            if os.path.getsize('high_score.txt') == 0:
                initialized_score = 0
                file.write(f"{today} User's Highest Score: {initialized_score}\n")
                return initialized_score
            else:
                file.seek(0)  # Move the cursor back to the Start of the line
                data = file.readlines()[-1]
                text = data.split()
                existing_score = int(text[-1])
                return existing_score
    elif operation == "update":
        with open("high_score.txt", mode="a") as file:
            file.write(f"{today} User's Highest Score: {new_score}\n")
            return new_score


def difficulty_level_changed(*args):
    difficulty_selector(lvl_dropdown.clicked.get())


def difficulty_selector(lvl):
    words = WordList()
    global sample_text
    text_area.txt.config(state="normal")

    if lvl == "Easy😪":
        max_length = 6
    elif lvl == "Medium😲":
        max_length = 7
    elif lvl == "Hard🥶":
        max_length = 8
    elif lvl == "Hell😈":
        max_length = 15
    else:
        max_length = 6  # Default to Easy if the level is not recognized

    sample_text = " ".join(words.generate(max_length=max_length))
    text_area.txt.delete("1.0", "end")
    text_area.txt.insert(END, sample_text)
    text_area.txt.config(state="disable")


# Call this function to highlight a specific word (e.g., "your_word_to_highlight")
def highlight_word(word_to_highlight):
    # Clear any existing highlighting
    text_area.txt.tag_delete("highlight")

    # Search for the word and highlight it
    start = "1.0"
    while True:
        start = text_area.txt.search(word_to_highlight, start, stopindex="end")
        if not start:
            break
        end = f"{start}+{len(word_to_highlight)}c"
        text_area.txt.tag_configure("highlight", background="yellow", foreground="black")
        text_area.txt.tag_add("highlight", start, end)
        start = end


def restart_window():
    global char_measured, words_measured, duration, words_measured
    char_measured.set(0)
    char_label.config(text=f"CPM: {char_measured.get()}")
    words_measured.set(0)
    correct_words_measured.set(0)
    words_label.config(text=f"{correct_words_measured.get()} : Words / Minute")
    typing_area.txt.config(state="normal")
    typing_area.txt.delete("1.0", "end")
    difficulty_selector(lvl_dropdown.clicked.get())
    duration = 60
    timer_label.config(text=f"Time Remaining: {duration}")
    main_window.bind("<KeyPress>", start_countdown, add="+")



# ---------------------------- GUI ------------------------------- #
# Window setup
main_window = ThemedTk(theme="Adapta")
main_window.geometry("1280x720")
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
char_label.grid(row=1, column=1, padx=0)

# WPM Label and variable
words_measured = IntVar()
words_measured.set(0)
correct_words_measured = IntVar()
correct_words_measured.set(0)
words_label = ttk.Label(text=f"{correct_words_measured.get()} : Words / Minute", font=NORMAL_FONT)
words_label.grid(row=1, column=2)

# Text Area
text_area = TextScrollCombo(main_window)
text_area.grid(row=2, column=0, columnspan=4, pady=5, padx=15)
text_area.config(width=1200, height=270)
text_area.txt.config(font=("consolas", 12), undo=True, wrap='word')
text_area.txt.config(borderwidth=3, relief="flat")

# Lvl Dropdown menu
lvl_dropdown = DifficultDropDown(main_window)
lvl_dropdown.grid(row=1, column=3)
# Bind the callback function to the difficulty dropdown
lvl_dropdown.clicked.trace_add("write", difficulty_level_changed)
# Initial call to set the text based on the initial difficulty level
difficulty_selector(lvl_dropdown.clicked.get())


# Typing Area
typing_area = TextScrollCombo(main_window)
typing_area.grid(row=3, column=0, columnspan=4, pady=5, padx=15)
typing_area.config(width=1200, height=270)
typing_area.txt.config(font=("consolas", 12), undo=True, wrap='word')
typing_area.txt.config(borderwidth=3, relief="flat")

# Timer
duration = 60
timer_label = ttk.Label(text=f"Time Remaining: {duration}", font=NORMAL_FONT)
timer_label.grid(row=4, column=0, columnspan=3)

# Restart Button
restart_btn = ttk.Button(text="Restart", command=restart_window)
restart_btn.grid(row=4, column=3)
# ---------------------------- Event Listener ------------------------------- #
main_window.bind("<KeyPress>", space_listener, add="+")
main_window.bind("<KeyPress>", start_countdown, add="+")
main_window.bind("<KeyPress>", char_listener, add="+")

main_window.mainloop()
