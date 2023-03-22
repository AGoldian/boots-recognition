import pandas as pd
import numpy as np
from collections import defaultdict


def advanced_prediction():
    result = pd.read_csv("./result/tmp_nn_result_old.csv", index_col=0)

    def get_class_id(row):
        class_id = eval(row['class_id'])[0] if isinstance(row['class_id'], str) else row['class_id'][1]
        return class_id

    result['new_class_id'] = result.apply(get_class_id, axis=1)
    result.drop(["dummy_labels", "smth", "file_path"], axis=1, inplace=True)
    result.to_csv("./result/tmp_nn_result.csv", index=False)


def form_final_prediction():
    is_use_parsing = False
    is_from_final = False

    result = pd.read_csv("./result/tmp_nn_result.csv", index_col=0)
    map_df = pd.read_csv("./result/map.csv", index_col=0)
    parsed = pd.read_csv('./result/parse_result_21344.csv')
    orig_df = pd.read_csv(r'./data/test.csv')

    tmp_df = pd.DataFrame()
    tmp_df['class_id'] = map_df['class_id']
    tmp_df['individual_id'] = map_df['individual_id']

    res = [item for item in tmp_df.to_dict('split')["data"]]
    mapped_encoder = defaultdict()

    for m in res:
        mapped_encoder[m[1]] = (m[0])
    mapped_encoder[-1] = -1

    result["class_id"] = result['colummn1'].map(mapped_encoder)

    orig_df["tmp_res"] = orig_df['image'].map(result.set_index('image')['class_id'])
    if is_use_parsing:
        orig_df['class_id'] = orig_df['tmp_res'].fillna(parsed['class_id'])
    else:
        # possible version when NN predict full dataset
        orig_df['class_id'] = orig_df['tmp_res'].fillna(-1)

    orig_df["class_id"] = orig_df["class_id"].astype("int64")
    orig_df.drop("tmp_res", axis=1, inplace=True)
    columnsTitles = ['class_id', 'image']
    orig_df = orig_df.reindex(columns=columnsTitles)

    if not is_from_final:
        one_of_best_prediction = pd.read_csv("./result/test_my109.csv")
        mask1 = (one_of_best_prediction['class_id'] == -1) & (orig_df['class_id'] != -1)
        mask2 = (one_of_best_prediction['class_id'] != -1) & (orig_df['class_id'] == -1)

        orig_df.loc[mask1, 'class_id'] = -1
        orig_df.loc[mask2, 'class_id'] = one_of_best_prediction.loc[mask2, 'class_id']
        # No action needed for mask3, as we are not modifying any value

    orig_df.to_csv("./result/final_result.csv", index=False)
    print(orig_df[orig_df.class_id == -1].shape)


form_final_prediction()
