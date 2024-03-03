# Read account balances from csv file
import csv      # The import used in csv reading
accFile = open('accounts.csv')     # Open the csv file
csvreader = csv.reader(accFile)    # Create a reader for csv file
accBalance = {}             # Create an empty dictionary to store csv cells
accHeader = next(csvreader)             # Read first row (headers)
for row in csvreader:       # Loop over the remaining rows
    accBalance[row[0]] = float(row[1])  # add csv row to dictionary
accFile.close()        # Close the csv file

# Read ATM balance from csv file
atmFile = open('atmBalance.csv')   # Open the csv file
csvreader = csv.reader(atmFile)    # Create a reader for csv file
atmHeader = next(csvreader)     # Skip first row (headers)
row = next(csvreader)   # Read second row 
atmBalance = float(row[0])     # Get reading from row column 0
atmFile.close()        # Close the csv file

# Amount of withdraws, deposits and fees
withdraw = 0
deposit = 0
fee = 0

# Display initial menu to select a customer or operator
topLevelMenu = True;    # repeat condition for displaying top-level menu
while(topLevelMenu):    # Keep displaying top-level menu
    # Display top-level menu
    print("1. Enter Account Number")
    print("2. Operator Login")
    print("3. Exit")
    # Get user input to select which rule
    userInput = input("Please enter your selection number: ")
    if userInput == "1":        # Customer operations
        accNumber = input("Please enter account number: ")  # Get user input for account number
        if accNumber in accBalance:     # check if the user input account number is found in bank accounts
            bottomLevelMenu = True;    # repeat condition for displaying bottom-level menu
            while(bottomLevelMenu):
                # Display all the available options for customer when his account is found
                print("1. Withdraw")
                print("2. Deposit")
                print("3. Balance")
                print("4. Exit")
                userInput = input("Please enter your selection number: ")   # Get customer input for which operation he wants
                match userInput:    # Test the input against all the available operations
                    case '1':   # Withdraw operation
                        # Get user input about the amount of money to withdraw
                        amount = float(input("Please enter amount to withdraw: "))
                        if amount < 1:  # The minimum amount is 1
                            print("Error: Minimum value is 1")  # display explanatory error message
                        elif amount > 100:  # The minimum amount is 100
                            print("Error: Maximum value is 100")    # display explanatory error message
                        elif amount+1.5>accBalance[accNumber]:    # The user does not have enough funds in hi account (amount + fees)
                            print("Error: No enough fund in your account")  # display explanatory error message
                        elif amount>atmBalance:     # The amount is not found in atm balance
                            print("Error: No enough cash in this ATM. Please check later.") # display explanatory error message
                        else:       # No error. Perform withdraw operation
                            withdraw = withdraw + amount    # Update the withdraw statistics
                            fee = fee + 1.5     # Update the fees statistics
                            atmBalance = atmBalance - amount  # remove amount from atm balance
                            accBalance[accNumber] = accBalance[accNumber] - (amount+1.5)    # update the account balance
                            # Find quantities and denominations to be provided to the customer
                            money = [20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.01]    # The available notes and coins
                            print("Output notes and coins are:")    # Header output
                            for m in money:     # Repeat over the available notes and coins
                                count = int(amount//m)   # When dividing the amount by note value, the integer is how many notes will be output. Convert to integer to be printed without .0
                                if count:   # If the count is not zero
                                    print(count, "of", m)   # display how many of this note or coin
                                amount = amount%m   # Update the amount with the remaining part
                                if amount==0:   # If the amount is covered entirely
                                    break   # Stop looping
                    case '2':   # Deposit operation
                        # Get user input about the amount of money to deposit
                        amount = float(input("Please enter amount to deposit: "))
                        if atmBalance+amount>10000:     #An ATM will never stock more than £10,000
                            print("Error in deposit. Please try again later") # display explanatory error message
                        else:
                            accBalance[accNumber] = accBalance[accNumber] + (amount-1.5) # add amount to account balance, without fees
                            atmBalance = atmBalance + amount # add amount to atm balance
                            deposit = deposit + amount    # Update the withdraw statistics
                            fee = fee + 1.5     # Update the fees statistics
                        print("Deposit successful")
                    case '3':   # Balance enquiry operation
                        print("Your account balance = ", accBalance[accNumber])
                    case '4':   # Exit operation
                        bottomLevelMenu = False     # Do not display bottom-level menu after this
                    case _:     # The user selected an invalid option
                        print("Error. Please select a valid operation")
        else:   # The account number is not found in bank system
            print("Error: account number not found")
    elif userInput == "2":      # Operator operations
        password = input("Please enter your password: ")
        if password=="MaintOp01":
            bottomLevelMenu = True;    # repeat condition for displaying bottom-level menu
            while(bottomLevelMenu):
                # Display all the available options for operator when the password is correct
                print("1. Refill")
                print("2. Empty")
                print("3. Statistics")
                print("4. Shutdown")
                print("5. Exit")
                userInput = input("Please enter your selection number: ")
                match userInput:    # Test the input against all the available operations
                    case '1':   # Refill operation
                        # Get user inputs about the amount of notes and coins to refill
                        note20L = int(input("How many note £20 entered?"))
                        note10L = int(input("How many note £10 entered?"))
                        note5L = int(input("How many note £5 entered?"))
                        coin2L = int(input("How many coin £2 entered?"))
                        coin1L = int(input("How many coin £1 entered?"))
                        coin50p = int(input("How many coin 50p entered?"))
                        coin20p = int(input("How many coin 20p entered?"))
                        coin10p = int(input("How many coin 10p entered?"))
                        coin5p = int(input("How many coin 5p entered?"))
                        coin2p = int(input("How many coin 2p entered?"))
                        coin1p = int(input("How many coin 1p entered?"))
                        # The added amount is each count of note or coin multiplied by note or coin value
                        amount = note20L*20 + note10L*10 + note5L*5 + coin2L*2 + coin1L*1 +  coin50p*0.5 + coin20p*0.2 + coin10p*0.1 + coin5p*0.05 + coin2p*0.02 + coin1p*0.01
                        if (atmBalance + amount)>10000:     # Check if the ATM balance will exceed the limit, do not refill
                            print("Error. ATM cannot contain more that £10000")       # display explanatory error message  
                        else:   # Update atm balance by accumulating the added amount
                            atmBalance = atmBalance + amount
                    case '2':   # Empty operation
                        atmBalance = 0;     # Empty the atm by setting its amount as zero
                        print("Successful: ATM is empty")   # Display informative message.
                    case '3':   # Statistics operation
                        import matplotlib.pyplot as plt 
                        plt.bar(['withdraw', 'deposit', 'fees'], [withdraw,deposit,fee])
                        plt.show()
                    case '4':   #Shutdown operation
                        accFile = open('accounts.csv', 'w', newline='')     # Open the csv file
                        csvwriter = csv.writer(accFile)    # Create a writer for csv file
                        csvwriter.writerow([accHeader[0], accHeader[1]])      # Write header read before
                        for key,value in accBalance.items():       # Loop over the accounts
                            csvwriter.writerow([key, value])        # add account to csv as row
                        accFile.close()        # Close the csv file

                        # Read ATM balance from csv file
                        atmFile = open('atmBalance.csv', 'w', newline='')   # Open the csv file
                        csvwriter = csv.writer(atmFile)    # Create a reader for csv file
                        csvwriter.writerow(atmHeader)      # Write header read before
                        csvwriter.writerow([atmBalance])
                        atmFile.close()        # Close the csv file
                    case '5':   # Exit operation
                        bottomLevelMenu = False     # Do not display bottom-level menu after this
                    case _:     # The user selected an invalid option
                        print("Error. Please select a valid operation")
        else:   # Wrong password
            print("Wrong password. Try again.") # Print error message
    elif userInput == "3":      # Exit
        topLevelMenu = False            # Do not display top-level menu after this
        print("Thanks for using our ATM")   # Thank you message
    else:                       # The user entered invalid rule
        print("Error. Please select 1, 2 or 3 only")    # Print error message