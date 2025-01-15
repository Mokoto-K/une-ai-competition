# TODO - this may need to be a class, figure that out fast
# TODO - add ability for risk to adjust % size to allocate for trading
# TODO - Have the nural net decide what risk strategy based on market conditions
# TODO - :wq

from features import DataFeatures
from neuralnetwork import NeuralNetwork
from database import Database


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

    # TODO - Find a better way to define risk amount, like a map maybe
    risk_percentage: float = 0.03 if risk == "D" else 0.05
    return nn, data, risk_percentage

    
if __name__ == "__main__":
    pass
