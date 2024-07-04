# Responsible for collecting user input (amount of money depositing)
# Functions are something that is called to exectue a certain block of code and then can potentially return us a value
def deposit(): # Function
    # Reason for while loop: We are going to continually ask the user to deposit amount until they give us a valid amount
    while True: # Continues until we 'break out' of the loop
        amount = input("What would you like to deposit? $")
        if amount.isdigit(): # Checks if it is a digit. Note negative number will also not be allowed
            amount = int(amount) # Convert string 
            if amount > 0:
                break
            else: 
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")

    return amount # Once broken out we will return here and bring us this amount

deposit() # Calling the function (allows the function to run)




