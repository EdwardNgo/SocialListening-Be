from helium import kill_browser
import re
import requests
import json
import sys
sys.path.append('../')

InsertPost = """mutation MyMutation($post_id: String, $like: String, $page_id: String, $comment: Int,       $content: String, $share: Int, $created_at: String) {
        insert_posts(objects: {
            post_id: $post_id,
            content: $content,
            like: $like,
            comment: $comment,
            share: $share,
            created_at: $created_at,
            page_id: $page_id
            }) {
            __typename
        }
        }"""

InsertPage = """mutation UpdatePage($id: Int, $name: String) {
        insert_pages(objects: {
            id: $id,
            name: $name
        }) {
        __typename
        }
        }
        """
InsertComment = """mutation MyMutation($content: String, $created_at: String, $post_id:String, $comment_id: String,$label:String,$user_url:String,$user_name: String, $user_avatar:String) {
  insert_comments(objects: {
    content: $content,
    created_at: $created_at,
    post_id: $post_id,
    comment_id: $comment_id,
    label:$label,
    user_name: $user_name,
    user_avatar: $user_avatar
    }) {
    __typename
  }
}"""
UpdatePost = """  mutation MyMutation($postId: String, $like: String, $comment: Int, $pos: Int ,$img_link: String) {
  update_posts(where: {post_id: {_eq: $postId}}, _set: {neg_total: $neg, neu_total: $neu, pos_total: $pos, img_link: $img_link}) {
    returning {
      post_id
    }
  }
} """


UpdatePostSentiment = """mutation MyMutation($postId: String, $neg: Int, $neu: Int, $pos: Int ,$img_link: String) {
  update_posts(where: {post_id: {_eq: $postId}}, _set: {neg_total: $neg, neu_total: $neu, pos_total: $pos, img_link: $img_link}) {
    returning {
      post_id
    }
  }
}

"""


def stop_and_save(fileName, listPosts):
    print("Save crawled data...")
    with open(fileName, "w", encoding="utf-8") as file:
        json.dump(listPosts, file, ensure_ascii=False, indent=4)
    kill_browser()


def graphQl_save(client, query, variables):
    data = client.execute(query=query, variables=variables)
    print(data)


def get_sentiment(comment,url = 'https://sa-api-1231.herokuapp.com/my-route?text='):
    # data = [comment]
    mapping = {"0": "__lb__negative",
               "1": "__lb__neutral", "2": "__lb__positive"}
    # j_data = json.dumps(data)
    # headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.get(url+comment)
    digit = re.search("\d", r.text)
    return mapping[digit.group(0)]  



COMMENTABLE_SELECTOR_GROUP = 'div._5pcr.userContentWrapper' + " .commentable_item"
COMMENTABLE_SELECTOR_PAGE = '[class="_427x"] .userContentWrapper' + \
    " .commentable_item"

if __name__ == "__main__":
  test = "vui vl"
  res = get_sentiment(test)
  print(res)