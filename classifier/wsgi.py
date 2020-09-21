from api import app

if __name__ == '__main__':
#     modelfile = 'model/Tfidf.pkl'
#     model = p.load(open(modelfile, 'rb'))
    app.run(debug=True, host='0.0.0.0')
