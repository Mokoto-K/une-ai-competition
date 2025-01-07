from features import MarketFeatures
from neuralnetwork import NeuralNetwork
from data import Database


def default_strategy():
    database = Database(time_frame = "1") 
    database.run()
    file_path = database.get_file_name()

    # Temp function, very bad behaviour btw

    data = MarketFeatures(file_path)
    data.process_all_features()

    # Get the data for the nn
    X_train, X_test, X_val, y_train, y_test, y_val = data.prep_data()

    # Structure for the nn
    architecture = [{"neurons": 5, "activation": "relu"},
                    {"neurons": 5, "activation": "relu"},
                    {"neurons": 3, "activation": "relu"},
                    {"neurons": 2, "activation": "relu"},
                    {"neurons": 1, "activation": "sigmoid"}
                    ]

    # INitialize the bad boi
    decision = NeuralNetwork(X_train, y_train, 
                             task = "binary", 
                             layers = architecture,
                             learning_rate = 0.1)

    # Train him
    decision.train(1000)

    # temp sending the file name this way, obvs refactor to a class shortly
    return decision, file_path
    # return X_train, y_train, "binary", architecture, 0.1

    
if __name__ == "__main__":
    pass
