from tkinter import *
import time
from text_class import TextScrollCombo
import tkinter.ttk as ttk
from random_words import WordList

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
        remaining_time.config(text=f"{duration}")
        main_window.after(1000, count_down)
    else:
        remaining_time.config(text="Time's Up!")
        typing_area.txt.config(state="disable")


def space_listener(event):
    global words_measured
    if event.keysym == "space":
        words_measured.set(words_measured.get() + 1)
        text = typing_area.txt.get("1.0", 'end-1c')
        text_list = text.split()
        test_list = sample_text.split()
        test_list_sliced = test_list[:words_measured.get()]
        for i in range(words_measured.get() - 1, words_measured.get()):
            # print(f"This's from Sample Text:             {test_list[i]}")
            # print(f"This's from user input:             {text_list[i]}")
            if text_list[i] == test_list_sliced[i]:
                print(f"They match {text_list[i]}")
                correct_words_measured.set(correct_words_measured.get() + 1)
                word_count.config(textvariable=correct_words_measured)
            else:
                print(f"They don't match {text_list[i]} and {test_list_sliced[i]}")


def char_listener(event):
    global char_measured
    pressed_key = event.keysym
    if len(pressed_key) == 1 and duration > 0:  # activate only when a letter is pressed, not space, shift, etc
        char_measured.set(char_measured.get() + 1)
        char_count.config(textvariable=char_measured)


# ---------------------------- Variables Initialization ------------------------------- #
words = WordList()
sample_text = " ".join(words.generate())
# sample_text = ("river call south girl final out do part bird develop note but water something come as science road")

# ---------------------------- GUI ------------------------------- #
main_window = Tk()
main_window.geometry("962x601")
main_window.title("Wordy / Minute")
main_window.config(bg=BACKGROUND_COLOR, padx=5, pady=5)
photo = PhotoImage(file='./keyboard.png')
main_window.iconphoto(False, photo)

title = Label(text="Wordy Per Minute", bg=BACKGROUND_COLOR, font=TITLE_FONT)
title.grid(row=0, column=0, padx=5, pady=5, columnspan=4)

char_count = Label(text="CPM:", bg=BACKGROUND_COLOR, font=NORMAL_FONT)
char_count.grid(row=1, column=0, padx=0)
char_measured = IntVar()
char_measured.set(0)
char_count = Label(textvariable=char_measured, bg=BACKGROUND_COLOR, font=NORMAL_FONT)
char_count.grid(row=1, column=1, padx=0)

words_measured = IntVar()
words_measured.set(0)
correct_words_measured = IntVar()
correct_words_measured.set(0)
word_count = Label(textvariable=correct_words_measured, bg=BACKGROUND_COLOR, font=NORMAL_FONT)
word_count.grid(row=1, column=2, padx=0)
words_label = Label(text=": Words / Minute", bg=BACKGROUND_COLOR, font=NORMAL_FONT)
words_label.grid(row=1, column=3)

combo = TextScrollCombo(main_window)
combo.txt.insert(END, sample_text)
# text_area.grid(row=1, column=0, columnspan=3)
combo.grid(row=2, column=0, columnspan=4, pady=5)
combo.config(width=600, height=200)
combo.txt.config(font=("consolas", 12), undo=True, wrap='word', state="disable")
combo.txt.config(borderwidth=3, relief="flat")
style = ttk.Style()
style.theme_use('clam')

typing_area = TextScrollCombo(main_window)
typing_area.grid(row=3, column=0, columnspan=4, pady=5)
typing_area.config(width=600, height=200)
typing_area.txt.config(font=("consolas", 12), undo=True, wrap='word')
typing_area.txt.config(borderwidth=3, relief="flat")


timer_label = Label(text="Time Remaining", bg=BACKGROUND_COLOR, font=NORMAL_FONT)
timer_label.grid(row=4, column=0, columnspan=2)
duration = 60
remaining_time = Label(text=f"{duration}", font=NORMAL_FONT)
remaining_time.grid(row=4, column=2, columnspan=2)

# ---------------------------- Event Listener ------------------------------- #
main_window.bind("<KeyPress>", space_listener, add="+")
main_window.bind("<KeyPress>", start_countdown, add="+")
main_window.bind("<KeyPress>", char_listener, add="+")
main_window.mainloop()
