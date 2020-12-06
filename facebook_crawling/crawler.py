from libs import stop_and_save, COMMENTABLE_SELECTOR_PAGE, COMMENTABLE_SELECTOR_GROUP, graphQl_save, InsertPage, InsertPost, InsertComment, UpdatePostSentiment, get_sentiment
from fasttext import load_model
from classifier import predict_results
import re
from libs import loader as loader
from libs import CMTS
import requests
from python_graphql_client import GraphqlClient
import sys
sys.path.append('../')


class Crawler:

    url = 'https://eager-fox-36.hasura.app/v1/graphql'
    client = GraphqlClient(url)

    def __init__(
        self, FILTER_CMTS_BY, VIEW_MORE_CMTS, VIEW_MORE_REPLIES
    ):

        self.FILTER_CMTS_BY = FILTER_CMTS_BY
        self.VIEW_MORE_REPLIES = VIEW_MORE_REPLIES
        self.VIEW_MORE_CMTS = VIEW_MORE_CMTS

    def get_child_attribute(self, element, selector, attr):
        try:
            element = element.find_element_by_css_selector(selector)
            return str(element.get_attribute(attr))
        except:
            return ""

    def get_comment_info(self, comment):
        cmt_url = self.get_child_attribute(comment, "a._6qw7", "href")
        # print("cmt_url: {}".format(cmt_url))

        if "&comment_id=" in cmt_url:
            cmt_id = cmt_url.split("&comment_id=")[1]
        else:
            cmt_id = (
                cmt_url.split("?")[-1]
                .replace("type=3&comment_id=", "")
                .replace("comment_id=", "")
            )
        try:
            post_id = cmt_url.split("story_fbid=")[1].split("&id=")[0]
        except:
            post_id = cmt_url.split("/")[5].split("?")[0]

        # print("post_id: {} ".format(post_id))
        # print("cmt_id: {}".format(cmt_id))
        if cmt_id == None:
            cmt_id = comment.get_attribute("data-ft").split(':"')[-1][:-2]
            user_url = user_id = user_name = "Acc clone"
        else:
            user_url = cmt_url.split("?")[0]
            user_id = user_url.split(
                "https://www.facebook.com/")[-1].replace("/", "")
            user_name = self.get_child_attribute(
                comment, "._6qw4", "innerText")

        utime = self.get_child_attribute(comment, "abbr", "data-utime")
        text = self.get_child_attribute(comment, "._3l3x ", "textContent")
        avt = self.get_child_attribute(comment, "img._3me-._3mf1.img", "src")
        return {
            "fbid": post_id,
            "id": cmt_id,
            "utime": utime,
            "user_url": user_url,
            "user_id": user_id,
            "user_name": user_name,
            "text": text,
            "avt": avt
        }

    def extract_fanpage_data(self, PAGE_URL):

        SCROLL_DOWN = 2
        loader.start(
            PAGE_URL,
            SCROLL_DOWN,
            self.FILTER_CMTS_BY,
            self.VIEW_MORE_CMTS,
            self.VIEW_MORE_REPLIES,
            COMMENTABLE_SELECTOR_PAGE
        )
        graphQl_save(Crawler.client, InsertPage, {
                     "id": 2111, "name": PAGE_URL})
        driver = loader.driver
        total = 0

        listJsonPosts = []
        listHtmlPosts = driver.find_elements_by_css_selector(
            '[class="_427x"] .userContentWrapper'
        )
        try:
            fanpage_pic = driver.find_element_by_css_selector(
                "img._6tb5.img").get_attribute('src')
        except:
            fanpage_pic = driver.find_element_by_css_selector(
                "img.scaledImageFitWidth.img").get_attribute('src')
        print("Start crawling", len(listHtmlPosts), "posts...")
        for post in listHtmlPosts:
            post_url = self.get_child_attribute(
                post, "._5pcq", "href")

            # try:
            #     post_id = re.findall("\d+", post_url)[-1]
            # except:
            #     post_id = post_url.split("/")[-1]
            utime = self.get_child_attribute(post, "abbr", "data-utime")
            post_text = self.get_child_attribute(
                post, ".userContent", "textContent")
            total_shares = self.get_child_attribute(
                post, '[data-testid="UFI2SharesCount/root"]', "innerText")
            total_cmts = self.get_child_attribute(post, "._3hg-", "innerText")
            image_url = self.get_child_attribute(
                post, "img.scaledImageFitWidth.img", "src")
            # fanpage_url = self.get_child_attribute(post, "_6tb5 img", "src")
            # print(fanpage_url)
            print(post_url)
            listJsonCmts = []
            listHtmlCmts = post.find_elements_by_css_selector("._7a9a>li")
            print(listJsonCmts)
            try:
                comment_owner = listHtmlCmts[0].find_elements_by_css_selector(
                    "._7a9b")
                post_id = self.get_comment_info(comment_owner[0])["fbid"]
            except:
                post_id = re.findall("\d+", post_url)[-1]

            print("post id: {}".format(post_id))
            num_of_cmts = len(listHtmlCmts)

            total += num_of_cmts

            listJsonReacts = []
            listHtmlReacts = post.find_elements_by_css_selector("._1n9l")

            for react in listHtmlReacts:
                react_text = react.get_attribute("aria-label")
                listJsonReacts.append(react_text)

            likes = listJsonReacts[0].split(
            )[0] if listJsonReacts != [] else "0"
            try:
                post_dict = {
                    "post_id": post_id,
                    "content": post_text,
                    "like": likes,
                    "comment": int(total_cmts.split()[0]) if total_cmts != "" else 0,
                    "share": int(total_shares.split()[0]) if total_shares != "" else 0,
                    "created_at": utime,
                    "page_id": "2111",
                }
                print(post_dict)
            except:
                print("Skip to next post")
                continue
            # Insert new post to db
            graphQl_save(Crawler.client, InsertPost, post_dict)

            if num_of_cmts > 0:
                print("Crawling", num_of_cmts, "comments of post", post_id)
                label_list = [0, 0, 0]
                for comment in listHtmlCmts:
                    comment_owner = comment.find_elements_by_css_selector(
                        "._7a9b")

                    comment_info = self.get_comment_info(comment_owner[0])
                    # print(comment_info["user_name"])
                    # print(comment_info["avt"])
                    # add predict function for comment
                    # label = predict_results(
                    #     Crawler.model, comment_info["text"])
                    label = get_sentiment(comment_info["text"])
                    if label == "__lb__positive":
                        label_list[0] += 1
                    elif label == "__lb__negative":
                        label_list[1] += 1
                    else:
                        label_list[2] += 1

                    comment_info_dict = {"content": comment_info["text"],
                                         "created_at": comment_info["utime"],
                                         "post_id": post_id,
                                         "comment_id": comment_info["id"],
                                         "label": label,
                                         "user_name": comment_info["user_name"],
                                         "user_avatar": comment_info["avt"]}
                    graphQl_save(Crawler.client, InsertComment,
                                 comment_info_dict)
                # Update num of sentiment
                sentiment_dict = {
                    "postId": post_id, "neg": label_list[1], "neu": label_list[2], "pos": label_list[0], "img_link": image_url if image_url != "" else fanpage_pic}
                graphQl_save(Crawler.client,
                             UpdatePostSentiment, sentiment_dict)
                listJsonCmts.append(comment_info)

        print("Total comments crawled:", total)

    def crawl_post(self, POST_URL):
        SCROLL_DOWN = 2
        loader.start_for_post(
            POST_URL,
            SCROLL_DOWN,
            self.FILTER_CMTS_BY,
            self.VIEW_MORE_CMTS,
            self.VIEW_MORE_REPLIES,
            COMMENTABLE_SELECTOR_GROUP
        )
        driver = loader.driver
        total = 0
        post = driver.find_element_by_css_selector(
            'div._5pcr.userContentWrapper'
        )
        post_url = self.get_child_attribute(
            post, "._5pcq", "href").split("?")[0]

        # try:
        #     post_id = re.findall("\d+", post_url)[-1]
        # except:
        #     post_id = post_url.split("/")[-1]
        utime = self.get_child_attribute(post, "abbr", "data-utime")
        post_text = self.get_child_attribute(
            post, ".userContent", "textContent")
        total_shares = self.get_child_attribute(
            post, '[data-testid="UFI2SharesCount/root"]', "innerText")
        total_cmts = self.get_child_attribute(post, "._3hg-", "innerText")
        image_url = self.get_child_attribute(
            post, "img.scaledImageFitWidth.img", "src")
        # fanpage_url = self.get_child_attribute(post, "_6tb5 img", "src")
        # print(fanpage_url)

        listJsonCmts = []
        listHtmlCmts = post.find_elements_by_css_selector("._7a9a>li")
        try:
            comment_owner = listHtmlCmts[0].find_elements_by_css_selector(
                "._7a9b")
            post_id = self.get_comment_info(comment_owner[0])["fbid"]
        except:
            post_id = re.findall("\d+", post_url)[-1]

            # print("post id: {}".format(post_id))
        num_of_cmts = len(listHtmlCmts)

        total += num_of_cmts

        listJsonReacts = []
        listHtmlReacts = post.find_elements_by_css_selector("._1n9l")

        for react in listHtmlReacts:
            react_text = react.get_attribute("aria-label")
            listJsonReacts.append(react_text)

        likes = listJsonReacts[0].split()[0] if listJsonReacts != [] else "0"
        print(total_cmts)
        # try:
        post_dict = {
            "post_id": post_id,
            "content": post_text,
            "like": likes,
            "comment": int(total_cmts.split()[0]) if "K" not in total_cmts else int(float(total_cmts.split('K')[0]))*1000,
            "share": int(total_shares.split()[0]) if total_shares != "" else 0,
            "created_at": utime,
            "page_id": "102573281588756",
        }
        print(post_dict)
        # except:
        #     print("Skip to next post")

        # Insert new post to db
        graphQl_save(Crawler.client, InsertPost, post_dict)
        print(num_of_cmts)
        if num_of_cmts > 0:
            print("Crawling", num_of_cmts, "comments of post", post_id)
            label_list = [0, 0, 0]
            for comment in listHtmlCmts:
                comment_owner = comment.find_elements_by_css_selector(
                    "._7a9b")

                comment_info = self.get_comment_info(comment_owner[0])
                # print(comment_info["user_name"])
                # print(comment_info["avt"])
                # add predict function for comment
                # label = predict_results(
                #     Crawler.model, comment_info["text"])
                label = get_sentiment(comment_info["text"])
                if label == "__lb__positive":
                    label_list[0] += 1
                elif label == "__lb__negative":
                    label_list[1] += 1
                else:
                    label_list[2] += 1

                comment_info_dict = {"content": comment_info["text"],
                                     "created_at": comment_info["utime"],
                                     "post_id": post_id,
                                     "comment_id": comment_info["id"],
                                     "label": label,
                                     "user_name": comment_info["user_name"],
                                     "user_avatar": comment_info["avt"]}
                graphQl_save(Crawler.client, InsertComment,
                             comment_info_dict)
                print(comment_info)
            # Update num of sentiment
            sentiment_dict = {
                "postId": post_id, "neg": label_list[1], "neu": label_list[2], "pos": label_list[0], "img_link": image_url}
            graphQl_save(Crawler.client, UpdatePostSentiment, sentiment_dict)

        # print(listJsonCmts)

    def extract_group_data(self):
        # load_group = FbLoader('div._5pcr.userContentWrapper')
        SCROLL_DOWN = 4
        loader.start(
            self.GROUP_URL,
            SCROLL_DOWN,
            self.FILTER_CMTS_BY,
            self.VIEW_MORE_CMTS,
            self.VIEW_MORE_REPLIES,
            COMMENTABLE_SELECTOR_GROUP
        )
        driver = loader.driver
        total = 0

        listJsonPosts = []
        listHtmlPosts = driver.find_elements_by_css_selector(
            "div._5pcr.userContentWrapper"
        )
        print("Start crawling", len(listHtmlPosts), "posts...")

        for post in listHtmlPosts:
            post_url = self.get_child_attribute(
                post, "._5pcq", "href").split("?")[0]
            post_id = re.findall("\d+", post_url)[-1]
            utime = self.get_child_attribute(post, "abbr", "data-utime")
            post_text = self.get_child_attribute(
                post, ".userContent", "textContent")
            total_shares = self.get_child_attribute(
                post, '[data-testid="UFI2SharesCount/root"]', "innerText"
            )
            total_cmts = self.get_child_attribute(post, "._3hg-", "innerText")

            listJsonCmts = []
            listHtmlCmts = post.find_elements_by_css_selector("._7a9a>li")

            num_of_cmts = len(listHtmlCmts)
            total += num_of_cmts

            if num_of_cmts > 0:
                print("Crawling", num_of_cmts, "comments of post", post_id)

                for comment in listHtmlCmts:
                    comment_owner = comment.find_elements_by_css_selector(
                        "._7a9b")
                    comment_info = self.get_comment_info(comment_owner[0])
                    listJsonCmts.append(comment_info)

            listJsonReacts = []
            listHtmlReacts = post.find_elements_by_css_selector("._1n9l")

            for react in listHtmlReacts:
                react_text = react.get_attribute("aria-label")
                listJsonReacts.append(react_text)

            listJsonPosts.append(
                {
                    "url": post_url,
                    "id": post_id,
                    "utime": utime,
                    "text": post_text,
                    "total_shares": total_shares,
                    "total_cmts": total_cmts,
                    "crawled_cmts": listJsonCmts,
                    "reactions": listJsonReacts,
                }
            )
        print("Total comments crawled:", total)
        filename = GROUP_URL.split(
            "www.facebook.com")[-1].replace("/", "") + ".json"
        stop_and_save("db/"+filename, listJsonPosts)


if __name__ == "__main__":

    POST_URL = "https://www.facebook.com/bancotaima/posts/3791780320873041"
    GROUP_URL = "https://www.facebook.com/groups/machinelearningcoban/"
    FANPAGE_URL = "https://www.facebook.com/pg/TTVCrush-108591870825801/posts/"
    SCROLL_DOWN = 2
    FILTER_CMTS_BY = CMTS.ALL_COMMENTS
    VIEW_MORE_CMTS = 3
    VIEW_MORE_REPLIES = 3

    page_crawler = Crawler(FILTER_CMTS_BY, VIEW_MORE_CMTS, VIEW_MORE_REPLIES)
    page_crawler.crawl_post(POST_URL)
    # page_crawler.extract_fanpage_data(FANPAGE_URL)
    # page_crawler.extract_group_data()
    # print(COMMENTABLE_SELECTOR_PAGE)
