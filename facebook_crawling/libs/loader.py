import time
import json
from helium import *
import sys
sys.path.append('../')
CMTS = type(
    "Enum",
    (),
    {
        "MOST_RELEVANT": "RANKED_THREADED",
        "NEWEST": "RECENT_ACTIVITY",
        "ALL_COMMENTS": "RANKED_UNFILTERED",
    },
)


def load_more_posts():
    js_script = "window.scrollTo(0, document.body.scrollHeight)"
    driver.execute_script(js_script)
    while find_all(S('.async_saving [role="progressbar"]')) != []:
        pass


def click_multiple_button(selector):
    js_script = (
        "document.querySelectorAll('" + selector +
        "').forEach(btn => btn.click())"
    )
    driver.execute_script(js_script)
    while find_all(S(selector + ' [role="progressbar"]')) != []:
        pass


def click_single_button(selector):
    js_script = (
        "document.querySelectorAll('" + selector +
        "').forEach(btn => btn.click())"
    )
    driver.execute_script(js_script)
    # while find_all(S(selector + ' [role="progressbar"]')) != []:
    #     pass


def filter_comments(by):
    if by == CMTS.MOST_RELEVANT:
        return
    click_multiple_button('[data-ordering="RANKED_THREADED"]')
    click_multiple_button('[data-ordering="' + by + '"]')


def start_for_post(
    url="",
    scroll_down=0,
    filter_cmts_by=CMTS.MOST_RELEVANT,
    view_more_cmts=0,
    view_more_replies=0,
    commentable_selector="",
):
    print("Go to: ", url)
    global driver
    driver = start_chrome(url, headless=True)
    global selector
    selector = commentable_selector
    print("Load more posts and check for Not Now button")
    load_more_posts()

    btnNotNow = find_all(S("#expanding_cta_close_button"))
    if btnNotNow != []:
        print("Click Not Now button")
        click(btnNotNow[0].web_element.text)
    if btnNotNow == []:
        click("Lúc khác")
    click_single_button("a._3hg-._42ft")
    for i in range(scroll_down - 1):
        print("Load more posts times", i + 2, "/", scroll_down)
        load_more_posts()
    # btnComment = find_all(S("a._3hg-._42ft"))
    # js_script = "window.scrollTo(0, document.body.scrollHeight/3)"
    # driver.execute_script(js_script)
    # time.sleep(3)
    # if btnComment != []:
    #     print("Click view comment button")
    #     time.sleep(2)
    #     print(btnComment[0].web_element.text)
    #     click(btnComment[0].web_element.text)

    print("Filter comments by", filter_cmts_by)
    filter_comments(filter_cmts_by)

    for i in range(view_more_cmts):
        print("Click View more comments buttons times",
              i + 1, "/", view_more_cmts)
        click_multiple_button(selector + " ._7a94 ._4sxc")

    # for i in range(view_more_replies):
    #     print("Click Replies buttons times", i + 1, "/", view_more_replies)
    #     click_multiple_button(COMMENTABLE_SELECTOR + " ._7a9h ._4sxc")

    print("Click See more buttons of comments")
    click_multiple_button(selector + " .fss")

    # print("Load Comment")
    # click_multiple_button("a._3hg-._42ft")


def start(
    url="",
    scroll_down=0,
    filter_cmts_by=CMTS.MOST_RELEVANT,
    view_more_cmts=0,
    view_more_replies=0,
    commentable_selector="",
):
    print("Go to: ", url)
    global driver
    driver = start_chrome(url, headless=True)
    global selector
    selector = commentable_selector
    print("Load more posts and check for Not Now button")
    load_more_posts()

    btnNotNow = find_all(S("#expanding_cta_close_button"))
    if btnNotNow != []:
        print("Click Not Now button")
        click(btnNotNow[0].web_element.text)
    if btnNotNow == []:
        click("Lúc khác")
    for i in range(scroll_down - 1):
        print("Load more posts times", i + 2, "/", scroll_down)
        load_more_posts()
    # time.sleep(3)
    # btnComment = find_all(S("a._3hg-._42ft"))
    # js_script = "window.scrollTo(0, document.body.scrollHeight/2)"
    # driver.execute_script(js_script)
    # if btnComment != []:
    #     print("Click view comment button")
    #     click(btnComment[0].web_element.text)
    # click("#u_0_v > div > div._7a9u > div._68wo > div > div._4vn1 > span:nth-child(1) > a")

    print("Filter comments by", filter_cmts_by)
    filter_comments(filter_cmts_by)

    for i in range(view_more_cmts):
        print("Click View more comments buttons times",
              i + 1, "/", view_more_cmts)
        click_multiple_button(selector + " ._7a94 ._4sxc")

    # for i in range(view_more_replies):
    #     print("Click Replies buttons times", i + 1, "/", view_more_replies)
    #     click_multiple_button(COMMENTABLE_SELECTOR + " ._7a9h ._4sxc")

    print("Click See more buttons of comments")
    click_multiple_button(selector + " .fss")

    # print("Load Comment")
    # click_multiple_button("a._3hg-._42ft")
if __name__ == "__main__":
    start_chrome("")
