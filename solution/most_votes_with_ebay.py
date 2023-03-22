import pandas as pd
import numpy as np
from collections import defaultdict

nn_result = pd.read_csv("./result/best_hash.csv")
ebay_result = pd.read_csv("./result/parse_result_20301.csv")
mktime_result_1 = pd.read_csv(r"./data/filled_true_1_mktime.csv")
mktime_result_2 = pd.read_csv(r"./data/filled_true_2_mktime.csv")
mktime_result_3 = pd.read_csv(r"./data/filled_true_3_mktime.csv")
classes = pd.read_csv(r"./data/classes.csv")
c = 0
k = 0

for index, col in nn_result.iterrows():
    results = [int(nn_result.loc[index, "class_id"]),
               int(ebay_result.loc[index, "class_id"]),
               int(mktime_result_1.loc[index, "class_id"]),
               int(mktime_result_2.loc[index, "class_id"]),
               int(mktime_result_3.loc[index, "class_id"]),
               # int(another_nn_result.loc[index, "class_id"]),
               ]
    rf = results.copy()
    results = list(filter((-1).__ne__, results))
    if len(set(results)) == 1:
        k += 1
    else:
        dc = {i: results.count(i) for i in set(results)}
        dc = {k: v for k, v in sorted(dc.items(), key=lambda item: -item[1])}
        ls = dc.values()
        if len(list(ls)) > 0:
            ks = dc.keys()
            if list(ls)[0] > 1:
                nn_result.loc[index, "class_id"] = list(ks)[0]
            else:
                print(col["image"])
                print(rf)
                list_of_int = list(ks)
                brands = []
                for jg in range(0, len(list_of_int)):
                    brands.append(classes[classes.id == int(list_of_int[jg])].brand.values[0])
                print(results)
                brands_count = {i: brands.count(i) for i in set(brands)}
                brands_count = {k: v for k, v in sorted(brands_count.items(), key=lambda item: -item[1])}
                top_val = list(brands_count.values())[0]
                top_key = list(brands_count.keys())[0]
                if top_val == 1:
                    if mktime_result_1.loc[index, "class_id"] != -1:
                        nn_result.loc[index, "class_id"] = mktime_result_1.loc[index, "class_id"]
                    # elif ebay_result.loc[index, "class_id"] != -1:
                    #     nn_result.loc[index, "class_id"] = ebay_result.loc[index, "class_id"]
                    elif mktime_result_2.loc[index, "class_id"] != -1:
                        nn_result.loc[index, "class_id"] = mktime_result_2.loc[index, "class_id"]
                    elif mktime_result_3.loc[index, "class_id"] != -1:
                        nn_result.loc[index, "class_id"] = mktime_result_3.loc[index, "class_id"]
                elif top_val >=3:
                    for val in range(len(results)):
                        if (mktime_result_1.loc[index, "class_id"] != -1) and brands[val] == top_key:
                            nn_result.loc[index, "class_id"] = mktime_result_1.loc[index, "class_id"]
                            break
                        # elif ebay_result.loc[index, "class_id"] != -1 and brands[val] == top_key:
                        #     nn_result.loc[index, "class_id"] = ebay_result.loc[index, "class_id"]
                        #     break
                        elif mktime_result_2.loc[index, "class_id"] != -1 and brands[val] == top_key:
                            nn_result.loc[index, "class_id"] = mktime_result_2.loc[index, "class_id"]
                            break
                        elif mktime_result_3.loc[index, "class_id"] != -1 and brands[val] == top_key:
                            nn_result.loc[index, "class_id"] = mktime_result_3.loc[index, "class_id"]
                            break
                else:
                    if len(list(brands_count.values())) == 1:
                        if mktime_result_1.loc[index, "class_id"] != -1:
                            nn_result.loc[index, "class_id"] = mktime_result_1.loc[index, "class_id"]
                        # elif ebay_result.loc[index, "class_id"] != -1:
                        #     nn_result.loc[index, "class_id"] = ebay_result.loc[index, "class_id"]
                        elif mktime_result_2.loc[index, "class_id"] != -1:
                            nn_result.loc[index, "class_id"] = mktime_result_2.loc[index, "class_id"]
                        elif mktime_result_3.loc[index, "class_id"] != -1:
                            nn_result.loc[index, "class_id"] = mktime_result_3.loc[index, "class_id"]
                    else:
                        if top_val == 2 and list(brands_count.values())[1] == 2:
                            if mktime_result_1.loc[index, "class_id"] != -1:
                                nn_result.loc[index, "class_id"] = mktime_result_1.loc[index, "class_id"]
                            # elif ebay_result.loc[index, "class_id"] != -1:
                            #     nn_result.loc[index, "class_id"] = ebay_result.loc[index, "class_id"]
                            elif mktime_result_2.loc[index, "class_id"] != -1:
                                nn_result.loc[index, "class_id"] = mktime_result_2.loc[index, "class_id"]
                            elif mktime_result_3.loc[index, "class_id"] != -1:
                                nn_result.loc[index, "class_id"] = mktime_result_3.loc[index, "class_id"]
                        else: # 2 1 cases
                            for val in range(len(results)):
                                if (mktime_result_1.loc[index, "class_id"] != -1) and brands[val] == top_key:
                                    nn_result.loc[index, "class_id"] = mktime_result_1.loc[index, "class_id"]
                                    break
                                # elif ebay_result.loc[index, "class_id"] != -1 and brands[val] == top_key:
                                #     nn_result.loc[index, "class_id"] = ebay_result.loc[index, "class_id"]
                                #     break
                                elif mktime_result_2.loc[index, "class_id"] != -1 and brands[val] == top_key:
                                    nn_result.loc[index, "class_id"] = mktime_result_2.loc[index, "class_id"]
                                    break
                                elif mktime_result_3.loc[index, "class_id"] != -1 and brands[val] == top_key:
                                    nn_result.loc[index, "class_id"] = mktime_result_3.loc[index, "class_id"]
                                    break

                # print(list(brands_count.keys())[0])
                # print(  (results == str(list(brands_count.keys())[0])))
                # print(np.argwhere(results == list(brands_count.keys())[0]))
                # print(brands_count)
                # print()
                # if mktime_result_1.loc[index, "class_id"] != -1:
                #     nn_result.loc[index, "class_id"] = ebay_result.loc[index, "class_id"]
                # else:
        else:
            nn_result.loc[index, "class_id"] = -1
            print(results)

        c += 1



nn_result.to_csv("./result/tmp_pos_with_nn_another_prioritet.csv", index=0)
print(c)
# print(another_nn_result.shape)
print(k)
