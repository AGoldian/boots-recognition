from collections import Counter

import pandas as pd
tr = pd.read_csv(r"data/mktime_train.csv")
ts = pd.read_csv(r"data/mktime_test.csv")
tr.head()

count = 0
for index, col in ts.iterrows():
    class_id = (tr[tr.date == col.date]).class_id.to_list()
    # print(sorted(class_id))
    if 0 < len(set(class_id)) <= 3:
        if len(set(class_id)) == 1:
            ts.loc[index, "class_id_1"] = list(set(class_id))[0]
        elif len(set((class_id))) == 2:
            ts.loc[index, "class_id_1"] = list(set(class_id))[0]
            ts.loc[index, "class_id_2"] = list(set(class_id))[1]
        else:
            ts.loc[index, "class_id_1"] = list(set(class_id))[0]
            ts.loc[index, "class_id_2"] = list(set(class_id))[1]
            ts.loc[index, "class_id_3"] = list(set(class_id))[2]

    else:
        ts.loc[index, "class_id_1"] = -1
        ts.loc[index, "class_id_2"] = -1
        ts.loc[index, "class_id_3"] = -1
        count += 1

orig_df = pd.read_csv(r"./data/test_mod_wdup_plus_avg_32.csv",
                      index_col=0)
orig_df["class_id"] = orig_df['image'].map(ts.set_index('image')['class_id_3'])
orig_df["class_id"] = orig_df["class_id"].fillna(-1)
orig_df["class_id"] = orig_df["class_id"].astype("int64")
orig_df.to_csv("filled_true_3_mktime.csv", index=False)

orig_df["class_id"] = orig_df['image'].map(ts.set_index('image')['class_id_2'])
orig_df["class_id"] = orig_df["class_id"].fillna(-1)
orig_df["class_id"] = orig_df["class_id"].astype("int64")
orig_df.to_csv("filled_true_2_mktime.csv", index=False)

orig_df["class_id"] = orig_df['image'].map(ts.set_index('image')['class_id_1'])
orig_df["class_id"] = orig_df["class_id"].fillna(-1)
orig_df["class_id"] = orig_df["class_id"].astype("int64")
orig_df.to_csv("filled_true_1_mktime.csv", index=False)
