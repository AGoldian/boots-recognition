IS_TRAIN = False # inference

# train based on : https://www.kaggle.com/code/vladvdv/simple-vanilla-pytorch-train-notebook-gem-pooling?scriptVersionId=92639607
# inference based on : https://www.kaggle.com/code/vladvdv/simple-vanilla-pytorch-inference-gem-pooling/notebook?scriptVersionId=92716824
if IS_TRAIN:
    # PREPROCESSING
    # 1) get train_mod and test_mod with manual deletion of corrupted image
    # 2) calculate average hash 24, 32 of each image to delete duplicates,
    # (file form_hash.py with 24 then 32 params) - got file allhash.csv - 24 hash
    # and when delete duplicates fill test with train label if it's possible
    print("Duplicates was dropped and hash was calculated")

    # 3) Found some correlation (res.ipynb) calculate ctime for each file
    # run first 4 cells in res.ipynb to get mktime_train.csv and mktime_test.csv -
    # - files with creation date of files
    # run python3 mktime_part.py to create files (filled_true_{1,2,3}_mktime.csv)
    print("Creation time was used and created")

    # TRAIN MODEL
    # run train.ipynb
    # Simple Vanilla Pytorch Train Notebook(GeM Pooling) taken from sorted by most votes from Kaggle competition  https://www.kaggle.com/competitions/happy-whale-and-dolphin
    # (top 10 notebook, open source, based on top 1)
    # https://www.kaggle.com/code/vladvdv/simple-vanilla-pytorch-train-notebook-gem-pooling?scriptVersionId=92639607
    print("Model was trained") # model was trained on the original data without any deletion

    # POST PROCESSING
    # run ebay parsing using average hash 24 to compare image in ebay with dataset image
    # run ebay_parsing.ipynb
    print("Ebay was parsed in folder parse_data")
    # process ebay data in folder parse_data
    print("Data was merged and file with 20301 unfilled was generated")

else:
    # INFERENCE

    # run inference.ipynb
    print("Result from NN got, writted to beda_best.csv and map_best.csv")
    # process NN result to map back and get only 1 item
    # run python3 process_nn.py
    print("Got file best_ever with prediction only neural network")

    # run simple_inference to form best_hash.csv (combined hash + neural network)
    # python3 merge_data_from_parse.py

    # merge all results
    # python3 most_votes.py
    # to get 0.773793234676996 public run without ebay files (only mktime + nn+hash)
    # return will be tmp_pos_with_nn_another_prioritet_without_ebay.csv

    # to get 0.8080541050122214 public score run most_votes_with_ebay.py
    # return will be tmp_pos_with_nn_another_prioritet.csv
    print("Done")
