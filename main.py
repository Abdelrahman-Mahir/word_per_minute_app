from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Arial", 32, "bold")
NORMAL_FONT = ("Arial", 24, "normal")


# ---------------------------- GUI ------------------------------- #
main_window = Tk()
main_window.geometry("962x601")
main_window.title("Wordy / Minute")
main_window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
photo = PhotoImage(file='./keyboard.png')
main_window.iconphoto(False, photo)


title = Label(text="Wordy Per Minute",bg=BACKGROUND_COLOR, font=TITLE_FONT)
title.grid(row=0, column=0, padx=5, pady=5)

words_measured = 0
units = Label(text=f"{words_measured} : Words / Minute",bg=BACKGROUND_COLOR, font=NORMAL_FONT)
units.grid(row=0, column=1)

text_area = Text(bg="white", width=100, pady=5,padx=5)
text_area.grid(row=1,column=0, columnspan=2)

main_window.mainloop()

