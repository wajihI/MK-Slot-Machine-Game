import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk
import pygame

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
JACKPOT_AMOUNT = 500

ROWS = 3
COLS = 3

symbol_count = {
    "Scorpion": 2,
    "Sub-Zero": 4,
    "Raiden": 6,
    "Liu Kang": 8
}

symbol_value = {
    "Scorpion": 5,
    "Sub-Zero": 4,
    "Raiden": 3,
    "Liu Kang": 2
}

JACKPOT_SYMBOL = "Scorpion"

# Initialise Pygame for sound
pygame.mixer.init()

def load_sounds():
    sounds = {
        "spin": pygame.mixer.Sound("sounds/spin.wav"),
        "win": pygame.mixer.Sound("sounds/win.wav"),
        "lose": pygame.mixer.Sound("sounds/lose.wav")
    }
    return sounds

def load_background_music():
    pygame.mixer.music.load("sounds/background.mp3")

def play_sound(sound, sounds):
    sounds[sound].play()

def play_background_music():
    pygame.mixer.music.play(-1) # Loops indefinitely

def load_images(symbols):
    images = {}
    for symbol in symbols:
        images[symbol] = Image.open(f"images/{symbol}.png")
    return images

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    jackpot = False
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
            if symbol == JACKPOT_SYMBOL:
                jackpot = True

    if jackpot:
        winnings += JACKPOT_AMOUNT
        winning_lines.append("Jackpot!")

    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot_machine(columns, frame):
    images = load_images(symbol_count)
    for widget in frame.winfo_children():
        widget.destroy()
    for row in range(len(columns[0])):
        row_frame = tk.Frame(frame)
        row_frame.pack(side="top")
        for i, column in enumerate(columns):
            img = ImageTk.PhotoImage(images[column[row]])
            lbl = tk.Label(row_frame, image=img)
            lbl.image = img
            lbl.pack(side="left")

def deposit(balance_var):
    while True:
        amount = simpledialog.askinteger("Deposit", "What would you like to deposit?")
        if amount and amount > 0:
            balance_var.set(amount)
            break
        else:
            messagebox.showerror("Invalid Amount", "Please enter a number greater than 0.")

def get_number_of_lines():
    while True:
        lines = simpledialog.askinteger("Lines", f"Enter the number of lines to bet on (1-{MAX_LINES})")
        if lines and 1 <= lines <= MAX_LINES:
            return lines
        else:
            messagebox.showerror("Invalid Input", f"Please enter a number between 1 and {MAX_LINES}.")

def get_bet():
    while True:
        amount = simpledialog.askinteger("Bet", f"What would you like to bet on each line? (${MIN_BET}-${MAX_BET})")
        if amount and MIN_BET <= amount <= MAX_BET:
            return amount
        else:
            messagebox.showerror("Invalid Bet", f"Please enter a number between ${MIN_BET} and ${MAX_BET}.")

def spin(balance_var, frame, sounds):
    play_sound("spin", sounds)
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance_var.get():
            messagebox.showerror("Insufficient Funds", f"You do not have enough to bet that amount, your current balance is: ${balance_var.get()}")
        else:
            break

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots, frame)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    if winnings > 0:
        play_sound("win", sounds)
    else:
        play_sound("lose", sounds)
    result_message = f"You won ${winnings}.\nYou won on lines: {', '.join(map(str, winning_lines))}"
    if "Jackpot!" in winning_lines:
        result_message += "\nJackpot!"
    messagebox.showinfo("Results", result_message)
    return winnings - total_bet

def main():
    root = tk.Tk()
    root.title("Mortal Kombat Slot Machine")
    sounds = load_sounds()
    load_background_music()
    play_background_music()

    balance_var = tk.IntVar()

    deposit_button = tk.Button(root, text="Deposit", command=lambda: deposit(balance_var))
    deposit_button.pack()

    play_frame = tk.Frame(root)
    play_frame.pack()

    play_button = tk.Button(root, text="Play", command=lambda: balance_var.set(balance_var.get() + spin(balance_var, play_frame, sounds)))
    play_button.pack()

    balance_label = tk.Label(root, textvariable=balance_var)
    balance_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
