# TODO - implement size if test acct is used.
# TODO - Look at strategy for more control over trades and conditions
# TODO - SO MUCH DOCUMENTATION MISSING
# TODO - implement a testing class for easier tuning of the nn
# TODO - Go through each file and look at the todos.
# TODO - Replace all limit orders with market orders 
# TODO - Add more features to train on

import os
from dotenv import load_dotenv
from simulation import run_simulation
from strategy import build_strategy 
from exchange import Exchange
import logger


# TODO - get_choice and get_risk are the same func, fold them into one.
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
            risk = "1 - High Risk"
        elif user.lower() == "l":
            risk = "D - Low Risk"
        else:
            print("Please check you input a valid option\n")
    os.system('cls||clear')
    return risk


# TODO - feel free to collapse these two functions into one converter conditional
def str_to_float(num: str) -> float:
    """
    Converts a str in "$x,xxx.xx" format to a float

    Params:
    num - a number represented as a string e.g "$xx,xxx.xx"
    """
    return float(num.replace("," ,"").strip("$").strip())


def float_to_str(num: float) -> str:
    """
    Converts a float to a string adding leading $ sign and two decimals

    Params:
    num
    """
    return f"${num:,.2f}"



def take_action(decision) -> None:
    """
    Depending on the ai's decision and the current position in the market, an 
    action will be taken to either enter a position, maintain a position or 
    close a position.

    Params:
    position - The current direction we are in the market
    decision - The Neural networks decision on where to do next
    """
    # TODO This whole logic may work at the moment but is extremely bug prone due 
    # to alot of assumptions im making because we currently have complete control 
    # over the test account we are using for this program, fix this to be more 
    # safe to use for the future

    # Create an instance of our exchange
    key = os.getenv("API_KEY")
    secret = os.getenv("API_SECRET")
    bybit = Exchange(key, secret, testnet= True)

    # Translate the nn decision to a market action
    decision = "Buy" if decision == 1 else "Sell"
    
    # Used for prettification of strings... and english... really
    direction = "Long" if decision == "Buy" else "Short"

    # Finds out if we are in a position or not. 
    position_details = bybit.get_position(symbol="BTCUSDT") 
    position = position_details[0]

    # TODO -Rewrite this more eloquently you rusher!!!!!
    account_size = bybit.get_balance()
    if account_size != "":
        account_size = str_to_float(account_size)
    else:
        print("There is no balance in the supplied account")
        exit(0)

    if logger.read_log_file()[6] == "None":
        starting_bal = account_size
    else:
        starting_bal = str_to_float(logger.read_log_file()[6])
     
    # The last trades profit and loss
    lpnl = logger.read_log_file()[4]

    if position != "":
        if position == decision:
            print(f"We are in a {direction} and will remain {direction}")
            price = f"${float(position_details[2]):,.2f}"

        else:
            print(f"We are closing our {direction} position")
            # Keep size as a string for creating orders, even tho we use it for math
            size = position_details[1]
            open_price = str_to_float(position_details[2]) 
            close_price = float(bybit.get_price())
            percent_chg = (close_price - open_price) / open_price * 100
            dollar_diff = close_price * float(size) - open_price * float(size)
            lpnl = f"${dollar_diff:,.2f} ({round(percent_chg, 2)}%)"

            # bybit.create_limit_order("linear", "BTCUSDT", decision, "Limit", size, "72000")
            # bybit.cancel_all() 
            # Uncomment when ready for final testing
            bybit.create_market_order("linear", "BTCUSDT", decision, "Market", size)

            # Changinge dir to nothing here instead of flipping pos, again think what you wanna do
            account_size += dollar_diff
            direction = "-"
            price = "-"

    else:
        print(f"Not in any position, Entering a {direction}\n")

        # TODO - write separate function that calcs size using risk and acct 
        risk_percent = 0.05     # This should be controlled by strategy module.
        size = str(round(max(account_size * risk_percent / float(bybit.get_price()), 0.001), 3))
        # bybit.create_limit_order("linear", "BTCUSDT", decision, "Limit", size, "72000")
        # TODO - Remove this once testing is done
        # bybit.cancel_all()

        bybit.create_market_order("linear", "BTCUSDT", decision, "Market", size)
        # This is needed when building out the program as we arnt sending orders yet
        # So return vals arnt what they should be yet
        price = position_details[2]
        price = f"${float(price):,.2f}" if price != '' else '-'
        
    # Calcs for total pnl for account
    dpnl = account_size - starting_bal
    ppnl = dpnl / starting_bal * 100
    tpnl = f"${dpnl:,.2f} ({round(ppnl, 2)}%)"

    # TODO - FIX THIS! it works for 1 char timeframes but if i add more later
    # it will be a big bug I either wont find or think of! FIX IT on the first run
    # of optimizing!!!
    strat = logger.read_log_file()[0]
   
    logger.write_log_file(strat, direction, price, f"${float(account_size):,.2f}", 
                          lpnl, tpnl, f"${float(starting_bal):,.2f}")
    logger.print_log()


def create_env() -> None:
    # TODO - Add more insrtuction like website to get account, to api, etc
    # TODO - change this from true to be more specific, fine for now while dev
    while True:
        with open(".env", "w") as file:
            api_key: str = input("Please enter your api key:\n")
            api_secret: str = input("Please enter you api secret:\n")

            print(f"{'-'*55}\nCREATING AUTHENTICATION LINK\n{'-'*55}")
            
            # TODO - Storing api keys as unprotected strings in a txt file i see... very good.
            # we should just roll our own encryption to protect them while we are at it.
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
            print("Error with api key/secret, try again and check internet connection\n")


# TODO - Pretty much just duplicating the func above but when an env file exists, 
# better solution to this exist, come back to fix this 
def validate_env():
    while True:
        try:
            # We have to pass in the user provided variables as the env 
            e = Exchange(os.getenv("API_KEY"), os.getenv("API_SECRET"), True)
            e.get_position()
            break
            # TODO - Handle error correctly, big black hole for a user here
        except Exception: 
            print("Error with api key/secret\n")
            create_env()

def next_action():

    while True:
        user = input("What would you like to do?\nPress c to Change strategy\n"
                         "Press e to exit\n\n>> ")
        if user == "c":
            #os.system('cls||clear')
            strat = get_risk()

            # ewww, bad bad bad design, figure out a way to work with the logs better
            log = logger.read_log_file()
            logger.write_log_file(strat, log[1], log[2], log[3], log[4], log[5], log[6])
            break
        elif user == "e":
            # TODO - better bye message bro, something like check in later or something
            print("see ya later")
            exit(0)
        else:
            print("Command unknown, please make sure you are entering a valid command")


def main():

    print("\nWelcome to self managing your retirement fund \n" + 
        "(This is a literal casino)\n")

    sim = get_choice()

    if sim:
        risk = get_risk()
        run_simulation(build_strategy(risk))
    else:

        # Check for a valid .env file with valid api key and secret
        if not os.path.exists("./.env"):
            # Create env file 
            create_env()
        else:
            validate_env()

        os.system('cls||clear')

        while True:
            risk = logger.read_log_file()[0] 

            # reads risk from log file, default to low or "D"
            nn, data = build_strategy(risk)

            # Make a prediction on the latest data
            latest_value = data.get_latest_values()
            decision = nn.predict(latest_value)

            # Runs the decision process and logs the output
            take_action(decision)

            # Asks user whats next
            next_action()


if __name__ == "__main__":
    load_dotenv()
    # Creating the log file before anything else to avoid critial destruction
    # .... also it probably shouldn't be a txt file....
    if not os.path.exists("./user_log.txt"):
        logger.write_log_file()

    main()
