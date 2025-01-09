# TODO - Fix up simulation class
# TODO - Add logging for real trades, when they open, close, profit, etc
# TODO - Add scaling to features and addm more features
# TODO - Look at what a test acct does and see if it should connect to that instead of real
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

    # sim = True 
    # risk = "1"

    # print("\nWelcome to self managing your retirement fund \n" + 
    #     "(this is a literal casino)\n")
    #
    # sim = get_choice()
    # risk = get_risk()
    #
    # if sim:
    #     run_simulation(build_strategy(risk))
    # else:
    #     nn, data = build_strategy(risk)
    #
    #     latest_value = data.get_latest_values()
    #     decision = nn.predict(latest_value)
    #
    #     take_action(decision)
    #


    nn, data = build_strategy("D")
    
    print(nn.predict(data.simulation_data(10)))

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
