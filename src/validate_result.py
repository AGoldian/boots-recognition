import pandas as pd

result_misc = pd.read_csv(r"D:\Kaggle\CleanCodeCup\2023\2023\everything_ebay\all_csv\misc12.csv", index_col=False)
result_avg = pd.read_csv(r"D:\Kaggle\CleanCodeCup\2023\2023\everything_ebay\all_csv\temp_result_fin_avg18.csv", index_col=False)

neural_predict = pd.read_csv(r"C:\Users\Sergey\PycharmProjects\RZD_Digital\test_my109.csv", index_col=False)
# neural_predict = pd.read_csv(r"D:\Kaggle\CleanCodeCup\2023\2023\test_mod_wdup.csv", index_col=False)
classes = pd.read_csv(r"C:\Users\Sergey\PycharmProjects\RZD_Digital\classes.csv", index_col=False)

hashes = pd.read_csv(r"C:\Users\Sergey\PycharmProjects\RZD_Digital\file_hashes_avg_24.csv")
test_with_label = pd.read_csv(r'D:\Kaggle\CleanCodeCup\2023\2023\test_with_label.csv')
test_with_label.drop('Unnamed: 0',axis=1,inplace=True)
test_with_label.drop('Unnamed: 0.1',axis=1,inplace=True)

data_dict_misc = result_misc.to_dict('list')
data_dict_avg = result_avg.to_dict('list')
count = 0
correct = 0
total_size = test_with_label.shape[0]
total_unlabeled = test_with_label[test_with_label.label == -1].shape[0]

for (image, hashs) in zip(hashes['Filename'], hashes['Avg_Hash']):
    found = False
    for i in range((result_misc.shape[0])):
        if hashs in data_dict_misc['hash'][i]:
            # if len(test_with_label.label[test_with_label.hash==hash]) > 0:
            #     if test_with_label.label[test_with_label.hash==hash].values[0] == -1:
            #         test_with_label.label[test_with_label.hash==hash] = data_dict['idx'][i]
            # print(image, i)
            if len(test_with_label[test_with_label.image == image]) > 0:
                if test_with_label.label[test_with_label.image == image].values[0] == -1:
                    count += 1
                    gt = classes.id[classes.model == data_dict_misc['brand'][i]].values[0]
                    test_with_label.label[test_with_label.image == image] = gt
                    nn = neural_predict.class_id[neural_predict.image == image].values[0]
                    if gt != nn:
                        correct += 1
                    print(image, "GT:", gt, "NN:", nn)
                    found = True
    if not found:
        for i in range((result_avg.shape[0])):
            if hashs in data_dict_avg['hash'][i]:
                if len(test_with_label[test_with_label.image == image]) > 0:
                    if test_with_label.label[test_with_label.image == image].values[0] == -1:
                        count += 1
                        gt = classes.id[classes.model == data_dict_avg['brand'][i]].values[0]
                        test_with_label.label[test_with_label.image == image] = gt
                        nn = neural_predict.class_id[neural_predict.image == image].values[0]
                        if gt != nn:
                            correct += 1
                        print(image, "GT:", gt, "NN:", nn)
                        found = True


print("Found total:", count)
print("Found unique:", correct, "Percentage:", correct / total_unlabeled * 100, "%")
print("Total size:", total_size)
print("Before total unlabeled:", total_unlabeled)
print("After total unlabeled:", test_with_label[test_with_label.label == -1].shape[0])

# save to csv neural_predict