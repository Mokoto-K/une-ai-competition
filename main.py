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


def take_action(position, decision) -> None:
    """
    Depending on the ai's decision and the current position in the market, an 
    action will be taken to either enter a position, maintain a position or 
    close a position.

    Params:
    position - The current direction we are in the market
    decision - The Neural networks decision on where to do next
    """
    # Translate the nn decision to a market action
    decision = "long" if decision == 1 else "short"

    if position != "":
        if position == decision:
            print(f"We are in a {position} and will remain {decision}")
        else:
            print(f"We are closing our {position} position")
            # close_position() 
    else:
        print(f"Not in any position, Entering a {decision}")
        # enter_position()

        
def main():

    load_dotenv()
    # TODO - Hide all of the print statements for training the neural net
    # run_simulation()
    # print("Welcome to the casino... essentially\n")
    #
    # choice = None
    # while choice == None:
    #     inp = input("press s for the simulation or r for real account\n")
    #
    #     if inp.lower() == "s":
    #         run_simulation(get_risk())
    #     elif inp.lower() == "r":
    #         risk = get_risk()
    #     else:
    #         print("Please check input character and try again\n")
    

    key: str = os.getenv("API_KEY")
    secret: str = os.getenv("API_SECRET")
    bybit = Exchange(key, secret)

    nn, data = build_strategy("1")
    latest_value = data.get_latest_values()
    decision = nn.predict(latest_value)

    position = bybit.get_position(symbol="BTC-28MAR25")
    take_action(position, decision)

    bybit.create_order("linear", "BTCUSDT", "Buy", "Limit", "0.05", "72000")
    bybit.cancel_all()
    

if __name__ == "__main__":
    main()
