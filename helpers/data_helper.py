import pandas as pd
import numpy as np
import random
import string


columns = ['national_rank', 'quality_of_education', 'alumni_employment', 'quality_of_faculty',
           'publications', 'influence', 'citations', 'broad_impact', 'patents']


# Normalize the data so that it's easier to compare
def normalize_and_filter_data():
    in_df = pd.read_csv('../datasets/cwur_data.csv')

    # Get only year 2015
    filtered = in_df[in_df['year'] == 2015]

    normalized = filtered.copy()
    for feature_name in columns:
        max_val = filtered[feature_name].max()
        min_val = filtered[feature_name].min()
        normalized[feature_name] = round((filtered[feature_name] - min_val) / (max_val - min_val), 4)

    normalized.set_index("world_rank", inplace=True)
    normalized.to_csv('../datasets/cwur_data_normalized.csv')


# Generate random data for testing
def generate_random():
    df_size = 7000

    df = pd.DataFrame(np.random.uniform(0, 1.0, size=(df_size, len(columns))), columns=columns)
    for col in columns:
        df[col] = df[col].round(decimals=4)

    letters = string.ascii_lowercase
    df['institution'] = [''.join(random.choice(letters) for _ in range(5)) for _ in range(df_size)]

    df.index.name = 'world_rank'

    print(df.head(10))

    df.to_csv('../datasets/random.csv')


generate_random()
