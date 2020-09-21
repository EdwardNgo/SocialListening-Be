import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np
from pyvi import ViTokenizer
# import crawler


def prepare_data(filepath):
    with open(filepath, "r") as f:
        f = json.load(f)
    data = []
    listJson = []
    for item in f:
        text = []
        for content in item["crawled_cmts"]:
            text.append(content["text"])
        data.append(text)
    return data


def clustering(corpus):
    corpus_tokenize = [ViTokenizer.tokenize(data) for data in corpus]
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(corpus_tokenize)

    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans = kmeans.fit(X)

    print("K-Means Clustering\n")
    for j in range(n_clusters):
        print("Cụm", j + 1)
        idx = np.where(kmeans.labels_ == j)[0]
        for idex in idx:
            print(corpus[idex])


if __name__ == "__main__":
    # corpus = data[1]
    # clustering(corpus)
    vs_data = prepare_data("db/groupsvatvostudio.json")
    flatten_list = [j for sub in vs_data for j in sub]
    # print(flatten_list)
    with open("./test.txt", "w") as wf:
        for text in flatten_list:
            wf.write(text + "\n")
