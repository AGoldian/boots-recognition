import cv2
from sklearn.cluster import KMeans
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.decomposition import PCA

def visualize():
    import matplotlib.pyplot as plt
    x1 =  np.array([[1, 2]])
    x2 =  np.array([[-2, -3]])
    x3 =  np.array([[-4, -5]])
    x4 =  np.array([[6, 5]])
    x11 =  cv2.cvtColor(cv2.resize(cv2.imread(r"E:\gnd1.jpg"),(5,5)),cv2.COLOR_BGR2GRAY).ravel()
    x22 =  cv2.cvtColor(cv2.resize(cv2.imread(r"E:\gnd2.jpg"),(5,5)),cv2.COLOR_BGR2GRAY).ravel()
    x21 =  cv2.cvtColor(cv2.resize(cv2.imread(r"C:\Users\Sergey\Desktop\abc.jpg"),(5,5)),cv2.COLOR_BGR2GRAY).ravel()
    print(x11.shape)
    data = np.concatenate((x1,x2,x3,x4),axis=0)
    data = np.asarray([x11,x21,x22])
#     data : ndarray of shape (n_samples, n_features)
    # https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html
    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans = KMeans(init="k-means++", n_clusters=2, n_init=4)
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = 0.02  # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(
        Z,
        interpolation="nearest",
        extent=(xx.min(), xx.max(), yy.min(), yy.max()),
        cmap=plt.cm.Paired,
        aspect="auto",
        origin="lower",
    )

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], "k.", markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(
        centroids[:, 0],
        centroids[:, 1],
        marker="x",
        s=269,
        linewidths=3,
        color="w",
        zorder=10,
    )
    plt.title(
        "K-means clustering on the digits dataset (PCA-reduced data)\n"
        "Centroids are marked with white cross"
    )
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()
from sklearn.cluster import MiniBatchKMeans

def work():
    x11 =  cv2.cvtColor(cv2.imread("E:\gnd1.jpg"),cv2.COLOR_BGR2GRAY).ravel()
    x21 =  cv2.cvtColor(cv2.imread("E:\gnd.png"),cv2.COLOR_BGR2GRAY).ravel()
    tt = [x11,x21]
    kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=300, random_state=0).fit(np.asarray(tt))
    # print(kmeans.cluster_centers_)

    # Get the cluster labels
    print(kmeans.labels_)
    print(x21.shape)

    Z = kmeans.predict(np.asarray([x11,x21]))
    print(Z)

work()
# visualize()