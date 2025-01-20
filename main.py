# TODO - Look through all modules todo lists, add types and documentation 
# TODO - log files and database files should probably be hidden dot files... dunno
import os
import time
import logger
import threading
from dotenv import load_dotenv
from simulation import run_simulation
from strategy import build_strategy, risk_amount, sim_strategy 
from exchange import Exchange


def str_to_float(num: str) -> float:
    """
    Converts a str in "$x,xxx.xx" format to a float
    """
    return round(float(num.replace("," ,"").strip("$").strip()), 2)


def float_to_str(num: float) -> str:
    """
    Formats a number string adding leading $ sign and two decimals
    """
    return f"${float(num):,.2f}"


def in_position(inverse: bool = False):
    """
    Checks to see if a position is open or not, useful to run after sending a trade
    """
    position: bool = False if get_current_position()[0] == "" else True
    # print this statement after making a trade to check for success or failure
    if position != inverse:
        print("\nBybit is currently experiencing heavy load\n"+"Unable to fully "+
            "execute your trade\nTry to run your command again\n")
        return False 
    else:
        print(f"\nTrade successfully executed\n{'-'*45}")
        return True 


def calc_pnl(open, close) -> str:
    """
    calculates the int difference and percent difference between two values
    """
    dpnl: float = str_to_float(close) - str_to_float(open)
    ppnl: float = dpnl / max(str_to_float(open), 1) * 100 # the max is used for divby0 error, FIX
    return f"{float_to_str(dpnl)} ({round(ppnl, 2)}%)"


def get_current_pnl():
    """
    Calculates the difference between two values... similiar to trade_math..?
    """
    side, size, entry, _ = exchange.get_position()
    if side != "":
        current, size, entry = float(exchange.get_price()), float(size), float(entry)
        return float_to_str(current * size - entry * size)
    else:
        return "-"


def get_account_balance():
    """
    Returns the users current account balance as a float
    """
    account_bal: str = exchange.get_balance()
    if account_bal != "0":
        return str_to_float(account_bal)
    else:
        print("\nYour account does not have sufficent funds to place a trade.\n"+
              "Visit testnet.bybit.com to add funds to your account & try again")
        exit(0)


def get_current_position() -> tuple:
    """
    Returns the side, size, entry price and retMsg from exchange as strings
    """
    return exchange.get_position() 


def calc_trade_size() -> str:
    """
    Calculates the size for a trade depending on the risk strategy & account balance
    """
    percent: float = risk_amount(logger.read_log_file()[0])
    return str(round(max(percent * get_account_balance() / float(exchange.get_price()), 0.001), 3))  # May change get price into a func


def log_trade():
    """
    Writes all current account and trade details to the log
    """
    side, size, entry_price, _ = get_current_position()
       
    a_bal = float_to_str(get_account_balance()) 
    s_bal = logger.read_log_file()[7] if logger.read_log_file()[7] != "None" else a_bal
    # strings needed for last trade calculations
    entry, trade_exit, size = exchange.get_last_pnl()
    lpnl = calc_pnl(str(entry * size), str(trade_exit * size)) if entry != 0 else "-"
    # logging strat,side,entry price,current pnl,last pnl,total pnl,acct bal & start bal)
    logger.write_log_file(logger.read_log_file()[0], side, float_to_str(entry_price), 
                          get_current_pnl(), lpnl, calc_pnl(s_bal, a_bal), a_bal, s_bal)

    logger.print_log()
    

def execute_trade_logic(decision) -> None:
    side, size, _, _= get_current_position()

    # Works through the logic if what the NN wants to do and what position the user is in 
    if side != "":
        if side == decision:
            print(f"We are {position_map[side]} and we will remain {position_map[side]}")  # Do nothing
        else:
            print(f"We are closing our {position_map[side]}")
            exchange.market_order(decision, size) # close trade
            if in_position():
                print(f"Now opening a {position_map[decision]}")
                exchange.market_order(decision, calc_trade_size()) # Open new one
                in_position(True)
    else:
        # If no position is currently open, open one!
        print(f"We are not in a position, we will {position_map[decision]}")
        exchange.market_order(decision, calc_trade_size(), "linear", "BTCUSDT")
        in_position(True)

    log_trade()


def refresh_trade() -> None:
    """
    Refresh the user view of the current trade they are in 
    """
    if get_current_position()[0] == "":
        print("You are currently not in any trade\nUse change strategy to enter a new trade\n")
        return 
    execute_trade_logic(get_current_position()[0])


def update_trade() -> None:
    """
    Uses the currently defined risk to retrieve the NNs next market decision 
    """
    # Reads current risk from log file and returns the nn's decision
    decision:str = build_strategy(logger.read_log_file()[0])
    # Passes the decision into the main logic conditional
    execute_trade_logic(decision)


def force_close() -> None:
    """
    Automatically closes a users position no matter what the nn thinks to do
    """
    side, size, _, _= get_current_position()
    if side != "":
        print(f"Attempting to close our {position_map[side]}")
        side: str = "Sell" if side == "Buy" else "Buy"
        exchange.market_order(side, size)
        in_position()
    else:
        print("You are currently not in a position\n")


def change_strategy() -> str:
    """
    Updates the log file with the newly selected strategy
    """
    logger.update_strategy_log(get_choice(risk_map))
    return "change"
    

def exit_automation(exit_event) -> None:
    """
    Listens for user input to specifically exit automation mode, check 'automate'
    """
    while True:
        user: str = input()
        if user.lower() == '':
            exit_event.set()
            print(f"\n{'-'*45}\nLeaving Automation mode...\n{'-'*45}\n")
            break


def automate() -> None:
    """
    Automates the selected trading strategy until user intervention
    """
    strat_map = {"1": 60, "5": 300, "15": 900, "H": 3600, "4": 14400, "D": 86400}

    # Set up our thread to cancel automation mode
    exit_event = threading.Event()
    key_thread = threading.Thread(target = exit_automation, args = (exit_event, ))
    key_thread.daemon = True
    key_thread.start()

    while True:
        risk: str = logger.read_log_file()[0] # return is e.g "D - low risk"
        update_trade()
        # Gets the right amount of time to sleep according to the current strat
        time_remaining: int = strat_map[risk[0]] # Danger with the slicing here
        print("\nTo exit automation mode hit the 'ENTER' key\n")
        while time_remaining > 0:
            if exit_event.is_set():
                return
            
            if risk == "D":
                print("UNE JUDGES - Switch to high risk to see quick decisions execute\n")

            print(f" Time before next decsision: {time_remaining:05d}", end="\r")
            time_remaining -= 1
            time.sleep(1)
        os.system("cls||clear")
 

def run_sim() -> None:
    """
    runs a simulation on the market 
    """
    risk = get_choice(risk_map) 
    run_simulation(sim_strategy(risk))


def exit_program() -> None:
    """
    Safely exits the program 
    """
    print("Check in later to see how the market is doing, see ya")
    exit(0)


def get_choice(input_map, is_command = False):
    """
    Takes a map containing a question to ask the user and answers to return 
    """
    while True:
        user: str = input(input_map["question"])
        for key in input_map["answers"].keys():
            if user == key:
                os.system('cls||clear')
                val = input_map["answers"][user]
                return val() if is_command else val


def validate_env() -> None:
    """
    Authenticates connection to exchange or aks user to enter api information 
    if none currently exists
    """
    while True:
        try:
            # Test that we can connect to the exchange before doing anything else
            Exchange(testnet=True).test_connection()
            # Once we know we can connect to the exchange, auth our connection 
            exchange.authenticate_connection(os.getenv("API_KEY"), os.getenv("API_SECRET"))
            # If request goes through then api and secret worked, return to main
            exchange.get_position()
            return 
        # TODO - Handle error correctly, big black hole for a user here
        except Exception: 
            if os.path.exists("./.env"):
                print("Error reading the api key and secret, please re-enter.\n")

            with open(".env", "w") as file:
                api_key: str = input("Please enter your api key:\n")
                api_secret: str = input("Please enter your api secret:\n")

                print(f"{'-'*55}\nCREATING AUTHENTICATION LINK\n{'-'*55}")
                # TODO - protec the keys!! nice plain text storage.
                str_to_write: str = f"API_KEY={api_key}\nAPI_SECRET={api_secret}"
                file.writelines(str_to_write)
            load_dotenv(override = True)
            os.system('cls||clear')


def main() -> None:
    print("\nWelcome to self managing your retirement fund \n" + 
        "(This is currently a literal casino)\n")

    validate_env()
    while True:
        choice = get_choice(command_map, True)
            
        if choice == "change":
            update_trade()


if __name__ == "__main__":
    # Load the environment variables
    load_dotenv()
    # Create an instance of the exchange 
    exchange: Exchange = Exchange(testnet = True)
    # Create a user log file if one does not exist
    if not os.path.exists("./user_log.txt"):
        logger.write_log_file()
    
    risk_map: dict = {"question": "\nEnter the risk strategy you would like to take:\n" +
        "Press 'h' for high risk (Minute by Minute decisions)\n" + 
        "Press 'l' for low risk (Day by Day decisions)\n\n" + ">> ", 
                "answers": {"h": "1 - High risk", "l": "D - Low risk"}}

    position_map: dict = {"Buy": "Long", "Sell": "Short", "": "-"}

    command_map: dict = {"question": "What would you like to do?\n" + 
        "Press s to Run a simulation on the market\n" + 
        "Press c to Enter trade or Change strategy\n" + 
        "Press r to Refresh current trade\n" + 
        "Press c to Change strategy\n" + 
        "Press a to Automate trading\n" + 
        "Press f to Force close the current trade\n" + 
        "Press e to Exit\n\nHit ENTER to confirm command\n\n" + ">> ",
                   "answers": {"c": change_strategy, 
                               "s": run_sim,
                               "r": refresh_trade,
                               "f": force_close,
                               "a": automate,
                               "e": exit_program}}
    main()

