# TODO - Fix up simulation class, pass in nn and data
# TODO - Hide all of the print statements for training the neural net
# TODO - Finish of logic for decisions with real account
# TODO - Look at what a test acct does and see if it should connect to that instead of real
# TODO - implement size if test acct is used.
# TODO - Go through each file and look at the todos.



# TODO - Implement everything from the cli, add a menu to check for different
# things like the trade you are in, profit?, etc
# TODO - Hide keys, also provide example api-key implementation?
# TODO - Cli logic
# TODO - indocrinate the impure to nvim
import os
from dotenv import load_dotenv
from database import Database
from features import DataFeatures
from simulation import run_simulation
from strategy import build_strategy 
from exchange import Exchange

load_dotenv()

def get_risk() -> str:
    """
    Gets the users choice of risk they would like to implement 

    Returns:
    risk - Either 1 for high risk of D for low risk, currently only two options
           representing timeframe intervals that the nn looks over in the data
    """

    risk = None
    while risk == None:
        user = input("Enter the risk you would like to take:\n 'high' or 'low'")
        if user == "high":
            risk = "1"
        elif user == "low":
            risk = "D"
        else:
            print("Please check you input a valid option\n")

    return risk


def get_position() -> str:
    """
    Query exchange to see if there is currently a position open

    Returns:
    position - A string of the current position; "long", "short", "none"
    """
    
    # Unsure as to how the exchange will return a position to us yet, so leaving
    # this as is till i implement the exchange class and all that jazz
    position = "none"
    
    return position 


def take_action(decision) -> None:
    """
    Depending on the ai's decision and the current position in the market, an 
    action will be taken to either enter a position, maintain a position or 
    close a position.

    Params:
    position - The current direction we are in the market
    decision - The Neural networks decision on where to do next
    """

    key: str = os.getenv("API_KEY")
    secret: str = os.getenv("API_SECRET")
    bybit = Exchange(key, secret)

    # Translate the nn decision to a market action
    decision = "Buy" if decision == 1 else "Sell"

    direction = "Buy" if decision == "long" else "Sell"

    position_details = bybit.get_position(symbol="BTC-28MAR25")
    position = position_details[0]

    if position != "":
        if position == decision:
            print(f"We are in a {position} and will remain {decision}")

        else:
            print(f"We are closing our {position} position")
            size = position_details[1]
            
            # TODO - Replace with market order with symbol, etc determined
            # TODO - remember to remove postOnl;y eventually too
            bybit.create_order("linear", "BTCUSDT", decision, "Limit", size, "72000")
            bybit.cancel_all() 
    else:
        print(f"Not in any position, Entering a {decision}")

        # TODO - Replace with market orders with symbol and size determined
        bybit.create_order("linear", "BTCUSDT", decision, "Limit", "0.05", "72000")
        # TODO - Remove this once testing is done
        bybit.cancel_all()
        
def main():

    sim = True 
    risk = "D"

    if sim:
        risk = "1" # get_risk
        run_simulation(build_strategy(risk))
    else:
        nn, data = build_strategy("1")

        latest_value = data.get_latest_values()
        decision = nn.predict(latest_value)
        risk = "1"

        take_action(decision)

    # key: str = os.getenv("API_KEY")
    # secret: str = os.getenv("API_SECRET")
    # bybit = Exchange(key, secret)
    #
    # position = bybit.get_position(symbol="BTC-28MAR25")
    # print(position)
    # bybit.create_order("linear", "BTCUSDT", "Buy", "Limit", "0.05", "72000")
    # bybit.cancel_all()
    

if __name__ == "__main__":
    main()
