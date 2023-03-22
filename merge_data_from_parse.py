import os
import pandas as pd
from tqdm import tqdm

DIR_FILES = r'parse_Data\\' # Directory PARSE DATA
fork_test = pd.read_csv(r'data\test.csv')
fork_test['class_id'] = -1

print('Start added data')
database = []
for file in tqdm(os.scandir(DIR_FILES)):
    tmp_df = pd.read_csv(file.path)
    tmp_df = tmp_df[tmp_df['class_id'] != -1]
    database.append(tmp_df)

print('Data added in database')


print('STARTING MERGE')
for dataframe in tqdm(database):
    for i, row in dataframe.iterrows():
        fork_test.loc[fork_test['image'] == row.image, 'class_id'] = row.class_id

    print(f'Added {len(dataframe)} rows in main dataframe')

fork_test.to_csv('merge_with_parse_test.csv', index=False)
print(f'Remaining {fork_test.class_id.value_counts()[-1]}/{len(fork_test)}')

print('DONE!')
print('Copyright SBER.')