import glob
import hashlib
import imagehash
from PIL import Image

hash_dict = dict()
hash_size = 48
i=0
for file in glob.glob(r"D:\Kaggle\CleanCodeCup\2023\2023\images\images\*.jpg"):
    with Image.open(file) as img:
        temp_hash = imagehash.average_hash(img, hash_size)

        file_name = file.split("\\")[-1]
        hash_dict[file_name] = temp_hash
    if i%100 == 0:
        print(i)
    i+=1
import csv

# Open a file for writing
with open('file_hashes_avg_48.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Filename', 'Avg_Hash'])

    # Write each row of data
    for file_name, md5_hash in hash_dict.items():
        writer.writerow([file_name, md5_hash])