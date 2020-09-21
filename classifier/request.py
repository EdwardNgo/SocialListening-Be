import requests
import json
import re


def get_sentiment(comment, url='https://sa-api-1231.herokuapp.com/api'):
    data = [comment]
    mapping = {"0": "__lb__negative",
               "1": "__lb__neutral", "2": "__lb__positive"}
    j_data = json.dumps(data)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data=j_data, headers=headers)
    digit = re.search("\d", r.text)
    return mapping[digit.group(0)]

def get_sentiment2(comment,url = 'https://sa-api-1231.herokuapp.com/my-route?text='):
    # data = [comment]
    mapping = {"0": "__lb__negative",
               "1": "__lb__neutral", "2": "__lb__positive"}
    # j_data = json.dumps(data)
    # headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.get(url+comment)
    digit = re.search("\d", r.text)
    print(r.text)
    return mapping[digit.group(0)]
if __name__ == '__main__':
    test = "Không ra phiên bản màu trắng à"
    sentiment = get_sentiment2(test)
    print(sentiment)
