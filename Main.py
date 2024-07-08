import random

# Responsible for collecting user input (amount of money depositing)
# Functions are something that is called to exectue a certain block of code and then can potentially return us a value
MAX_LINES = 3 # Wrote it in capital (writing method) because this a constant value and will not change
MAX_BET = 100
MIN_BET = 1
# Rows and coloumn in the slot machine
ROWS = 3 
COLS = 3

# Created a dictionary for all the items in the slot machine and the number is how valuable they are by how often they will appear
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = { # The more rarer it is the higher the multiplier
    "A": 5, 
    "B": 4,
    "C": 3,
    "D": 2
}

def check_winnings(columns, lines, bet, values):
    # Check the rows the user bet on and if they won, if they bet 2 lines it will check line 0* and 1* (index)
    winnings = 0
    winning_lines = []
    for line in range(lines): # Line 1 is 0, 2 = 1, 3 = 2, based off index
        symbol = columns[0][line] # Easy method is that we look at first element and check if the rest of the row is the same
        for column in columns: # Checking if the element in the column is the same as column[0], if not we break out 
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else: 
            winnings += values[symbol] * bet
            winning_lines.append(line + 1) # Checks what line they one (+ 1 is because it is an index, thus line 1 is 0 + 1)

    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols): # Generating items in the slot machine
    all_symbols = [] # Create a list of all values we can select from then randomly choose 3 of them, removes the value from the list and then chooses again
    # E.g. Symbol will be A, symbol_count will be 2
    for symbol, symbol_count in symbols.items(): # Gives us the key and value of dictionary
        for _ in range(symbol_count): # Loops through the symbol_count and adds it to all_symbols
            all_symbols.append(symbol) # Loops through A 2 times and adds

    columns = [] # Defining our columns list
    for col in range(cols): # Generate a column for every column we have, if we have 3 columns  we need to do everything 3 times
        column = [] # All codes here are just picking random values for each column
        current_symbols = all_symbols[:] # Duplicating the list and creating a new one
        for _ in range(rows): # Loop through the number of values we need to generate equal to number of rows
            value = random.choice(current_symbols) # Randomly finds a value from the copy list
            current_symbols.remove(value) # Then add the value to our column list
            column.append(value)
        
        columns.append(column) # Then add our column to our column list
     
    return columns

# Printing out the values in the slot machine, currently they will print vertically but we want it to be horizontal
def print_slot_machine(columns): # Transposing, -> currently [A, B, C] we want them to go down horizontally, do this for each row
    for row in range(len(columns[0])): # Determines the amount of rows based of elements in column, 0 is the starting index assuming the column has elements in it
        for i, column in enumerate(columns): 
            if i != len(columns) - 1: # A | B | C is correct not A | B | C |, do not need it the end, only twice
                print(column[row], end=" | ") # If i is equal to the max index than print I if not then don't
            else: # For above, if we have a column with 3 elements the maximum index is 2 
                print(column[row], end="") # End of the print, it will print 'nothing' for the other print it will be |
        # Everything above occurs on the same line, once completed it print will run creating a new line
        print() # Prints an empty line which forces the function to go to another line

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

#deposit()  Calling the function allows the function to run

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

def spin(balance):
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
# How parameters work: when we first create the paramters think of them like placeholders where they accept those values 
# In this case, for rows we are using ROWS = 3, same for cols and symbol_count
# This means that we can choose any other values for these parameters and it will run the function based on them 
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count) 
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on line(s):", *winning_lines) # * is called splat or unpack operator, it's going to pass every line from the winning_lines to the print function
    # E.g. if won lines 1 and 2 it it will say 1 2 
    return winnings - total_bet # Calculates how much they won and lost 

def main(): #If we end the program, we can just call this function to play the game again
    balance = deposit() # Initial balance is the amount deposited
    while True: # Allows us to continue playing
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
    
    print(f"You are left with ${balance}")
        
main()


