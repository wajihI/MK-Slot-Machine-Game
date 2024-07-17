import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import pygame
import threading

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

# Updated symbol counts for balanced odds
symbol_count = {
    "Scorpion": 4,
    "Sub-Zero": 5,
    "Raiden": 6,
    "Liu Kang": 7
}

symbol_value = {
    "Scorpion": 5,
    "Sub-Zero": 4,
    "Raiden": 3,
    "Liu Kang": 2
}

# Initialize Pygame for sound
pygame.mixer.init()

def load_sounds():
    sounds = {
        "spin": pygame.mixer.Sound("sounds/spin.wav"),
        "win": pygame.mixer.Sound("sounds/win.wav"),
        "lose": pygame.mixer.Sound("sounds/lose.wav")
    }
    return sounds

def play_sound(sound, sounds):
    sounds[sound].play()

def load_images(symbols):
    images = {}
    for symbol in symbols:
        # Load and resize images with transparent borders
        image = Image.open(f"images/{symbol}.png").convert("RGBA")
        image = image.resize((100, 100), Image.LANCZOS)

        # Create alpha channel mask to make borders transparent
        datas = image.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        image.putdata(newData)

        # Convert Image object to PhotoImage for tkinter
        img = ImageTk.PhotoImage(image)
        images[symbol] = img

    return images

def load_background_music():
    pygame.mixer.music.load("sounds/background.mp3")

def play_background_music():
    pygame.mixer.music.play(-1)  # Loop indefinitely

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
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

def animate_spin(images, frame):
    for _ in range(20):  # Adjust number for animation duration
        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
        for row in range(len(slots[0])):
            for i, column in enumerate(slots):
                label = frame.grid_slaves(row=row, column=i)[0]
                img = images[column[row]]
                label.config(image=img)
                label.image = img
        frame.update_idletasks()
        frame.after(50)  # Adjust speed

def print_slot_machine(columns, frame):
    images = load_images(symbol_count)
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            img = images[column[row]]
            lbl = tk.Label(frame, image=img)
            lbl.image = img
            lbl.grid(row=row, column=i, padx=10, pady=10)

def deposit(balance_var):
    amount = simpledialog.askinteger("Deposit", "What would you like to deposit?")
    if amount and amount > 0:
        balance_var.set(amount)
    else:
        messagebox.showerror("Invalid Amount", "Please enter a number greater than 0.")

def get_number_of_lines():
    lines = simpledialog.askinteger("Lines", f"Enter the number of lines to bet on (1-{MAX_LINES})")
    if lines and 1 <= lines <= MAX_LINES:
        return lines
    else:
        messagebox.showerror("Invalid Input", f"Please enter a number between 1 and {MAX_LINES}.")

def get_bet():
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

    threading.Thread(target=animate_spin, args=(load_images(symbol_count), frame)).start()
    frame.after(2000, lambda: show_results(balance_var, frame, lines, bet, sounds))

def show_results(balance_var, frame, lines, bet, sounds):
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots, frame)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    if winnings > 0:
        play_sound("win", sounds)
    else:
        play_sound("lose", sounds)
    result_message = f"You won ${winnings}.\nYou won on lines: {', '.join(map(str, winning_lines))}"
    messagebox.showinfo("Results", result_message)
    balance_var.set(balance_var.get() + winnings - (bet * lines))

def main():
    root = tk.Tk()
    root.title("Mortal Kombat Slot Machine")

    # Set background image
    bg_image = Image.open("images/mortal_kombat_logo.png")
    bg_image = ImageTk.PhotoImage(bg_image.resize((800, 600), Image.LANCZOS))
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    sounds = load_sounds()
    load_background_music()
    play_background_music()

    balance_var = tk.IntVar()

    deposit_button = tk.Button(root, text="Deposit", command=lambda: deposit(balance_var), width=10, height=2, font=("Arial", 12))
    deposit_button.pack(pady=10)

    play_frame = tk.Frame(root)
    play_frame.pack()

    play_button = tk.Button(root, text="Play", command=lambda: spin(balance_var, play_frame, sounds), width=10, height=2, font=("Arial", 12))
    play_button.pack(pady=10)

    balance_label = tk.Label(root, textvariable=balance_var, font=("Arial", 14))
    balance_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
