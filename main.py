# TODO - Rigorously check for no internet, no account bal, etc. type of bugs
# TODO - SO MUCH DOCUMENTATION MISSING

import os
import time
import logger
import threading
from dotenv import load_dotenv
from simulation import run_simulation
from strategy import build_strategy, risk_amount 
from exchange import Exchange


def get_choice(input_map, is_command = False):
    
    """
    Takes a map containing a question to ask the user and answers to return 
    """
    while True:
        user = input(input_map["question"])
        for key in input_map["answers"].keys():
            if user == key:
                os.system('cls||clear')
                val = input_map["answers"][user]
                return val() if is_command else val
            else:
                print("Please check that you have input a valid option\n")
                os.system('cls||clear')
                

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
    Formats a number string adding leading $ sign and two decimals

    Params:
    num
    """
    return f"${float(num):,.2f}"


def trade_math(open: float, close: float):
    """
    Calculates the int and percent difference between two numbers
    """
    # Sometimes bybit will return o values when it should, due to server overload
    # working on bigger fix, for now, we just catch ZeroDivisionError and retrun 0
    try:
        difference = close - open
        percent_difference = difference / open * 100
    except ZeroDivisionError:
        return 0.0 , 0.0
    return difference, percent_difference


def take_action(decision, exchange) -> None:
    """
    What doesn't this function do.... and that's a problem
    """
    bybit = exchange
    
    # Translate the nn decision to a market action & command
    decision = "Buy" if decision > 0.5 else "Sell"
    direction = "Long" if decision == "Buy" else "Short"

    # Finds out if we are in a position or not. 
    side, size, entry_price, _ = bybit.get_position(symbol="BTCUSDT") 

    # Check for zero balance / get the accounts current balance
    account_bal = get_account_balance(exchange)

    # Control for starting bal to be initiated and never changed
    if logger.read_log_file()[7] == "None":
        starting_bal = account_bal
    else:
        starting_bal = str_to_float(logger.read_log_file()[7])
     
    # The last trades profit and loss
    cpnl = "-"
    lpnl = logger.read_log_file()[4]
    # print(f"Current position: {side}, Current decision: {decision}") 
    if side != "":
        if side == decision:
            print(f"We are in a {direction} and will remain {direction}")
            cpnl = float_to_str(get_current_pnl(exchange))
            entry_price = float_to_str(entry_price) 

        else:
            print(f"We are closing our {logger.read_log_file()[1]} position")
            direction, entry_price, account_bal, lpnl = exit_trade(exchange, decision)
            
    else:
        print(f"Not in any position, Entering a {direction}\n")
        entry_price = enter_trade(bybit, decision)
        
    # Calcs for total pnl for account
    dpnl, ppnl = trade_math(starting_bal, account_bal)
    tpnl = f"${dpnl:,.2f} ({round(ppnl, 2)}%)"

    # Write and print the upodated information to the log file and stdoput
    logger.write_log_file(logger.read_log_file()[0], direction, entry_price, cpnl,
            lpnl, tpnl, float_to_str(account_bal), float_to_str(starting_bal))
    logger.print_log()

    
def get_account_balance(exchange):
    account_bal = exchange.get_balance()
    if account_bal != "0":
        return str_to_float(account_bal)
    else:
        print("\nYour account does not have sufficent funds to place a trade.\n")
        exit(0)

    
# uncomrfotable with how this is written
def get_current_pnl(exchange):
    """
    Calculates the difference between two values... similiar to trade_math..?
    """
    _, size, entry, _ = exchange.get_position()
    current, size, entry = float(exchange.get_price()), float(size), float(entry)

    return current * size - entry * size

def get_position(exchange):
    in_position = exchange.get_position()[0]
    if in_position == "":
        return False
    else:
        print("\nBybit is currently experiencing heavy load\n"+
            "Unable to fully close your position\n"+
            "try to execute your command again\n")
        return True


# TODO - Thin this function out. If forced close is on, decision = None by default
def exit_trade(exchange, decision = None, forced = False):
    """
    Closes an open position and enters a new trade in the opposite direction
    """
    # Querying exchange for information on the current trade
    side, size, open_price, _ = exchange.get_position()
    
    # If we are forcing a trade closed, then take the opposite position in the market
    # override the NNs decision and reassign decision to exit 
    if forced and side != "":
        side = "Buy" if side == "Sell" else "Sell"
        decision = side

    # Converting price and size to floats for some math on pnl
    open_price, float_size = str_to_float(open_price), str_to_float(size)

    # Calculating entry and exit values
    close, open = float(exchange.get_price()) * float_size, open_price * float_size
    dollar_difference, percent_difference =  trade_math(open, close)

    # String containing dollar and precent pnl info for the log
    lpnl = f"${dollar_difference:,.2f} ({round(percent_difference, 2)}%)"
    
    # Close position
    exchange.market_order("linear", "BTCUSDT", decision, "Market", size)

    account_bal = get_account_balance(exchange) + dollar_difference
   
    # Deals with mostly bybit overload problems and protection against user trying to 
    # force close a trade that doesnt exist
    if get_position(exchange):
        direction = "Long" if side == "Buy" else "Short"
        return direction, open_price, account_bal, lpnl
    else: 
        # Add the dollar amount difference to the... wait do i need to do this. 
        direction = "Long" if decision == "Buy" else "Short"
        entry_price = "None" if forced else enter_trade(exchange, decision)
        if not forced:
            print(f"Opening a {direction}")
        else:
            print("\nYou are current not in any trade\n")
    
        return direction, entry_price, account_bal, lpnl


# I can remove risk_percent as a param and account_size
def enter_trade(exchange, decision):
    risk_percent = risk_amount(logger.read_log_file()[0][0])
    account_size = get_account_balance(exchange)

    # TODO - Turn this into a function, maybe, if i do it again somewhere else
    size = str(round(max(account_size * risk_percent / float(exchange.get_price()), 
                         0.001), 3))
    exchange.market_order("linear", "BTCUSDT", decision, "Market", size)
    
    # Return the entry price of the new trade
    return float_to_str(exchange.get_position()[2])
    

def validate_env_2_boogaloo():
    """
    You should have seen validate_env_1.... this information doesnt help the users
    """
    while True:
        try:
            # Test that we can connect to the exchange before doing anything else
            Exchange(testnet=True).test_connection()

            # We have to pass in the user provided variables as the env 
            # Testnet is hard set to true here for une ai competition
            e = Exchange(os.getenv("API_KEY"), os.getenv("API_SECRET"), True)

            # Defining this here instead of earlier because the exchange 
            # object didn't exist prior, better design would fix this 
            command_map["answers"]["a"] = lambda: automate(e) # A sneaky lambda
            command_map["answers"]["r"] = lambda: refresh_trade(e) 

            # Currently turning off till i can solve the bybit execution problem
            # i.e they don't let your trade through if there isnt enough liquiidty
            command_map["answers"]["f"] = lambda: exit_trade(e, forced=True) 

            e.get_position()
            return e

            # TODO - Handle error correctly, big black hole for a user here
        except Exception: 
            if os.path.exists("./.env"):
                print("Error reading the api key and secret\n")

            with open(".env", "w") as file:
                api_key: str = input("Please enter your api key:\n")
                api_secret: str = input("Please enter you api secret:\n")

                print(f"{'-'*55}\nCREATING AUTHENTICATION LINK\n{'-'*55}")
                
                # TODO - Storing api keys as unprotected strings in a txt file i 
                # see... very good. we should just roll our own encryption to 
                # protect them while we are at it.
                str_to_write: str = f"API_KEY={api_key}\nAPI_SECRET={api_secret}"
                file.writelines(str_to_write)
            
            load_dotenv(override = True)
            os.system('cls||clear')


def change_strategy():
    """
    Updates the log file with the newly selected strategy
    """
    logger.update_strategy_log(get_choice(risk_map))
    return "change"
    

    
def exit_automation(exit_event):
    """
    Listens for user input to specifically exit automation mode, check 'automate'
    """
    while True:
        user = input()
        if user.lower() == '':
            exit_event.set()
            # os.system('cls||clear')
            
            print(f"\n{'-'*55}\nLeaving Automation mode...\n{'-'*55}\n")
            break


# TODO - Would rather have some kind of observer pattern watching the market updating
# instead of using sleep, or maybe some kind of thread, but ducktape and bandaids for now.
def automate(exchange):
    strat_map = {"1": 60, "5": 300, "15": 900, "H": 3600, "4": 14400, "D": 86400}

    # Set up our thread to cancel automation mode
    exit_event = threading.Event()
    key_thread = threading.Thread(target = exit_automation, args = (exit_event, ))
    key_thread.daemon = True
    key_thread.start()

    while True:
        # TODO - just call logger and get strategy to pass to the risk map slicing 
        # the first char to automate the time this shortcut for now is fine though
        risk = update_trade(exchange)

        # ChHANGE THIS BACK WHEN TESTING IS OVER
        time_remaining = strat_map[risk[0]]
        
        print("\nTo exit automation mode hit the 'ENTER' key\n")
        while time_remaining > 0:
            if exit_event.is_set():

                return
            
            if risk == "D":
                print("Warning: Daily strategy is enabled. Change strategy to high"+
                " risk to see the program execute trades automatically every 60 seconds.\n")

            print(f" Time before next decsision: {time_remaining:05d}", end="\r")
            time_remaining -= 1
            time.sleep(1)
        os.system("cls||clear")
    

def exit_program():
    print("Check in later to see how the market is doing, see ya")
    exit(0)


def update_trade(exchange):
    
    risk = logger.read_log_file()[0] 

    # reads risk from log file, default to low or "D"
    nn, data = build_strategy(risk)

    # Make a prediction on the latest data
    decision = nn.predict(data.get_latest_values())
             
    # Runs the decision process and logs the output
    take_action(decision, exchange)
    # This is lazy and shortcutty
    return risk


def refresh_trade(exchange):
    # Recreates the NNs decision (which needs to be a float) by reading the log file
    # main is turning into a disater, a slow carcrash that i have the power to stop!
    decision = 0.51 if logger.read_log_file()[1] == "Long" else 0.49
    take_action(decision, exchange)


def main():

    print("\nWelcome to self managing your retirement fund \n" + 
        "(This is a literal casino)\n")

    sim = get_choice(task_map)

    if sim:
        risk = get_choice(risk_map) 
        run_simulation(build_strategy(risk))
    else:

        exchange = validate_env_2_boogaloo()
        update_trade(exchange) 

        while True:
            choice = get_choice(command_map, True)
            
            if choice == "change":
                update_trade(exchange)


if __name__ == "__main__":
    load_dotenv()
    # Creating the log file before anything else to avoid critial destruction
    # .... also it probably shouldn't be a txt file....
    if not os.path.exists("./user_log.txt"):
        logger.write_log_file()

    task_map = {"question" : "Please select a task: \n" +
        "Press 's' to run a simulation on the market \n" + 
        "Press 'r' to run a real trade in the market \n\n" + ">> ",
                "answers": {"s": True, "r": False}}

    risk_map = {"question": "\nEnter the risk strategy you would like to take:\n" +
        "Press 'h' for high risk\n" + 
        "Press 'l' for low risk\n\n" + ">> ", 
                "answers": {"h": "1 - High risk", "l": "D - Low risk"}}


    command_map = {"question": "What would you like to do?\n" + 
        "Press r to Refresh Current or Enter a trade\n" + 
        "Press c to Change strategy\n" + 
        "Press a to Automate trading\n" + 
        "Press f to Force close the current trade\n" + 
        "Press e to Exit\n\n" + ">> ",
                   "answers": {"c": change_strategy, 
                               "e": exit_program}}

    main()

