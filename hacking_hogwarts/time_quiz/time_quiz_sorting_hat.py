import numpy as np
import pandas as pd
import math
import json
import warnings
from plumbum import cli
from keras.models import Sequential
from keras import constraints
from keras import metrics
from keras.models import load_model, model_from_json
from pandas.io.json import json_normalize

from hacking_hogwarts.sorting_hat import SortingHat, HOGWARTS_HOUSES
#dense means fully connected layers, dropout is a technique to improve convergence, flatten to reshape our matrices for feeding
#into respective layers
from keras.layers import Dense, Dropout, Flatten
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

class TimeQuizSortingHat(SortingHat):
    INPUTS = [
        "hppi_pushes_hard",
        "hppi_worried_anxious",
        "hppi_sympathetic_warm",
        "hppi_dangerous_things",
        "hppi_critical_quarrelsome",
        "hppi_manipulate_others",
        "hppi_minimum_work",
        "hppi_flattery",
        "hppi_disorganized_careless",
        "hppi_deceit_lied",
        "hppi_feels_terrified",
        "hppi_treat_as_superior",
        "hppi_dependable_disciplined",
        "hppi_face_scary",
        "hppi_checks_work",
        "hppi_not_back_down",
        "hppi_more_respect",
        "hppi_ambitious_goals",
        "hppi_face_fears",
        "hppi_ordinary_person",
        "hppi_exploit_others",
    ]

    # LAYER NAMES
    MAIN_INPUT = "main_input"
    BIG_5 = "big_5"
    NORMALIZED_OUTPUT = "normalized_output"

    def __init__(self):
        super(TimeQuizSortingHat, self).__init__()

    def format_dataframe(self, df):
        # Load the house_sorting dataset
        house_sorting_df = df

        house_sorting_inputs = house_sorting_df.filter(regex='inputs.')

        # Remapping the house sorting input column names
        input_col_mapping = dict((c, c.replace("inputs.","")) for c in house_sorting_inputs.columns)

        # Creating inputs
        house_sorting_inputs = house_sorting_inputs.rename(columns=input_col_mapping)
        house_sorting_inputs = house_sorting_inputs[self.INPUTS]

        # Remapping the house sorting output column names
        house_sorting_outputs = house_sorting_df.filter(regex='results.')
        house_sorting_outputs = house_sorting_outputs.replace('%','', regex=True)
        house_sorting_outputs = house_sorting_outputs.astype('float')/100
        output_col_mapping = dict((c, c.replace("results.","")) for c in house_sorting_outputs.columns)

        # In place this time, since I don't rename this
        house_sorting_outputs.rename(columns=output_col_mapping, inplace=True)
        house_sorting_outputs = house_sorting_outputs[HOGWARTS_HOUSES]

        return (house_sorting_inputs, house_sorting_outputs)

    def generate_model(self, x_size, y_size):
        # create model
        model = Sequential()

        # Adding a layer with size equal to the number of inputs
        main_input_layer = Dense(
            x_size,
            name=self.MAIN_INPUT,
            input_dim=x_size,
            activation='relu',
        )
        model.add(main_input_layer)

        # Since they specify this is based on 'Big 5', adding
        # hidden layer to reflect this
        big_5_layer = Dense(
            5,
            name=self.BIG_5,
        )
        model.add(big_5_layer)

        # Since the outputs have been normalized, using softmax
        normalized_output_layer = Dense(
            y_size,
            name=self.NORMALIZED_OUTPUT,
            activation='softmax', 
            # kernel_constraint=constraints.max_norm(max_value=1.0),
        )
        model.add(normalized_output_layer)

        # Compile model
        model.compile(
            loss='mean_squared_error',
            optimizer='adam',
            metrics=[
                metrics.mae,
                metrics.categorical_accuracy,
            ],
        )
        return model

    def train(self):
        epochs = 1000
        batch_size = 128
        self.model = self.generate_model(
            x_size=len(self.INPUTS),
            y_size=len(HOGWARTS_HOUSES),
        )
        self.model.summary()

        history = self.model.fit(
            self.train_x, 
            self.train_y,
            batch_size=batch_size,
            epochs=epochs,
            shuffle=True,
            # verbose=0, # Change it to 2, if wished to observe execution
            validation_data=(
                self.test_x,
                self.test_y,
            ),
            # callbacks=keras_callbacks,
        )

    def predict(self, inputs):
        data = pd.DataFrame(data=json_normalize(inputs))
        data = data[self.INPUTS]
        return pd.DataFrame(
            data=self.model.predict(data),
            columns=HOGWARTS_HOUSES,
        )

    def evaluate(self):
        print("#### {} Evaluation ####".format(self.__class__.__name__))
        train_score = self.model.evaluate(
            self.train_x,
            self.train_y,
            verbose=0,
        )
        print(train_score)

        test_score = self.model.evaluate(
            self.test_x,
            self.test_y,
            verbose=0,
        )

        print(test_score)


