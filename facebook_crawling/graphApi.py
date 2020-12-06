import facebook
import json
from libs import stop_and_save, COMMENTABLE_SELECTOR_PAGE, COMMENTABLE_SELECTOR_GROUP, graphQl_save, get_sentiment
from libs import InsertPost_1,access_token,bulkInsertPost,dateToSecond
from python_graphql_client import GraphqlClient
import requests
import re
from collections import defaultdict

class ApiCrawler:
    def __init__(self,access_token):
        self.access_token = access_token
        self.graph = facebook.GraphAPI(access_token = access_token,version = "2.12")
        
    def getSinglePost(self,post_id):
        post = self.graph.get_object(id=post_id, fields='message,comments,from')
        return post
    
    def getPostsGroup(self,group_id):
        group_post_data = self.graph.get_object(id = group_id,fields='posts,feed{full_picture,created_time,reactions,shares,comments,from,message}')
        detailed = []

        return group_post_data
    
    def getPostsPage(self,url):
        page_id = self.getPageId(url)
        print(page_id)
        page_post_data = self.graph.get_object(id = page_id,fields="""posts.limit(5){full_picture,created_time,message,comments.limit(200){message,created_time}}""")
        posts = page_post_data['posts']['data']
        cmts = []
        total_post = []
        for post in posts:
            post_dict = {'img_link':'','created_at':'','content':'','post_id':'','page_id':''}
            post_dict['page_id'] = post['id'].split("_")[0]
            post_dict['post_id'] = post['id'].split("_")[1]
            try:
                post_dict['img_link'] = post['full_picture']
            except:
                post_dict['img_link'] = ''
            post_dict['created_at'] = dateToSecond(post['created_time'])
            post_dict['content'] = post['message']
            total_post.append(post_dict)
            for cmt in post['comments']['data']:
                cmt_dict = {'content':'','created_at':'','post_id':'','comment_id':'','label':''}
                cmt_dict['content'] = cmt['message']
                cmt_dict['created_at'] = dateToSecond(cmt['created_time'])
                cmt_dict['post_id'] = post_dict['post_id']
                cmt_dict['content'] = cmt['message']
                cmt_dict['comment_id'] = cmt['id'].split("_")[1]
                cmts.append(cmt_dict)
                

        return total_post,cmts,posts
    
    def getPageId(self,url):
        pattern = "\"pageID\":.\d+"
        try:
            response = requests.get(url)
            html_raw = response.text
            page_id = re.search(pattern,html_raw)
            page_id = page_id.group()
            page_id = page_id.split(":\"")[1]
        except Exception as e:
            page_id = ""
            print(e)
        return page_id
        
if __name__ == "__main__":
    # posts,detailed = getMultiplePosts('905871509607608')
    # # print(posts)
    # with open("test.json","w") as jf:
    #     json.dump(detailed,jf,indent= 4,ensure_ascii = False)
    # print(detailed)
    url = 'https://eager-fox-36.hasura.app/v1/graphql'
    client = GraphqlClient(url)
    testCrawler = ApiCrawler(access_token)
    # private_group_posts = testCrawler.getPostsGroup('929563144068596')
    # print(private_group_posts)
    fanpage_posts,cmts,posts = testCrawler.getPostsPage('https://www.facebook.com/truongnguoita.vn/')
    # print(fanpage_posts)
    # test={'objects':''}
    # test['objects'] = fanpage_posts
    # print(cmts)
    graphQl_save(client,bulkInsertPost,fanpage_posts)
