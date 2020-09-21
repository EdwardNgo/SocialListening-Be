import sys
sys.path.append('../')

from classifier import preprocessing, preprocessing_2
import json
import traceback
import fasttext as ft
from flask import Flask, request, render_template
import re


def rev_dict(dict):
    _dict = {}
    for key, val in dict.items():
        _dict[val] = key
    return _dict


app = Flask(__name__)


class CodeIdentify:
    def __init__(self,
                 model_file='../classifier/model/ft.li.1701.bin',
                 code2namefile='sentiment_code.json'):
        self.model = ft.load_model(model_file)
        self.code2name = rev_dict(
            json.load(open(code2namefile, encoding='utf8')))
        # self.tp = CodePreprocess()

    def pred(self, txt):
        # txt = self.tp.preprocessing(txt)
        res = self.model.predict(txt)
        label = res[0][0]
        print(label)
        score = round(res[1][0], 2)
        sentiment = self.code2name[label[6:]].upper()
        return sentiment, score


ci = CodeIdentify()


@app.route('/')
def ping():
    return 'ok'


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            review = request.form['review']
            review = preprocessing(review)
            # if not review or len(review) <= 20:
            #     return render_template('index.html',error='Please enter more than 20 characters')
            sentiment, score = ci.pred(review)
            return render_template('index.html', sentiment=sentiment, score=score, review=review)
        except:
            traceback.print_exc()
            return render_template('index.html', error='Unknown error has occurred, please try again!')


if __name__ == '__main__':
    app.run(debug=True)
