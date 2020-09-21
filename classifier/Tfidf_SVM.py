from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
from sklearn.svm import LinearSVC, SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV
import sklearn.metrics as metrics
import pickle
from build_model import preprocessing as pre
encoder = preprocessing.LabelEncoder()

sentiment = pd.read_csv("../data_preprocessed/sentiment.csv", encoding="utf-8")
encoder.fit(sentiment["sentiment"])
X = sentiment["text"].fillna(' ')
y = encoder.transform(sentiment["sentiment"])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

tfidf = TfidfVectorizer(min_df=0.05, max_df=0.9, sublinear_tf=True,
                        norm='l2', encoding='utf-8', ngram_range=(1, 2))

# # params_grid = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
# #                 'C': [1, 10, 100, 1000]},
# #                {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
# # svm_model = GridSearchCV(SVC(), params_grid, cv=5)

svm_model = SVC()
clf = Pipeline([('vect', tfidf),
                ('clf', svm_model)])
clf.fit(X_train, y_train)
classifiers = [
            # MultinomialNB(),
            # DecisionTreeClassifier(),
            # LogisticRegression(),
            # SGDClassifier(),
            LinearSVC(fit_intercept = True,multi_class='crammer_singer', C=1),
        ]
for classifier in classifiers:
    steps = []
    steps.append(('CountVectorizer', CountVectorizer(ngram_range=(1,5),max_df=0.5, min_df=5)))
    steps.append(('tfidf', TfidfTransformer(use_idf=False, sublinear_tf = True,norm='l2',smooth_idf=True)))
    steps.append(('classifier', classifier))
    clf = Pipeline(steps)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    report1 = metrics.classification_report(y_test, y_pred, labels=[1,0,2], digits=3)
print(report1)

# # # Now apply those above metrics to evaluate your model
# Your code here
# predictions = clf.predict(X_test)
# print('accuracy:', accuracy_score(y_test, predictions))
# print('confusion matrix:\n', confusion_matrix(y_test, predictions))
# print('classification report:\n', classification_report(y_test, predictions))

pickle.dump(clf, open('model/Tfidf.pkl', 'wb'))
with open('Tfidf.pkl', 'rb') as model:
    reload_model = pickle.load(model)

while True:
    text = input()
    text = [pre(text)]
    res = reload_model.predict(text)
    print(res)
