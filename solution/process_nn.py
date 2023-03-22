import pandas as pd
import numpy as np
from collections import defaultdict

best_model = pd.read_csv(r"./result/beda_best.csv", index_col=0)
mapa = pd.read_csv(r"./result/map_best.csv", index_col=0)

# Apply the function to each row of the dataframe to extract the desired class ID
best_model['new_column'] = best_model['class_id'].apply(lambda x: eval(x)[1] if isinstance(eval(x)[0], str) else eval(x)[0])

dd = pd.DataFrame()
dd['class_id'] = mapa['class_id']
dd['individual_id'] = mapa['individual_id']
dicts = dd.to_dict('split')

res = [item for item in dicts["data"]]
dict_my_mapped = defaultdict()

for m in res:
    dict_my_mapped[m[1]] = (m[0])
dict_my_mapped[-1] = -1

# read orig files, because was infered on test_mod
orig_df = pd.read_csv(r'./result/test.csv', index_col=0)
orig_df["class_id"] = orig_df['image'].map(best_model.set_index('image')['new_column'])
orig_df["class_id"] = orig_df["class_id"].fillna(-1)
orig_df["class_id"] = orig_df["class_id"].astype("int64")
orig_df["class_id"] = orig_df['class_id'].map(dict_my_mapped)
orig_df.to_csv("./result/best_ever.csv", index=False)
