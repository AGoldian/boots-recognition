import pandas as pd
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from sklearn.cluster import KMeans

ROOT_DIR = r'data/images/'

def read_image(root_dir):
    ids = []
    data =[]
    for filename in os.scandir(root_dir):
        filename = filename.name
        if filename.endswith('.jpg'):
            img = cv2.imread(root_dir + filename)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img = cv2.resize(img, dsize=(128, 128))
            data.append(img)
            ids.append(root_dir + filename)

    return np.array(data), ids


def divide_clusters(root_dir=ROOT_DIR, num_clusters=3, mode='cpu'):
    dataframe, ids = read_image(root_dir)
    dataframe = dataframe.reshape(-1, 128*128)
    kmean = KMeans(n_clusters=num_clusters)
    cluster = kmean.fit_predict(dataframe)

    output = pd.DataFrame({'id': ids, 'cluster': cluster})

    return output


def plot_images(dataframe, cluster, num_images=10):
    """dataframe must have columns:
        id - path_to_image
        cluster - № cluster"""
    images = dataframe[dataframe['cluster'] == cluster]['id']
    cols = num_images // 5 + 1
    if num_images % 5 == 0:
        cols = num_images // 5
    
    fig, axs = plt.subplots(cols, 5, figsize=(15, 10))
    for i in range(num_images):
        image = cv2.imread(images.iloc[i]) 
        image = cv2.resize(image, dsize=(128, 128))
        try:
            ax = axs[i // 5, i % 5]
        except IndexError:
            ax = axs[i % 5]
        ax.imshow(image)
        ax.axis('off')



# from libKMCUDA import kmeans_cuda

if __name__ == '__main__':
    df = divide_clusters()
    plot_images(df, cluster=1)