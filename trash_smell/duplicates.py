import glob
import hashlib

hash_dict = dict()
for file in glob.glob(r"D:\Kaggle\CleanCodeCup\2023\2023\images\images\*.jpg"):
    with open(file, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
        file_name = file.split("\\")[-1]
        hash_dict[file_name] = file_hash
import csv

# Open a file for writing
with open('file_hashes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Filename', 'MD5_Hash'])

    # Write each row of data
    for file_name, md5_hash in hash_dict.items():
        writer.writerow([file_name, md5_hash])