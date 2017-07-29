import numpy as np
from sklearn import linear_model
import pandas as pd
import math
import json

PERCENT_TEST = 0.2

# Load the house_sorting dataset
house_sorting_df = pd.read_pickle('data/dataframe.pkl')

house_sorting_inputs = house_sorting_df.filter(regex='inputs.')

# Remapping the house sorting input column names
input_col_mapping = dict((c, c.replace("inputs.","")) for c in house_sorting_inputs.columns)

# Creating X, mainly for naming convention
house_sorting_X = house_sorting_inputs.rename(columns=input_col_mapping)

# Remapping the house sorting output column names
house_sorting_outputs = house_sorting_df.filter(regex='results.')
output_col_mapping = dict((c, c.replace("results.","")) for c in house_sorting_outputs.columns)

# In place this time, since I don't rename this
house_sorting_outputs.rename(columns=output_col_mapping, inplace=True)

# Saving model outputs
output = []

NUM_TEST = int(math.floor(PERCENT_TEST * house_sorting_X.shape[0]))

# I will try to create multiple generalized models, but since the outputs are normalized
# they are codependent and I have yet to figure out a way to handle this with sklearn
for house_name in house_sorting_outputs.columns:
	house_sorting_lm = linear_model.LinearRegression()
	house_sorting_y = house_sorting_outputs[house_name]

	# Split into train and test
	house_sorting_X_train = house_sorting_X[:-NUM_TEST]
	house_sorting_X_test = house_sorting_X[-NUM_TEST:]

	house_sorting_y_train = house_sorting_y[:-NUM_TEST]
	house_sorting_y_test = house_sorting_y[-NUM_TEST:]

	# Fit the model
	house_model = house_sorting_lm.fit(house_sorting_X_train, house_sorting_y_train)
	print("house {}".format(house_name))
	print("coef {}".format(house_sorting_lm.coef_))

	print("intercept {}".format(house_sorting_lm.intercept_))

	mean_squared_error = np.mean((house_sorting_lm.predict(house_sorting_X_test) - house_sorting_y_test) ** 2)
	print("Mean squared error: {:0.2f}".format(mean_squared_error))

	# 1.0 is a perfect score
	variance_score = house_sorting_lm.score(house_sorting_X_test, house_sorting_y_test)
	print('Variance score: {:0.2f}'.format(variance_score))

	item = dict(zip(house_sorting_X.columns, house_sorting_lm.coef_))
	item['house'] = house_name
	item['intercept'] = house_sorting_lm.intercept_

	output.append(item)

with open('data/sklearn/model.json', 'w') as outfile:
    json.dump(output, outfile)


