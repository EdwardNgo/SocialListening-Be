
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import json
from build_model import preprocessing

app = Flask(__name__)


@app.route('/api/', methods=['POST'])
def makecalc():
    modelfile = 'model/Tfidf.pkl'
    model = p.load(open(modelfile, 'rb'))
    data = request.get_json()
    prediction = np.array2string(model.predict(preprocessing(data))

    return jsonify(prediction)

@app.route('/my-route',methods = ['GET', 'POST'])
def my_route():
#   page = request.args.get('page', default = 1, type = int)
    modelfile = 'model/Tfidf.pkl'
    model = p.load(open(modelfile, 'rb'))
    text = request.args.get('text', default = '*', type = str)
    prediction = np.array2string(model.predict([preprocessing(text)]))
    return jsonify(prediction)

if __name__ == '__main__':
    # modelfile = 'model/Tfidf.pkl'
    # model = p.load(open(modelfile, 'rb'))
    app.run(debug=True, host='0.0.0.0')