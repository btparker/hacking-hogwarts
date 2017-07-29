import numpy as np
import pandas as pd
import math
import json
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

PERCENT_TEST = 0.2

# Mostly being cute here, this is the base class
# for predictive models
class SortingHat(object):
    def __init__(self):
        self.num_test = 0
        self.house_sorting_train_inputs = None
        self.house_sorting_test_inputs = None
        self.house_sorting_train_outputs = None
        self.house_sorting_test_outputs = None

    def load_dataframe(self, dataframe_path):
        """Load and split dataframe into inputs, outputs for
        training and evaluation
        """

        # Load the house_sorting dataset
        house_sorting_df = pd.read_pickle(dataframe_path)

        house_sorting_inputs = house_sorting_df.filter(regex='inputs.')

        # Remapping the house sorting input column names
        input_col_mapping = dict((c, c.replace("inputs.","")) for c in house_sorting_inputs.columns)

        # Creating inputs
        house_sorting_inputs = house_sorting_inputs.rename(columns=input_col_mapping)

        # Remapping the house sorting output column names
        house_sorting_outputs = house_sorting_df.filter(regex='results.')
        output_col_mapping = dict((c, c.replace("results.","")) for c in house_sorting_outputs.columns)

        # In place this time, since I don't rename this
        house_sorting_outputs.rename(columns=output_col_mapping, inplace=True)

        NUM_TEST = int(math.floor(PERCENT_TEST * house_sorting_inputs.shape[0]))

        # Split into train and test
        self.house_sorting_train_inputs = house_sorting_inputs[:-NUM_TEST]
        self.house_sorting_test_inputs = house_sorting_inputs[-NUM_TEST:]

        self.house_sorting_train_outputs = house_sorting_outputs[:-NUM_TEST]
        self.house_sorting_test_outputs = house_sorting_outputs[-NUM_TEST:]

    def train(self):
        pass

    def predict(self):
        pass

class LinearRegressionSortingHat(SortingHat):
    def __init__(self):
        super(LinearRegressionSortingHat, self).__init__()
        self.house_models = {}


    def train(self):
        from sklearn import linear_model

        # I will try to create multiple generalized models, but since the outputs are normalized
        # they are codependent and I have yet to figure out a way to handle this with sklearn
        for house_name in self.house_sorting_train_outputs.columns:
            house_sorting_lm = linear_model.LinearRegression()
            house_sorting_train_y = self.house_sorting_train_outputs[house_name]

            # Fit the model
            house_model =  house_sorting_lm.fit(self.house_sorting_train_inputs, house_sorting_train_y)
            self.house_models[house_name] = house_model

    def predict(self, inputs):
    
        results = {}

        for house_name in self.house_sorting_train_outputs.columns:
            house_sorting_lm = self.house_models[house_name]
            results[house_name] = house_sorting_lm.predict(inputs)

        results_df = pd.DataFrame(results)
        min_df = results_df.min(axis=1)
        max_df = results_df.max(axis=1)
        normalized_results_df = (results_df.sub(min_df, axis=0)).div(max_df.sub(min_df, axis=0), axis=0)
        return normalized_results_df

    def evaluate(self):
        print("-- Mean squared error --")
        for house_name in self.house_sorting_train_outputs.columns:
            house_sorting_test_y = self.house_sorting_test_outputs[house_name]
            house_sorting_lm = self.house_models[house_name]
            mean_squared_error = np.mean((house_sorting_lm.predict(self.house_sorting_test_inputs) - house_sorting_test_y) ** 2)
            print("{}: {:0.5f}".format(house_name, mean_squared_error))
            
        print("-- Variance score (1.0 is a perfect score) --")
        for house_name in self.house_sorting_train_outputs.columns:
            house_sorting_test_y = self.house_sorting_test_outputs[house_name]
            house_sorting_lm = self.house_models[house_name]

            # 1.0 is a perfect score
            variance_score = house_sorting_lm.score(self.house_sorting_test_inputs, house_sorting_test_y)
            print('{}: {:0.2f}'.format(house_name, variance_score))

def main():
    sorting_hat = LinearRegressionSortingHat()
    sorting_hat.load_dataframe('data/dataframe.pkl')
    sorting_hat.train()
    sorting_hat.evaluate()


if __name__ == "__main__":
    main()


