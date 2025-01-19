# import matplotlib.pyplot as plt 
import numpy as np

# TODO - More informative descriptions with proper params list, etc

class NeuralNetwork:
    
    def __init__(self, X, y, layers, task = 'binary', learning_rate=0.01, l2=0.0, training = False):
        
        # Adding checks for what type of data is being passed in as bugs persist
        self.X = X.to_numpy() if hasattr(X, "to_numpy") else np.array(X)
        temp_y = y.to_numpy() if hasattr(y, "to_numpy") else np.array(y)
        

        # Reshape y as needed depending on the task at hand, less reliance on input shapes
        # I feel like i could just auto reshape here but not smart enough to know how it
        # effects all types of models and y inputs in the future
        if len(temp_y.shape) == 1 or (len(temp_y.shape) == 2 and temp_y.shape[1] == 1):
            if task == "binary":
                self.y = temp_y.reshape(-1, 1)
            elif task == "multiclass":
                self.y = temp_y
            else: # For regression
                self.y = temp_y.reshape(-1, 1)
        else:
            self.y = temp_y

        self.layers = layers
        self.learning_rate = learning_rate
        self.params = {}
        self.cache = {}
        self.loss_history = []
        self.l2 = l2
        self.training = training
        
        # setting which output layer and loss functions to use depending on task 
        if task == 'binary':
            self.output_activation = self.sigmoid
            self.loss_function = self.binary_cross_entropy
        elif task == "multiclass":
            self.output_activation = self.softmax
            self.loss_function = self.categorical_cross_entropy
        elif task == "regression":
            self.output_activation = None
            self.loss_function = self.mean_squared_error
        else:
            raise ValueError("Task must be 'regression', 'binary' or 'multiclass'")

        self.initialization()

    
    def initialization(self):
        """ 
        Initializes all of the input weights and bias for the network
        """

        np.random.seed(42)

        input_dimensions = self.X.shape[1]
        
        # Setting initial weights and bias
        for i, layer in enumerate(self.layers):
            layer_number = f"layer_{i+1}"
            neurons = layer["neurons"]

            self.params[f"W_{layer_number}"] = np.random.randn(input_dimensions, neurons) * np.sqrt(2 / input_dimensions)
            self.params[f"b_{layer_number}"] = np.zeros((1, neurons))

            input_dimensions = neurons

    
    def relu(self, z):
        """
        returns either 0 or the value of z, depending on which is bigger
        """
        return np.maximum(0, z)


    def relu_deriv(self, dz):
        """
        The derivative of our relu function
        """
        return (dz > 0).astype(float)
        
    
    def sigmoid(self, z):
        """
        returns a value between 0 - 1, used mostly for our binary output layer
        """
        return 1 / (1 + np.exp(-z))


    def sigmoid_deriv(self, z):
        """
        The derivative of our sigmoid function 
        """
        s = self.sigmoid(z)
        return s * (1 - s)


    def softmax(self, z):
        """
        Used for multiclassification only, will return a bunch of values between
        0 - 1 all adding upto 1 in total
        """
        exp_z = np.exp(z - np.max(z, axis = 1, keepdims = True))
        return exp_z / np.sum(exp_z, axis = 1, keepdims = True)


    def binary_cross_entropy(self, y, y_hat):
        """
        the loss function for binary classification, used to help adjust weights
        for back prop
        """
        epsilon = 1e-8
        return -np.mean(y * np.log(y_hat + epsilon) + (1 - y) * np.log(1 - y_hat + epsilon))
    

    def categorical_cross_entropy(self, y, y_hat):
        """
        The loss function for multiclass classification, used to help adjust
        weights for back propagation
        """
        return -np.mean(np.sum(y * np.log(y_hat + 1e-8),axis = 1))
    

    def mean_squared_error(self, y, y_hat):
        """
        The loss function for linear regression, used to help calc and adjust
        the weights for back prop
        """
        return np.mean((y - y_hat) ** 2)

    
    def forward_prop(self):
        """
        The forward pass through the network that calcs a weighted sum of the 
        input, weight and bias, which is passed to the selected activation 
        function over and over for every connection to every neuron until we 
        make it to the final layer and produce a prediciton ( I should probably
        get better at descripbing these things.
        """
        A = self.X
        self.cache["A_0"] = A

        for idx, layer in enumerate(self.layers):
            layer_id = f"layer_{idx + 1}"
            W = self.params[f"W_{layer_id}"]
            b = self.params[f"b_{layer_id}"]

            Z = np.dot(A, W) + b
            activation = layer["activation"]

            if idx < len(self.layers) -1:
                if activation == "relu":
                    A = self.relu(Z)
                elif activation == "sigmoid":
                    A = self.sigmoid(Z)
                elif activation == None:
                    A = Z
                else:
                    raise ValueError("Unsupported activation function")
            else:
                if self.output_activation:
                    A = self.output_activation(Z)
                else:
                    A = Z

            self.cache[f"Z_{layer_id}"] = Z
            self.cache[f"A_{idx + 1}"] = A
        
        return A

        
    def back_prop(self, y_hat):
        """
        The back pass through the network that uses a loss function to calc how
        much each neuron contributed to the mistakes of its ancestors which is 
        then used to re adjust the weights for the next forward prop
        """
        m = self.y.shape[0]
        epsilon = 1e-8
        dA = - (np.divide(self.y, y_hat + epsilon) - np.divide(1 - self.y, 1 - y_hat + epsilon))

        for idx in reversed(range(len(self.layers))):
            layer_id = f"layer_{idx + 1}"
            Z = self.cache[f"Z_{layer_id}"]
            A_prev = self.cache[f"A_{idx}"]

            activation = self.layers[idx]["activation"]
            W = self.params[f"W_{layer_id}"]

            if activation == "relu":
                dZ = dA * self.relu_deriv(Z)
            elif activation == "sigmoid":
                dZ = dA * self.sigmoid_deriv(Z)
            elif activation is None:
                dZ = dA 
            else:
                raise ValueError("Unsupported activation function")

            dW = (np.dot(A_prev.T, dZ) / m) + (self.l2 * self.params[f"W_{layer_id}"])
            db = np.sum(dZ, axis = 0, keepdims = True) / m
            dA = np.dot(dZ, W.T)

            self.params[f"W_{layer_id}"] -= self.learning_rate *dW
            self.params[f"b_{layer_id}"] -= self.learning_rate *db

            
    def train(self, epochs=100, validation=None):
        """
        Trains the neural network on the input data
        """

        if not self.training:
            print("I'm thinking of what to do...\n")

        for epoch in range(epochs):
            y_hat = self.forward_prop()

            loss = self.loss_function(self.y, y_hat)

            # Implementation of L2 reg hopefully to help generalize better.
            l2_penalty = (self.l2 / (2 * self.X.shape[0])) * sum(np.sum(
                np.square(self.params[f"W_layer_{i + 1}"]))
                for i in range(len(self.layers)))
            total_loss = loss + l2_penalty
            
            self.loss_history.append(loss)
            self.back_prop(y_hat)

            if self.training and epoch % 100 == 0:

                # add validation scoring to the training to observe overtraining
                if validation is not None: 
                    X_val, y_val = validation

                    # Handle conversion of dataframe to numpy array if needed...(it is)
                    X_val = X_val.to_numpy() if hasattr(X_val, "to_numpy") else np.array(X_val)
                    y_val = y_val.to_numpy() if hasattr(y_val, "to_numpy") else np.array(y_val)
            
                    # Reshape y_val to match training data shape
                    if len(y_val.shape) == 1 or (len(y_val.shape) == 2 and y_val.shape[1] == 1):
                        y_val = y_val.reshape(-1, 1)

                    val_pred = self.predict(X_val)
                    val_loss = self.loss_function(y_val, val_pred)

                    print(f"Epoch {epoch:5} | Train Loss: {total_loss:.4f} | "
                          f"Val Loss: {val_loss:.4f} | "
                          f"diff: {(total_loss - val_loss):.4f}")

                else:
                    print(f"Epoch {epoch}, Loss: {total_loss:.4f}")

        if not self.training:
            print("Found a solution!\n")

        
    def predict(self, X):
        """
        Makes a prediction on a passed in set of features.
        """
        
        # Add protections for X being misshaped
        X = X.reshape(1, -1) if len(X.shape) == 1 else X

        A = X
        for idx, layer in enumerate(self.layers):
            layer_id = f"layer_{idx + 1}"
            W = self.params[f"W_{layer_id}"]
            b = self.params[f"b_{layer_id}"]

            Z = np.dot(A, W) + b
            if idx < len(self.layers) - 1:
                activation = layer["activation"]
                A = self.relu(Z) if activation == "relu" else self.sigmoid(Z)
            else:
                A = self.output_activation(Z) if self.output_activation else Z

        return A


    # def visualize(self):
    #
    #     plt.plot(range(len(self.loss_history)), self.loss_history)
    #     plt.xlabel("Epochs")
    #     plt.ylabel("Loss")
    #     plt.title("Loss Over Epochs")
    #     plt.grid()
    #     plt.show()

if __name__ == "__main__":
    pass
