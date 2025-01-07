# TODO - Implement everything from the cli, add a menu to check for different
# things like the trade you are in, profit?, etc
# TODO - strategies class for potential different risk strategies
# TODO - Build the api to the exchange
# TODO - Hide keys, also provide example api-key implementation?
# TODO - Cli logic
# TODO - indocrinate the impure to nvim

from data import Database
from features import MarketFeatures
from neuralnetwork import NeuralNetwork
from strategy import default_strategy
from simulation import run_simulation
#FILE_PATH = "./BTCUSDT_D_Data.csv"

def get_data():
    data = Database(time_frame="D")
    data.run()


# def neural_net():
#     # TODO - Change the X and y from features to be numpy arrays.
#     # TODO - I think this needs to move outta here to a training class/module
#     """
#     Currently trains a neural network on the databases data and predicts the 
#     next decision in the market.
#
#     Returns:
#     position - Either a 1 or 0 depending on the networks decision on the latest 
#                data
#     """
#     # TODO - Temporarily putting the data and nn structure in here, needs its own class
#
#     data = MarketFeatures(FILE_PATH)
#     data.process_all_features()
#
#     # Get the data for the nn
#     X_train, X_test, X_val, y_train, y_test, y_val = data.prep_data()
#
#     # Structure for the nn
#     architecture = [{"neurons": 5, "activation": "relu"},
#                     {"neurons": 5, "activation": "relu"},
#                     {"neurons": 3, "activation": "relu"},
#                     {"neurons": 2, "activation": "relu"},
#                     {"neurons": 1, "activation": "sigmoid"}
#                     ]
#
#     # INitialize the bad boi
#     decision = NeuralNetwork(X_train, y_train, 
#                              task = "binary", 
#                              layers = architecture,
#                              learning_rate = 0.1)
#
#     # Train him
#     decision.train(1000)
#
#     # Get the next decision to take 
#     latest_values = data.get_latest_values() 
#     print(latest_values)
#     return 1 if decision.predict(latest_values) > 0.5 else 0


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

    if position != "none":
        if position == decision:
            print(f"We are in a {position} and will remain {decision}")
        else:
            print(f"We are closing our {position} position")
            # close_position() 
    else:
        print(f"Not in any position, Entering a {decision}")
        # enter_position()

        
def main():
    # TODO - Hide all of the print statements for training the neural net
    # data = Database(time_frame="1")
    # data.run()
    # default_strategy()
    run_simulation()
    # Update the database
    #get_data()

    # Get the AI's decision on the market
    # decision = neural_net()
    #print(decicion) 

    # Get the current position we are in
    # position = get_position()
    
    # take_action(position, decision)


if __name__ == "__main__":
    main()
