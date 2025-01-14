# This class is great but was the source of most pain in the project, could have
# just used scikitlearn.

import numpy as np
import pandas as pd

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

    def fit(self, y):
        """
        Converts each unqiue instant of our char/str labels into an int val and index          
        """

        self.classes_ = np.unique(y)


        self._mapping = {val: idx for idx, val in enumerate(self.classes_)}
        return self


    def transform(self, y):
        """
        Creates a numpy array out of our converted vals 
        """
        return np.array([self._mapping[val] for val in y])


    def fit_transform(self, y):
        """
        Combines the converting and creating of our labels to a numpoy array 
        """
        return self.fit(y).transform(y)


    def uno_reverse_transform(self, y):
        """
        ever played uno? ever use the reverse? ever done math? *raises eyebrows twice
        at you*
        """
        return self.classes_[y]


# THIS WAS A TERRIBLE IDEA, THE PROBLEMS I HAD WERE NOT WORTH IT!!!!!
class NonStandardScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None


    def fit(self, X):
        """
        Fits the passed in data to the scaler by calculating the mean and std
        of the data, saving them as class variables
        """
        
        # controls for what X may be.... pain 
        if isinstance(X, pd.DataFrame):

            self.mean_ = X.mean().values            #.values CAUSED SO MUCH PAIN
            self.scale_ = X.std(ddof=0).values
        else:

            X = np.array(X)
            self.mean_ = np.mean(X, axis=0)
            self.scale_ = np.std(X, axis=0, ddof=0)

        # controls where std is zero to avoid division by zero
        self.scale_ = np.where(self.scale_ == 0, 1.0, self.scale_)

        return self


    def transform(self, X):
        """
        Standardizes the data by removing the mean and scaling the variance
        """
        if self.mean_ is None or self.scale_ is None:
            raise ValueError("Scaler has not been fitted yet. Call 'fit' first.")

        # Controlling for panadas or numpy ds again
        if isinstance(X, pd.DataFrame):
            return pd.DataFrame(
                (X.values - self.mean_) / self.scale_,
                index=X.index,
                columns=X.columns,)

        X = np.array(X)
        return (X - self.mean_) / self.scale_


    def fit_transform(self, X):
        """
        Fit and transform the data in one.
        """
        return self.fit(X).transform(X)


# class UnstandardScaler():
#
#     def __init__(self) -> None:
#         self.mean = None
#         self.scale = None
#
#
#     def fit(self, X):
#         """
#         Fits the passed in data to the scaler by calculating the mean and std
#         of the data, saving them as class variables
#         """
#
#         self.mean = np.mean(X, axis=0)
#         self.scale = np.std(X, axis=0, ddof=1)
#
#         # checks zero std situation
#         self.scale = np.where(self.scale == 0, 1.0, self.scale)
#
#         return self
#
#
#     def transform(self, X):
#         """
#         Standardizes the data by removing the mean and scaling the variance
#         """
#
#         if self.mean is None or self.scale is None:
#             raise ValueError("Scaler has not been fitted yet. Call 'fit' first.")
#
#         # Check for pandas dataframe over numpy array (this caused me a slow death)
#         if isinstance(X, pd.DataFrame):
#             X_array = X.values
#             if X_array.shape[1] != self.mean.shape[0]:
#                 raise ValueError(
#                     f"Mismatch: X has {X_array.shape[1]} features but scaler expects {self.mean.shape[0]} features."
#                 )
#             standardized = (X_array - self.mean) / self.scale
#             return pd.DataFrame(standardized, index=X.index, columns=X.columns)
#
#         # scale if its a numpy array
#         X = np.array(X)
#         return (X - self.mean) / self.scale
#
#
#     def fit_transform(self, X):
#         """
#         Fit and transform the data in one.
#         """
#         return self.fit(X).transform(X)
#
#
