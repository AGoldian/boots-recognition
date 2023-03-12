import glob
import hashlib
import imagehash
from PIL import Image
import pandas as pd
from tqdm import tqdm

hash_size = 32

filename = []
md5_hash = []
avg_hash = []

for file in tqdm(glob.glob(r"W:\Users\Goldian\Desktop\data\images\images\*.jpg")):
    file_name = file.split("\\")[-1]

    with open(file, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
        
    with Image.open(file) as img:
        temp_hash = imagehash.average_hash(img, hash_size)


    filename.append(file_name)
    md5_hash.append(file_hash)
    avg_hash.append(temp_hash)


pd.DataFrame({'image': filename, 'md5': md5_hash, 'avg': avg_hash}).to_csv('beda.csv', index=False)