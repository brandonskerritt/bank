import csv
from monzo.monzo import Monzo # Import Monzo Class

class finance():
    """
    ** ATTRIBUTES **
    - initial_take_out
        how much is initially taken out of the bank account (leaving 20%)
    - updated_take_Out
        this is the same as initial_take_out but is updated in the program when 10% is removed
    - high_vol
        10% of updated_take_out
        remove 10% from updated_take_out
    - invest
        40% of updated_take_out
        remove 40% from updated_take_out
    - other_savings
        the rest of the 50% (the full updated_take_out) or 50% of initial_take_out
    
    ** METHODS **
    - __init__
        constructor
    - update_take_out
        used to update the attribute of same name
    - check
        checks to see if the result of adding high_vol + invest + other_savings is = to initial_take_out
    - printAll
        prints all the attributes nicely
    """

    def __init__(self, x):
        """ Constructor method """
        self.initial_natwest = x 

        latest_file = open("data.txt", "r")
        latest_file_read = latest_file.read().split(" ")
        latest = latest_file_read[0]
        latest = float(latest)
        self.natwest_balance = latest

        # If you've put in £50 and theres £100 in the account this will mess it up
        ## that's why absolute is used.
        # I also want to save 20% of the natwest account in the savings itself
        newly_added = float(abs(self.initial_natwest - latest))
        if self.natwest_balance > 600:
            self.initial_take_out = float(newly_added)
            self.more600 = True
            self.over60020Percent = newly_added * 0.2
        else:
            self.initial_take_out = float(newly_added * 0.8)
        self.updated_take_out = float(self.initial_take_out)

        latest_file.close()
        latest_file = open("data.txt", "w")
        latest_file_read.append(str(abs(self.initial_natwest - self.initial_take_out)))
        latest_file_data = ' '.join(latest_file_read)
        latest_file.write(latest_file_data)
        latest_file.close()

        self.high_vol = 0.0
        self.invest = 0.0
        self.other_savings = 0.0

        # vanguard requires at least £100 per month
        if self.updated_take_out * 0.40 < 100.0:
            if self.updated_take_out * 0.45 > 99.99:
                self.invest = self.updated_take_out * 0.45
                self.updateTakeout(self.invest)

                self.high_vol = self.updated_take_out * 0.05
                self.updateTakeout(self.high_vol)
            elif self.updated_take_out * 0.5 > 99.99:
                self.invest = self.updated_take_out * 0.5
                self.updateTakeout(self.invest)

                self.high_vol = self.updated_take_out * 0
                self.updateTakeout(self.high_vol)
        else:
            self.invest = self.updated_take_out * 0.40
            self.updateTakeout(self.invest)

            self.high_vol = self.updated_take_out * 0.10
            self.updateTakeout(self.high_vol)

        self.left_with = self.initial_take_out - (self.invest + self.high_vol)

        self.left_over = self.initial_natwest - self.initial_take_out

    def updateTakeout(self, money):
        """ Method to update the updated_take_out attrbutes"""
        self.updated_take_out = self.updated_take_out - money
    
    def check(self):
        addition = self.other_savings + self.invest + self.high_vol

        if addition == self.initial_take_out:
            return True
        else:
            return False
    
    def printAll(self):
        print("\nYou should take out £" + str(round(self.initial_take_out)) + " out of your NatWest account")
        if self.more600:
            print("You should invest £" + str(self.over60020Percent) + " into something")
        print("You should put £" + str(round(self.high_vol)) + " into cryptocurrencies")

        if self.high_vol > 50:
            print("    * Split 4 ways this is £" + str(round(self.high_vol / 4.00)))
            print("    * Split 3 ways this is £" + str(round(self.high_vol / 3.0)))

        print("You should put £" + str(round(self.invest)) + " into Vanguard LS 80")
        print("This leaves you with £" + str(round(self.left_with)))
        self.updateTakeout(30)
        print("Taking away your subscriptions (£30) this is £" + str(round(self.updated_take_out)))
        self.updateTakeout(75)
        print("Take away £75 for your chocolate addiction this is £ " + str(round(self.updated_take_out)))
        print("* 10% to put into a holiday pot is £" + str(round(self.updated_take_out * 0.10)))
        print("* Split over 4 weeks this is £" + str(round(self.updated_take_out / 4.0)))
        print("You should put roughly £" + str(round(self.updated_take_out / 11)) + " into each YNAB category")
        print("Left in your NatWest is £" + str(round(self.left_over)))

        if (self.left_with / 4.0) > 45.0:
            print("Overall this was a good financial month, well done!!")
            print("You should consider these things: ")
            print("    * Putting 10% (£" + str(round(self.left_with * 0.10)) + ") into a holiday pot")
            print("    * Reinvesting 20% (£" + str(round(self.left_with * 0.20)) + ") into the NatWest account")
        else:
            print("You'll have a better month ;)")


class monzoAPI():
    """
    Monzo API in a class I've built

    ** ATTRIBUTES **
    - spend_today
        how much money was spent today
    - balance
        your current monzo balance
    """
    def __init__(self):
        client = Monzo('access_token_goes_here') # Replace access token with a valid token found at: https://developers.getmondo.co.uk/
        account_id = client.get_first_account()['id'] # Get the ID of the first account linked to the access token
        balance = client.get_balance(account_id) # Get your balance object
        self.spend_today = balance['spend_today']
        self.balance = balance['balance']
        
    def get_transactions_api(self, account_id, client):
        # gets transactions from monzo
        return client.transactions(account_id)
    
    def parse_transactions(self, transactions):
        # parses the transactions into a list of dictionary items
        transactionsParsed = []
        for item in transactions:
            # Merchant
            try:
                merchant = item.merchant.name
            except AttributeError:
                merchant = "No name"
            except TypeError:
                merchant = "No merchant for this item"
            # Date
            date = item.created
            amount = float(item.amount)
            transactionsParsed.append({
                'date': date,
                'transaction': amount,
                'merchant': merchant})
        return transactionsParsed

        def sort_chronologically(transactions):
            # sorts the transactions chronologically
            transactions = sorted(transactions, key=lambda k: k['date'])
            return transactions

        def sort_months(transactions):
            # Store the dates in stored_transactions with Y/M dates
            sorted_transactions = {}
            for transaction in transactions:
                # Make a list of months
                month = transaction['date'].strftime("%y/%m")
                if month in sorted_transactions:
                    sorted_transactions[month].append(transaction)
                else:
                    sorted_transactions[month] = [transaction]
            print("sorted")
            ordered_transactions = {}
            for key in sorted(sorted_transactions.keys()):
                print(key)
                ordered_transactions[key] = sorted_transactions[key]
            print("sorted")
            print(ordered_transactions)
            return ordered_transactions

x = float(input("How much money do you have in your account? "))
obj = finance(x)
obj.printAll()
