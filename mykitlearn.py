import numpy as np

def split_test_train(X, y, test_size = 0.2, random_state = None) -> tuple:
    """
    Definitely a function I built from my brain and not an exact replica of 
    scikit learns "train_test_split", nuh uh... certainly not, you can't even
    select training size, shuffle or stratify!

    Params:
    X - an array full of features ready for training
    y - an array full of labels for the X set of features
    test_size - the percent of instances to be used for testing only
    random_state - Controls the randomness of the shuffling for repeated results

    Returns:
    X_train - The X set of features to train on
    X_test - The X set of features to test on
    y_train - The set of training labels for the training set
    y_test - The set of testing labels for the testing set
        """
    # set a rando seed if provided
    if random_state is not None:
        np.random.seed(random_state)
    
    # Calculate the number of test samples
    training_samples: int = len(X)
    test_samples: int = int(training_samples * test_size)

    # Create a random order the length of our dataset to shuffle the order
    shuffle = np.random.permutation(training_samples)

    # Split the shuffled ordering into our two sets
    training_set: np.ndarray = shuffle[test_samples: ]
    test_set: np.ndarray = shuffle[: test_samples]

    # train_test_split.inc ;)
    if hasattr(X, 'iloc'):
        # If they are a pandas dataframe (this bug got me for moment)
        X_train = X.iloc[training_set]
        X_test = X.iloc[test_set]
        y_train = y.iloc[training_set]
        y_test = y.iloc[test_set]
    else:
        # If they are a normal numpy array
        X_train: np.ndarray = X[training_set]
        X_test: np.ndarray = X[test_set]
        y_train: np.ndarray = y[training_set]
        y_test: np.ndarray = y[test_set]
    
    return X_train, X_test, y_train, y_test


# Ok I did practically use sklearns labelencoder for this one.... i did change 
# the name though... an original thought!
class encode_labeler:
# TODO - Rewrite with y init so that its not needed to be passed in on uno_reverse
# TODO - Write up documentation at some point when there are less things to do

    def fit(self, y):
        """
          
        """

        self.classes_ = np.unique(y)


        self._mapping = {val: idx for idx, val in enumerate(self.classes_)}
        return self


    def transform(self, y):
        """
          
        """
        return np.array([self._mapping[val] for val in y])


    def fit_transform(self, y):
        """
          
        """
        return self.fit(y).transform(y)


    def uno_reverse_transform(self, y):
        """
          
        """
        return self.classes_[y]

