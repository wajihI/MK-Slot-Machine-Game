import random

# Responsible for collecting user input (amount of money depositing)
# Functions are something that is called to exectue a certain block of code and then can potentially return us a value
MAX_LINES = 3 # Wrote it in capital (writing method) because this a constant value and will not change
MAX_BET = 100
MIN_BET = 1
# Rows and coloumn in the slot machine
ROWS = 3 
COLS = 3

# Created a dictionary for all the items in the slot machine and the number is how valuable they are by how often they will apear
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

def get_slot_machine_spin(rows, cols, sumbols): 
    all_symbols = []
    

def deposit(): # Function
    # Reason for while loop: We are going to continually ask the user to deposit amount until they give us a valid amount
    while True: # Continues until we 'break out' of the loop
        amount = input("What would you like to deposit? $")
        if amount.isdigit(): # Checks if it is a digit. Note negative number will also not be allowed
            amount = int(amount) # Converts string to int
            if amount > 0:
                break
            else: 
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")

    return amount # Once broken out we will return here and bring us this amount

#deposit()  Calling the function (allows the function to run)

# Collect bet from the user - Need to determine how much they want to bet and how many lines
# Multiply bet amount by the number of lines, - Better finding out how many lines first then how much money

def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES})? ") #Reason for MAX_LINES is that changing the constant means more lines can be added to the game
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES: # Check if user input is within the boundaries set
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number")

    return lines

def get_bet(): # Getting the amount to bet
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - {MAX_BET}.")
        else:
            print("Please enter a number")

    return amount


def main(): #If we end the program, we can just call this function to play the game again
    balance = deposit() # Initial balance is the amount deposited
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance: 
            bet_max = int(balance/lines)
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
            print(f"Max amount that you can bet is: ${bet_max}")
        else: 
            break
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")
    

main()


