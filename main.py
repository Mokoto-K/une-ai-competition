# TODO - Rebuild main
# TODO - Strategy builds diff netwrok using testing class to create a strat
# TODO - strategy returns risk amount for size calc
# TODO - SO MUCH DOCUMENTATION MISSING

# TODO - Grid search for strat class to train networks using nntrain class
# TODO - Build more features
# TODO - implement Automation 
# TODO - Implement size calc, but not for use y_test
# TODO - Rigorously check for no internet, no account bal, etc. type of bugs

import os
import time
from dotenv import load_dotenv
from simulation import run_simulation
from strategy import build_strategy 
from exchange import Exchange
import logger
import threading


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
    difference = close - open
    percent_difference = difference / open * 100

    return difference, percent_difference


def take_action(decision, exchange) -> None:
    """
    What doesn't this function do....
    """
    bybit = exchange
    
    # Translate the nn decision to a market action & command
    decision = "Buy" if decision > 0.5 else "Sell"
    direction = "Long" if decision == "Buy" else "Short"

    # Finds out if we are in a position or not. 
    side, size, entry_price, _ = bybit.get_position(symbol="BTCUSDT") 

    # Check for zero balance
    account_size = bybit.get_balance()
    if account_size != "":
        account_size = str_to_float(account_size)
    else:
        print("There is no balance in the supplied account")
        exit(0)

    # Control for starting bal to be initiated and never changed
    if logger.read_log_file()[7] == "None":
        starting_bal = account_size
    else:
        starting_bal = str_to_float(logger.read_log_file()[7])
     
    # The last trades profit and loss
    cpnl = "-"
    lpnl = logger.read_log_file()[4]
    
    if side != "":
        if side == decision:
            print(f"We are in a {direction} and will remain {direction}")
            cpnl = float_to_str(get_current_pnl(exchange))
            entry_price = float_to_str(entry_price) 

        else:
            print(f"We are closing our {logger.read_log_file()[1]} position")
            direction, entry_price, account_size, lpnl = exit_trade(exchange, account_size, decision)
            print(f"Opening a {direction}")
    else:
        print(f"Not in any position, Entering a {direction}\n")
        entry_price = enter_trade(bybit, decision, account_size)
        
    # Calcs for total pnl for account
    dpnl, ppnl = trade_math(starting_bal, account_size)
    tpnl = f"${dpnl:,.2f} ({round(ppnl, 2)}%)"

    # Write and print the upodated information to the log file and stdoput
    logger.write_log_file(logger.read_log_file()[0], direction, entry_price, cpnl,
            lpnl, tpnl, float_to_str(account_size), float_to_str(starting_bal))
    logger.print_log()


# uncomrfotable with how this is written
def get_current_pnl(exchange):
    """
    Calculates the difference between two values... similiar to trade_math..?
    """
    _, size, entry, _ = exchange.get_position()
    current, size, entry = float(exchange.get_price()), float(size), float(entry)

    return entry * size - current * size


# TODO - Thin this function out.
def exit_trade(exchange, account_size, nn_decision):
    """
    Closes an open position and enters a new trade in the opposite direction
    """
    # Querying exchange for information on the current trade
    _, size, open_price, _ = exchange.get_position()

    # Converting price and size to floats for some math on pnl
    open_price, float_size = str_to_float(open_price), str_to_float(size)

    # Calculating entry and exit values
    close, open = float(exchange.get_price()) * float_size, open_price * float_size
    dollar_difference, percent_difference =  trade_math(open, close)

    # String containing dollar and precent pnl info for the log
    lpnl = f"${dollar_difference:,.2f} ({round(percent_difference, 2)}%)"
    
    # Close position
    exchange.market_order("linear", "BTCUSDT", nn_decision, "Market", size)

    account_size += dollar_difference
    entry_price = enter_trade(exchange, nn_decision, account_size)
    direction = "Long" if nn_decision == "Buy" else "Short"

    return direction, entry_price, account_size, lpnl


def enter_trade(exchange, decision, account_size):
    # TODO - write separate function that calcs size using risk and acct 
    risk_percent = 0.05     # This should be controlled by strategy module.
    size = str(round(max(account_size * risk_percent / float(exchange.get_price()), 0.001), 3))

    exchange.market_order("linear", "BTCUSDT", decision, "Market", size)

    return float_to_str(exchange.get_position()[2])
    

def validate_env_2_boogaloo():
    """
    """
    while True:
        try:
            # We have to pass in the user provided variables as the env 
            # Testnet is hard set to true here for une ai competition
            e = Exchange(os.getenv("API_KEY"), os.getenv("API_SECRET"), True)
            # the sneakiest lambda you'll ever see. We have to do this here as 
            # we want to pass the exchange object to automate and can't do it 
            # when we defined our command map. alt could just create new exchange?
            command_map["answers"]["a"] = lambda: automate(e)
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


def change_strategy():
    logger.update_strategy_log(get_choice(risk_map))

    
def exit_automation(exit_event):
    while True:
        user = input()
        if user.lower() == '':
            exit_event.set()
            print("\nLeaving Automation mode...")
            break

# TODO - Would rather have some kind of observer pattern watching the market updating
# instead of using sleep, but ducktape and bandaids for now.
def automate(exchange):
    strat_map = {"1": 60, "5": 300, "15": 900, "H": 3600, "4": 14400, "D": 86400}

    # Set up our thread to cancel automation mode
    exit_event = threading.Event()
    key_thread = threading.Thread(target = exit_automation, args = (exit_event, ))
    key_thread.daemon = True
    key_thread.start()

    while True:
        # if exit_event.is_set():
        #     break

        risk = logger.read_log_file()[0].split(" ")[0] 
        # reads risk from log file, default to low or "D"
        nn, data = build_strategy(risk)
        # Make a prediction on the latest data
        decision = nn.predict(data.get_latest_values())
        # Runs the decision process and logs the output
        take_action(decision, exchange)
        
        time_remaining = 11 #strat_map[risk]
        
        start = time.time()
        print("Hit 'enter' at any point to exit automation mode")
        while time_remaining > 0:
            if exit_event.is_set():
                return       

            if time.time() - start > 1:
                time_remaining -= 1  
                start = time.time()

            print(f"Time before next decision: {time_remaining} seconds", end="\r")
            time.sleep(0.1)
            
            # print("\033[A       \033[A")
        os.system("cls||clear")
    

def exit_program():
    print("Check in later to see how the market is doing, see ya")
    exit(0)


def main():

    print("\nWelcome to self managing your retirement fund \n" + 
        "(This is a literal casino)\n")

    sim = get_choice(task_map)

    if sim:
        risk = get_choice(risk_map) 
        run_simulation(build_strategy(risk))
    else:

        exchange = validate_env_2_boogaloo()

        os.system('cls||clear')

        while True:
            risk = logger.read_log_file()[0] 

            # reads risk from log file, default to low or "D"
            nn, data = build_strategy(risk)

            # Make a prediction on the latest data
            decision = nn.predict(data.get_latest_values())
             
            # Runs the decision process and logs the output
            take_action(decision, exchange)

            # Asks user whats next
            get_choice(command_map, True)


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
        "Press c to Change strategy\n" + 
        "Press a to Automate trading\n" + 
        "Press e to exit\n\n" + ">> ",
                   "answers": {"c": change_strategy, 
                               "e": exit_program}}

    main()
    
