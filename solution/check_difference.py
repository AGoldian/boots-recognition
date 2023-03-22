import pandas as pd

first_df = pd.read_csv(r"./result/tmp_pos_with_nn_another_prioritet_without_ebay.csv")
second_df = pd.read_csv(r"./result/tmp_pos_with_nn.csv")

j = 0
for idx, col in second_df.iterrows():
    if first_df.loc[idx, "class_id"] != second_df.loc[idx, "class_id"]:
        print(col.image, col.class_id)
        j += 1
print(j)
