import imagehash
import glob
from PIL import Image
import pandas as pd

hash_size = 24

filename = []
avg_hash = []

for file in glob.glob("./images/*.jpg"):
    with Image.open(file) as img:
        temp_hash = imagehash.average_hash(img, hash_size)

    filename.append(file.split("\\")[-1])
    avg_hash.append(temp_hash)

pd.DataFrame({'image': filename, 'avg': avg_hash}).to_csv('./data/allhash.csv', index=False)