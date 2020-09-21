from sklearn.model_selection import train_test_split
import os
from build_model import preprocessing, preprocessing_2
import pandas as pd


def save_fasttext_format(X_data, y_data, output_file, prefix="__lb__"):
    with open(output_file, "w", encoding="utf-8") as fp:
        for x, y in zip(X_data, y_data):
            fp.write(prefix + y + " " + x + "\n")


def save_csv_format(csvpath):
    file_path = os.listdir('/home/viethoang/DevC_Project/data')
    data_dict = {"text": [], "sentiment": []}
    for path in file_path:
        with open('/home/viethoang/DevC_Project/data/'+path, 'r') as f:
            lines = f.read().split("\n")
            for line in lines:
                data_dict["text"].append(preprocessing(line))
                data_dict["sentiment"].append(path.split('.')[0])
    df = pd.DataFrame(data_dict)
    df.to_csv(csvpath)
    # return data_dict


Xs = []
ys = []

data_dir = os.path.dirname(os.path.realpath(os.getcwd()))
data_dir_raw = os.path.join(data_dir, "data")
data_dir_final = os.path.join(data_dir, "data_preprocessed")
for file in os.listdir(data_dir_raw):
    if file.endswith(".txt"):
        label = file[:-4]
        for line in (
            open(os.path.join(data_dir_raw, file),
                 encoding="utf-8").read().split("\n")
        ):
            Xs.append(preprocessing(line.strip()))
            ys.append(label)

X_train, X_test, y_train, y_test = train_test_split(
    Xs, ys, test_size=0.2, random_state=42
)
save_csv_format("../data_preprocessed/sentiment.csv")
save_fasttext_format(X_train, y_train, os.path.join(data_dir_final, "train.txt"))
save_fasttext_format(X_test, y_test, os.path.join(data_dir_final, "test.txt"))
