import pandas as pd
import numpy as np
from collections import defaultdict

result = pd.read_csv("./result/best_hash.csv")
hashes = pd.read_csv("./data/test_mod_mktime_hash.csv")
c = 0
for index, col in hashes.iterrows():
    if hashes.loc[index, "class_id"] != -1:
        if hashes.loc[index, "class_id"] != result.loc[index, "class_id"]:
            print(result.loc[index, "image"])
            c += 1
        result.loc[index, "class_id"] = hashes.loc[index, "class_id"]
result.to_csv("./result/best_with_test_mod_mktime_hash.csv", index=0)

print(c)
