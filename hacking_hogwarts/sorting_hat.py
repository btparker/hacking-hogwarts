import numpy as np
import pandas as pd
import math
import json
import warnings
from keras.models import Sequential
from keras import constraints
from keras import metrics
from keras.models import load_model, model_from_json
from pandas.io.json import json_normalize
#dense means fully connected layers, dropout is a technique to improve convergence, flatten to reshape our matrices for feeding
#into respective layers
from keras.layers import Dense, Dropout, Flatten
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

PERCENT_TEST = 0.2

HOGWARTS_HOUSES = [
    "Gryffindor",
    "Hufflepuff",
    "Ravenclaw",
    "Slytherin",
]

class SortingHat(object):
    def __init__(self):
        self.num_test = 0
        self.train_x = None
        self.test_x = None
        self.train_y = None
        self.test_y = None

    def load_model(self, model_path):
        import os
        filename = os.path.splitext(model_path)[0]

        json_model_path = "{}.json".format(filename)
        json_model_file = open(json_model_path, "r")
        loaded_model_json = json_model_file.read()
        json_model_file.close()
        
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("{}.h5".format(filename))
        self.model = loaded_model

    def format_dataframe(self, df):
        pass

    def load_dataframe(self, dataframe_path):
        """Load and split dataframe into inputs, outputs for
        training and evaluation
        """

        from sklearn import model_selection

        df = pd.read_pickle(dataframe_path)

        (inputs, outputs) = self.format_dataframe(df)

        # Split into train and test
        (
            self.train_x,
            self.test_x,
            self.train_y,
            self.test_y,
        ) = model_selection.train_test_split(
            inputs,
            outputs,
            test_size=PERCENT_TEST,
            random_state=42
        )

    def train(self):
        pass

    def predict(self):
        pass

    def save(self, path):
        import os
        filename = os.path.splitext(path)[0]
        self.model.save_weights("{}.h5".format(filename))
        model_json = self.model.to_json()

        with open("{}.json".format(filename), "w") as json_file:
            json_file.write(model_json)
        
        self.model.save_weights("{}.h5".format(filename))
