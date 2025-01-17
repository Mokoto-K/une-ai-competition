# TODO - this may need to be a class, figure that out fast
# TODO - add ability for risk to adjust % size to allocate for trading
# TODO - Have the nural net decide what risk strategy based on market conditions
# TODO - :wq
# TODO - duplicated straties to serve different purposes for now, can be rewritten better

from features import DataFeatures
from neuralnetwork import NeuralNetwork
from database import Database

# Currently a dup class of build strat, rework for sim only, different flow
def sim_strategy(risk: str = "D"):
    database = Database(time_frame = risk[0]) # passing only the first letter in 
    database.run()
    file_path = database.get_file_name()
    data = DataFeatures(file_path)
    data.process_all_features()
    # Get the data for the nn, no need for test or val data, testing done elsewhere
    X_train, _, _, y_train, _, _= data.prep_data()

    # Structure for the nn
    architecture = [{"neurons": 9, "activation": "relu"},
                    {"neurons": 7, "activation": "relu"},
                    {"neurons": 5, "activation": "relu"},
                    {"neurons": 3, "activation": "relu"},
                    {"neurons": 1, "activation": "sigmoid"}
                    ]
    # INitialize the bad boi
    nn = NeuralNetwork(X_train, y_train, 
                             task = "binary", 
                             layers = architecture,
                             learning_rate = 0.1, training=False)
    # Train him
    nn.train(2000)

    return nn, data


def build_strategy(risk: str = "D"):
    database = Database(time_frame = risk[0]) # passing only the first letter in 
    database.run()
    file_path = database.get_file_name()

    data = DataFeatures(file_path)
    data.process_all_features()

    # Get the data for the nn, no need for test or val data, testing done elsewhere
    X_train, _, _, y_train, _, _= data.prep_data()

    # Structure for the nn
    architecture = [{"neurons": 9, "activation": "relu"},
                    {"neurons": 7, "activation": "relu"},
                    {"neurons": 5, "activation": "relu"},
                    {"neurons": 3, "activation": "relu"},
                    {"neurons": 1, "activation": "sigmoid"}
                    ]

    # INitialize the bad boi
    nn = NeuralNetwork(X_train, y_train, 
                             task = "binary", 
                             layers = architecture,
                             learning_rate = 0.1, training=False)

    # Train him
    nn.train(2000)
   
    # Get latest prediction in terms of what the market will understand 
    decision = "Buy" if nn.predict(data.get_latest_values()) > 0.5 else "Sell"

    return decision


# Another fantastic bandaid being applied!!!
def risk_amount(risk):
    return 0.01 if risk[0] == "D" else 0.02  # Only looking at first letter of risk

    
if __name__ == "__main__":
    pass
