# TODO - Rebuild main
# TODO - Strategy builds diff netwrok using testing class to create a strat
# TODO - strategy returns risk amount for size calc
# TODO - SO MUCH DOCUMENTATION MISSING

import os
from dotenv import load_dotenv
from simulation import run_simulation
from strategy import build_strategy 
from exchange import Exchange
import logger


def get_choice(input_map) -> str | None:
    
    """
    Takes a map containing a question to ask the user and answers to return 
    """
    while True:
        user = input(input_map["question"])
        for key in input_map["answers"].keys():
            if user == key:
                os.system('cls||clear')
                return input_map["answers"][user]
            else:
                print("Please check that you have input a valid option\n")
                

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
    return f"${float(num):,.2f}"


def trade_math(open: float, close: float):
    difference = close  - open
    percent_difference = difference / open * 100

    return difference, percent_difference


def take_action(decision, exchange) -> None:
    """

    """
    bybit = exchange
    
    # Translate the nn decision to a market action
    decision = "Buy" if decision > 0.5 else "Sell"
    
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
            entry_price = f"${float(position_details[2]):,.2f}"

        else:
            # print(f"We are closing our {direction} position")
            print("Market has flipped! Closing the current trade")
            direction, entry_price, account_size, lpnl = exit_trade(exchange, account_size, decision)
            print("TODO THE NEW POSITION WE ARE IN")
    else:
        print(f"Not in any position, Entering a {direction}\n")
        entry_price = enter_trade(bybit, decision, account_size)
        
    # Calcs for total pnl for account
    dpnl, ppnl = trade_math(starting_bal, account_size)
    tpnl = f"${dpnl:,.2f} ({round(ppnl, 2)}%)"

    # TODO - FIX THIS! it works for 1 char timeframes but if i add more later
    # it will be a big bug I either wont find or think of! FIX IT on the first run
    # of optimizing!!!
    strat = logger.read_log_file()[0]
   
    logger.write_log_file(strat, direction, entry_price, f"${float(account_size):,.2f}", 
                          lpnl, tpnl, f"${float(starting_bal):,.2f}")
    logger.print_log()
    

# TODO - Thin this function out.
def exit_trade(exchange, account_size, nn_decision):
    side, size, open_price, _ = exchange.get_position()
    print(side, size, open_price, nn_decision)
    open_price = str_to_float(open_price)
    print(open_price)
    # will use trade4 math function for this shortly
    close_price = float(exchange.get_price())
    percent_chg = (close_price - open_price) / open_price * 100
    dollar_diff =  close_price * float(size) - open_price * float(size)
    lpnl = f"${dollar_diff:,.2f} ({round(percent_chg, 2)}%)"
    
    exchange.market_order("linear", "BTCUSDT", nn_decision, "Market", size)

    account_size += dollar_diff
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
    while True:
        try:
            # We have to pass in the user provided variables as the env 
            e = Exchange(os.getenv("API_KEY"), os.getenv("API_SECRET"), True)
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
                
                # TODO - Storing api keys as unprotected strings in a txt file i see... very good.
                # we should just roll our own encryption to protect them while we are at it.
                str_to_write: str = f"API_KEY={api_key}\nAPI_SECRET={api_secret}"
                file.writelines(str_to_write)
            
            load_dotenv(override = True)


def change_strategy():
    logger.update_strategy_log(get_choice(risk_map))


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
            latest_value = data.get_latest_values()
            decision = nn.predict(latest_value)

            # Runs the decision process and logs the output
            take_action(decision, exchange)

            # Asks user whats next
            get_choice(command_map)()


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
        "Press e to exit\n\n" + ">> ",
                   "answers": {"c": change_strategy, 
                               "e": exit_program}}

    main()
    
