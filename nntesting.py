# Instead of practically curve fitting here testing different layer combos, neuron
# amounts and activation functions, I want to build the testing into the nn class
# and havew it far more stream lined, I also want to be able to save the model and 
# warm start it or better yet just thread it and hot start it... not sure which and
# how.

from neuralnetwork import NeuralNetwork
from features import DataFeatures

file_path = "./BTCUSDT_1_Data.csv"

data = DataFeatures(file_path)
data.process_all_features()
X_train, X_test, X_val, y_train, y_test, y_val= data.prep_data()


layer_config = [
    [{"neurons": 9, "activation": "relu"},
     {"neurons": 7, "activation": "relu"},
     {"neurons": 5, "activation": "relu"},
     {"neurons": 3, "activation": "relu"},
     {"neurons": 1, "activation": "sigmoid"}
     ],
    [{"neurons": 15, "activation": "relu"},
     {"neurons": 7, "activation": "relu"},
     {"neurons": 3, "activation": "relu"},
     {"neurons": 1, "activation": "sigmoid"}
     ],
    [{"neurons": 3, "activation": "relu"},
     {"neurons": 2, "activation": "relu"},
     {"neurons": 1, "activation": "sigmoid"}
     ],
    [{"neurons": 5, "activation": "relu"},
     {"neurons": 5, "activation": "relu"},
     {"neurons": 3, "activation": "relu"},
     {"neurons": 2, "activation": "relu"},
     {"neurons": 1, "activation": "sigmoid"}
     ],
    [{"neurons": 7, "activation": "relu"},
     {"neurons": 6, "activation": "relu"},
     {"neurons": 5, "activation": "relu"},
     {"neurons": 4, "activation": "relu"},
     {"neurons": 3, "activation": "relu"},
     {"neurons": 2, "activation": "relu"},
     {"neurons": 1, "activation": "sigmoid"}
     ],

]

best_nn = i = 0 
epochs = 2000
lowest_loss = 1
for layers in layer_config:
     
    nn = NeuralNetwork(X_train, y_train, layers = layers, learning_rate=0.1, training = True)
    
    nn.train(epochs, (X_val, y_val))
    
    y_pred = nn.predict(X_val)
    
    correct = mistake = 0
    
    for true, pred in zip(y_test, y_pred):
        if true == 1 and pred > 0.5:
            correct += 1
        elif true == 0 and pred < 0.5:
            correct += 1
        else:
            mistake += 1
    
    print(f"correct: {correct}\nmistakes: {mistake}\n%: {correct /(correct+mistake) *100}")

    if float(nn.loss_history[epochs-1]) < lowest_loss:
        best_nn = i 
        lowest_loss = nn.loss_history[epochs-1]
        
    i+=1
print(best_nn, lowest_loss)
