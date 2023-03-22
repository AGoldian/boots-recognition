import pandas as pd
import numpy as np
from collections import defaultdict

nn_result = pd.read_csv("./result/best_hash.csv")
ebay_result = pd.read_csv("./result/parse_result_20301.csv")
# mktime_result = pd.read_csv("./data/test_mod_mktime_hash.csv")
mktime_result_1 = pd.read_csv(r"C:\Users\Sergey\PycharmProjects\Python3_9\filled_true_1_mktime.csv")
mktime_result_2 = pd.read_csv(r"C:\Users\Sergey\PycharmProjects\Python3_9\filled_true_2_mktime.csv")
mktime_result_3 = pd.read_csv(r"C:\Users\Sergey\PycharmProjects\Python3_9\filled_true_3_mktime.csv")
# another_nn_result = pd.read_csv("./result/test_my109.csv")
c = 0
k = 0
for index, col in nn_result.iterrows():
    results = [int(nn_result.loc[index, "class_id"]),
           int(ebay_result.loc[index, "class_id"]),
           # int(another_nn_result.loc[index, "class_id"]),
           int(mktime_result_1.loc[index, "class_id"]),
           int(mktime_result_2.loc[index, "class_id"]),
           int(mktime_result_3.loc[index, "class_id"]),
           ]
    rf = results.copy()
    results = list(filter((-1).__ne__, results))
    # results=np.delete(results,(results==-1).argmax())
    if len(set(results)) == 1:
        k += 1
    else:
        print(results)
        dc = {i:results.count(i) for i in set(results)}
        dc = {k: v for k, v in sorted(dc.items(), key=lambda item: -item[1])}
        ls = dc.values()
        if len(ls)>0:
            print(list(ls)[0])
        else:
            print(results)
            
            break
        # result["class_id"] = result['colummn1'].map(mapped_encoder)

        c += 1
# result.to_csv("./result/best_with_test_mod_mktime_hash.csv", index=0)
print(c)
# print(another_nn_result.shape)
print(k)