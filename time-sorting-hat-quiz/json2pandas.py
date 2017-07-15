import numpy as np
import pandas as pd
from os import path
from pandas.io.json import json_normalize
from glob import glob
import json

JSON_DIR = 'data/scraped_json/'

data = []
for file_name in glob(path.join(JSON_DIR, '*.json')):
    with open(file_name) as f:
        data.append(json.load(f))

df = pd.DataFrame(data=json_normalize(data))

# Convert the scraped percentage values to float values
df = df.replace('%','',regex=True).astype('float')/100
df.to_pickle('data/dataframe.pkl')
