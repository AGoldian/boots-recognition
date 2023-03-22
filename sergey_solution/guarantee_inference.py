import pandas as pd
import numpy as np
from collections import defaultdict

guarantee = pd.read_csv("./data/test_mod_mktime_hash.csv")
hashes = pd.read_csv("./result/parse_result_20301.csv")
c=0
for index, col in guarantee.iterrows():
    if guarantee.loc[index, "class_id"] == -1:
        c += 1
        guarantee.loc[index, "class_id"] = hashes.loc[index, "class_id"]

guarantee.to_csv("./result/guarantee_mktime_parser.csv", index=0)
print(c)
