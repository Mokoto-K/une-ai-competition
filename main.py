# TODO - Implement everything from the cli, add a menu to check for different
# things like the trade you are in, profit?, etc
# TODO - strategies class for potential different risk strategies
# TODO - Build the api to the exchange
# TODO - Hide keys, also provide example api-key implementation?
# TODO - Cli logic
# TODO - indocrinate the impure to nvim

import data
from features import prep_data, get_latest_values 
from neuralnet import NeuralNetwork


def get_data():
    data.main()


def neural_net():
    # TODO - Change the X and y from features to be numpy arrays.
    # TODO - I think this needs to move outta here to a training class/module
    """
    Currently trains a neural network on the databases data and predicts the 
    next decision in the market.

    Returns:
    position - Either a 1 or 0 depending on the networks decision on the latest 
               data
    """

    # Structure for the nn
    architecture = [{"neurons": 5, "activation": "relu"},
                    {"neurons": 5, "activation": "relu"},
                    {"neurons": 3, "activation": "relu"},
                    {"neurons": 2, "activation": "relu"},
                    {"neurons": 1, "activation": "sigmoid"}
                    ]
    
    X_val, X_train, X_test, y_val, y_train, y_test = prep_data()
    decision = NeuralNetwork(X_train.to_numpy(), y_train.to_numpy().reshape(-1, 1), 
                             task = "binary", 
                             layers = architecture,
                             learning_rate = 0.1)

    decision.train(1000)

    # predictions = decision.predict(X_test[:5])
    #
    # print(f"nn predicted: {predictions}, actual was: {y_test[:5]}")
    latest_values = get_latest_values() 
    return 1 if decision.predict(latest_values) > 0.5 else 0


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
    

    # Update the database
    #get_data()
    print(get_latest_values)
    # Get the AI's decision on the market
    decision = neural_net()
    #print(decicion) 

    # Get the current position we are in
    position = get_position()
    
    take_action(position, decision)


if __name__ == "__main__":
    main()
