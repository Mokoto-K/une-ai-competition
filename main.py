# TODO - Fix up simulation class *
# TODO - Add logging for real trades, when they open, close, profit, etc
# TODO - Add scaling to features and addm more features
# TODO - implement size if test acct is used.
# TODO - Look at strategy for more control over trades and conditions
# TODO - implement a testing class for easier tuning of the nn
# TODO - Go through each file and look at the todos.
# TODO - Replace all limit orders with market orders 

import os
from dotenv import load_dotenv
from database import Database
from features import DataFeatures
from simulation import run_simulation
from strategy import build_strategy 
from exchange import Exchange

load_dotenv()


def get_choice() -> bool:
    """
    Gets choice of simulation or real trading mode
    """

    choice = None
    while choice == None:
        user = input("Please select a task: \n" +
            "Press 's' to run a simulation on the market \n" + 
            "Press 'r' to run a real trade in the market \n\n" +
            ">> ")
        print()
        if user.lower() == "s":
            choice = True
        elif user.lower() == "r":
            choice = False 
        else:
            print("Please check that you have input a valid option\n")
    os.system('cls||clear')
    return choice


def get_risk() -> str:
    """
    Gets the users choice of risk they would like to implement 

    Returns:
    risk - Either 1 for high risk of D for low risk, currently only two options
           representing timeframe intervals that the nn looks over in the data
    """

    risk = None
    while risk == None:
        user = input("\nEnter the risk strategy you would like to take:\n" +
                     "Press 'h' for high risk\n" + 
                     "Press 'l' for low risk\n\n" +
                     ">> ")
        print()
        if user.lower() == "h":
            risk = "1"
        elif user.lower() == "l":
            risk = "D"
        else:
            print("Please check you input a valid option\n")

    return risk


def take_action(decision) -> None:
    """
    Depending on the ai's decision and the current position in the market, an 
    action will be taken to either enter a position, maintain a position or 
    close a position.

    Params:
    position - The current direction we are in the market
    decision - The Neural networks decision on where to do next
    """
    
    # Create an instance of our exchange
    key: str = os.getenv("API_KEY")
    secret: str = os.getenv("API_SECRET")
    bybit = Exchange(key, secret, testnet= True)

    # Translate the nn decision to a market action
    decision = "Buy" if decision == 1 else "Sell"
    
    # Used for prettification of strings... and english... really
    direction = "Long" if decision == "Buy" else "Short"

    # Finds out if we are in a position or not. 
    position_details = bybit.get_position(symbol="BTC-28MAR25")
    position = position_details[0]

    # TODO -Rewrite this more eloquently you rusher!!!!!
    account_size = bybit.get_balance()
    if read_log_file()[6] == "None":
        starting_bal = account_size
    else:
        starting_bal = read_log_file()[6]
     
    account_size = float(account_size)

    # The last trades profit and loss
    lpnl = read_log_file()[4]

    if position != "":
        if position == decision:
            print(f"We are in a {direction} and will remain {direction}")
            price = position_details[2]

        else:
            print(f"We are closing our {direction} position")
            # Keep size as a string for creating orders, even tho we use it for math
            size = position_details[1]
            open_price = float(position_details[2])
            close_price = float(bybit.get_price())
            percent_chg = (close_price - open_price) / open_price * 100
            dollar_diff = close_price * float(size) - open_price * float(size)
            lpnl = f"${dollar_diff:,.2f} ({round(percent_chg, 2)}%)"
            # TODO - Replace with market order with symbol, etc determined
            # TODO - remember to remove postOnl;y eventually too
            # TODO - send two orders to flip or double size... think about best way
            bybit.create_order("linear", "BTCUSDT", decision, "Limit", size, "72000")
            bybit.cancel_all() 

            # Changinge dir to nothing here instead of flipping pos, again think what you wanna do
            account_size += dollar_diff
            direction = "-"
            price = "-"

    else:
        print(f"Not in any position, Entering a {direction}")

        # TODO - Replace with market orders with symbol and size determined
        bybit.create_order("linear", "BTCUSDT", decision, "Limit", "0.05", "72000")
        # TODO - Remove this once testing is done
        bybit.cancel_all()
        price = position_details[2]
        
    # Calcs for total pnl for account
    dpnl = account_size - float(starting_bal)
    ppnl = dpnl / float(starting_bal) * 100
    tpnl = f"${dpnl:,.2f} ({round(ppnl, 2)}%)"

    # Look at me go, trying as hard as possible to bug out cuz im lazy
    # TODO - FIX THIS IDIOT! it works for 1 char timeframes but if i add more later
    # it will be a big bug I either wont find or think of! FIX IT on the first run
    # of otimizing!!!
    strat = read_log_file()[0][0]

    log = (f"Current Strategy: {strat}\nCurrent Position: {direction}\n"
           f"Open_price: {price}\nAccount Balance: {account_size}\n"
           f"Last trade PNL: {lpnl}\nTotal PNL: {tpnl}\nStarting Bal: {starting_bal}\n")
   
    write_log_file(log)
    print(log)

def create_env() -> None:
    # TODO - Add more insrtuction like website to get account, to api, etc
    # TODO - change this from true to be more specific, fine for now while dev
    while(True):
        with open(".env", "w") as file:
            api_key: str = input("Please enter your api key:\n")
            api_secret: str = input("Please enter you api secret:\n")

            print(f"{'-'*55}\nCREATING AUTHENTICATION LINK\n{'-'*55}")

            str_to_write: str = f"API_KEY={api_key}\nAPI_SECRET={api_secret}"
            file.writelines(str_to_write)
        
        load_dotenv(override = True)

        api_key = os.getenv("API_KEY") #
        api_secret = os.getenv("API_SECRET") #
        
        try:
            # We have to pass in the user provided variables as the env 
            e = Exchange(api_key, api_secret, True)
            e.get_position()
            break
            # TODO - Handle error correctly, big black hole for a user here
        except Exception: 
            print("Error with api key/secret, try again and check internet connection")


def write_log_file(log: str = "") -> None:
    if log == "":
        log = "Current Strategy: Default\nCurrent Position: None\nOpen_price: None\n \
        Account Balance: None\nLast trade PNL: None\nTotal PNL: None\nStarting Bal: None"

    with open("user_log.txt", "w") as file:
        file.writelines(log)

        
def read_log_file():

    log_vars = []

    with open("user_log.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            log_vars.append(line.split(":")[1].strip(" ").strip("\n"))
        log_vars.append(lines)
    return log_vars


def next_action():
    while True:


        user = input("What do you wanna do?\nPress c to Change strategy\n"
                         "Press e to exit\n\n>> ")
        if user == "c":
            os.system('cls||clear')
            strat = get_risk()
            # This doesnt work but im tired, fix tomorrow
            current_log = f"Current Strategy: {strat}{read_log_file()[7]}"
            write_log_file(current_log)
            break
        elif user == "e":
            # TODO - better bye message bro, something like check in later or something
            print("see ya later")
            exit(0)
        else:
            print("Command unknown, please make sure you are entering a valid command")

def main():

    print("\nWelcome to self managing your retirement fund \n" + 
        "(this is a literal casino)\n")

    sim = get_choice()

    if sim:
        risk = get_risk()
        run_simulation(build_strategy(risk))
    else:

        if not os.path.exists("./.env"):
            # Create env file 
            create_env()

            # create log file indent back under not os.path when finished testing
        write_log_file()
        os.system('cls||clear')

        while True:
            # This is some sneaky bug bound shit im trying to pull off, read the
            # first char from the first item in the list returned by the log reader...
            # I could not think up less dynamic and modular code, great work me.
            risk = "D" if read_log_file()[0][0] == "D" else "1"

            
            # reads risk from log file, default to low or "D"
            nn, data = build_strategy(risk)

            latest_value = data.get_latest_values()
            decision = nn.predict(latest_value)

            take_action(decision)

            next_action()


if __name__ == "__main__":
    main()
