from flask import Flask, request, jsonify
from crawler import Crawler
from libs import CMTS
from libs import loader as loader

app = Flask(__name__)


@app.route('/api/post',methods = ['POST'])
def fanpage():
    # group = ''
    # fanpage_name = request.get_json()
    post_name = request.get_json()
    crawler = Crawler(CMTS.ALL_COMMENTS,3,3)
    crawler.crawl_post(post_name)
    return "Crawling ......"



if __name__ == '__main__':
    app.run(debug=True)
    