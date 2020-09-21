import requests
import json
import re


def post_crawl(fanpage, url='https://fb-crawl-app.herokuapp.com/api/post'):
    j_data = json.dumps(fanpage)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    print(j_data)
    print(type(j_data))
    r = requests.post(url, data=j_data, headers=headers)
    return r, r.text


if __name__ == "__main__":
    # _, test = fanpage_crawl("https://www.facebook.com/VinBigdata/posts/164325381940910")
    # print(test)
    post_crawl("https://www.facebook.com/permalink.php?story_fbid=102575158255235&id=102573281588756",
               "https://92546467fa0e.ngrok.io/api/post")
