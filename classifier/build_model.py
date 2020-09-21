from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from pyvi import ViTokenizer, ViPosTagger
import re
import pandas as pd
import string
import codecs
import tqdm
from fasttext import train_supervised, load_model
import os


# Từ điển tích cực, tiêu cực, phủ định
path_neg = "../classifier/sentiment_dicts/neg.txt"
path_pos = "../classifier/sentiment_dicts/pos.txt"
path_not = "../classifier/sentiment_dicts/not.txt"
stopwords_path = "../classifier/sentiment_dicts/stopwords.txt"


def load_list(filepath):
    with codecs.open(filepath, "r", encoding="UTF-8") as f:
        data_list = f.readlines()
    word_list = [n.replace("\n", "") for n in data_list]
    return word_list


neg_list = load_list(path_neg)
pos_list = load_list(path_pos)
not_list = load_list(path_not)
stw_list = load_list(stopwords_path)

# with codecs.open(path_neg, "r", encoding="UTF-8") as f:
#     neg = f.readlines()
# neg_list = [n.replace("\n", "") for n in neg]

# with codecs.open(path_pos, "r", encoding="UTF-8") as f:
#     pos = f.readlines()
# pos_list = [n.replace("\n", "") for n in pos]
# with codecs.open(path_not, "r", encoding="UTF-8") as f:
#     not_ = f.readlines()
# not_list = [n.replace("\n", "") for n in not_]

# with codecs.open(stopwords_path, "r", encoding="UTF-8") as f:
#     stw = f.readlines()
# stw_list = [n.replace("\n", "") for n in stw]


def preprocessing(text):
    # Remove các ký tự kéo dài: vd: đẹppppppp
    text = re.sub(
        r"([A-Z])\1+", lambda m: m.group(1).upper(), text, flags=re.IGNORECASE
    )
    text = re.sub(
        r"(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)", " ", text)
    # Chuyển thành chữ thường
    text = text.lower()

    # Chuẩn hóa tiếng Việt, xử lý emoj, chuẩn hóa tiếng Anh, thuật ngữ
    replace_list = {
        "òa": "oà",
        "óa": "oá",
        "ỏa": "oả",
        "õa": "oã",
        "ọa": "oạ",
        "òe": "oè",
        "óe": "oé",
        "ỏe": "oẻ",
        "õe": "oẽ",
        "ọe": "oẹ",
        "ùy": "uỳ",
        "úy": "uý",
        "ủy": "uỷ",
        "ũy": "uỹ",
        "ụy": "uỵ",
        "uả": "ủa",
        "ả": "ả",
        "ố": "ố",
        "u´": "ố",
        "ỗ": "ỗ",
        "ồ": "ồ",
        "ổ": "ổ",
        "ấ": "ấ",
        "ẫ": "ẫ",
        "ẩ": "ẩ",
        "ầ": "ầ",
        "ỏ": "ỏ",
        "ề": "ề",
        "ễ": "ễ",
        "ắ": "ắ",
        "ủ": "ủ",
        "ế": "ế",
        "ở": "ở",
        "ỉ": "ỉ",
        "ẻ": "ẻ",
        "àk": " à ",
        "aˋ": "à",
        "iˋ": "ì",
        "ă´": "ắ",
        "ử": "ử",
        "e˜": "ẽ",
        "y˜": "ỹ",
        "a´": "á",
        # Quy các icon về 2 loại emoj: Tích cực hoặc tiêu cực
        "👹": "negative",
        "👻": "positive",
        "💃": "positive",
        "🤙": " positive ",
        "👍": " positive ",
        "💄": "positive",
        "💎": "positive",
        "💩": "positive",
        "😕": "negative",
        "😱": "negative",
        "😸": "positive",
        "😾": "negative",
        "🚫": "negative",
        "🤬": "negative",
        "🧚": "positive",
        "🧡": "positive",
        "🐶": " positive ",
        "👎": " negative ",
        "😣": " negative ",
        "✨": " positive ",
        "❣": " positive ",
        "☀": " positive ",
        "♥": " positive ",
        "🤩": " positive ",
        "like": " positive ",
        "💌": " positive ",
        "🤣": " positive ",
        "🖤": " positive ",
        "🤤": " positive ",
        ":(": " negative ",
        "😢": " negative ",
        "❤": " positive ",
        "😍": " positive ",
        "😘": " positive ",
        "😪": " negative ",
        "😊": " positive ",
        "?": " ? ",
        "😁": " positive ",
        "💖": " positive ",
        "😟": " negative ",
        "😭": " negative ",
        "💯": " positive ",
        "💗": " positive ",
        "♡": " positive ",
        "💜": " positive ",
        "🤗": " positive ",
        "^^": " positive ",
        "😨": " negative ",
        "☺": " positive ",
        "💋": " positive ",
        "👌": " positive ",
        "😖": " negative ",
        "😀": " positive ",
        ":((": " negative ",
        "😡": " negative ",
        "😠": " negative ",
        "😒": " negative ",
        "🙂": " positive ",
        "😏": " negative ",
        "😝": " positive ",
        "😄": " positive ",
        "😙": " positive ",
        "😤": " negative ",
        "😎": " positive ",
        "😆": " positive ",
        "💚": " positive ",
        "✌": " positive ",
        "💕": " positive ",
        "😞": " negative ",
        "😓": " negative ",
        "️🆗️": " positive ",
        "😉": " positive ",
        "😂": " positive ",
        ":v": "  positive ",
        "=))": "  positive ",
        "😋": " positive ",
        "💓": " positive ",
        "😐": " negative ",
        ":3": " positive ",
        "😫": " negative ",
        "😥": " negative ",
        "😃": " positive ",
        "😬": " 😬 ",
        "😌": " 😌 ",
        "💛": " positive ",
        "🤝": " positive ",
        "🎈": " positive ",
        "😗": " positive ",
        "🤔": " negative ",
        "😑": " negative ",
        "🔥": " negative ",
        "🙏": " negative ",
        "🆗": " positive ",
        "😻": " positive ",
        "💙": " positive ",
        "💟": " positive ",
        "😚": " positive ",
        "❌": " negative ",
        "👏": " positive ",
        ";)": " positive ",
        "<3": " positive ",
        "🌝": " positive ",
        "🌷": " positive ",
        "🌸": " positive ",
        "🌺": " positive ",
        "🌼": " positive ",
        "🍓": " positive ",
        "🐅": " positive ",
        "🐾": " positive ",
        "👉": " positive ",
        "💐": " positive ",
        "💞": " positive ",
        "💥": " positive ",
        "💪": " positive ",
        "💰": " positive ",
        "😇": " positive ",
        "😛": " positive ",
        "😜": " positive ",
        "🙃": " positive ",
        "🤑": " positive ",
        "🤪": " positive ",
        "☹": " negative ",
        "💀": " negative ",
        "😔": " negative ",
        "😧": " negative ",
        "😩": " negative ",
        "😰": " negative ",
        "😳": " negative ",
        "😵": " negative ",
        "😶": " negative ",
        "🙁": " negative ",
        # Chuẩn hóa 1 số sentiment words/English words
        ":))": "  positive ",
        ":)": " positive ",
        "ô kêi": " ok ",
        "okie": " ok ",
        " o kê ": " ok ",
        "okey": " ok ",
        "ôkê": " ok ",
        "oki": " ok ",
        " oke ": " ok ",
        " okay": " ok ",
        "okê": " ok ",
        " tks ": " cám ơn ",
        "thks": " cám ơn ",
        "thanks": " cám ơn ",
        "ths": " cám ơn ",
        "thank": " cám ơn ",
        "⭐": "star ",
        "*": "star ",
        "🌟": "star ",
        "🎉": " positive ",
        "kg ": " không ",
        "not": " không ",
        " kg ": " không ",
        '"k ': " không ",
        " kh ": " không ",
        "kô": " không ",
        "hok": " không ",
        " kp ": " không phải ",
        " kô ": " không ",
        '"ko ': " không ",
        " ko ": " không ",
        " k ": " không ",
        "khong": " không ",
        " hok ": " không ",
        "he he": " positive ",
        "hehe": " positive ",
        "hihi": " positive ",
        "haha": " positive ",
        "hjhj": " positive ",
        " lol ": " negative ",
        " cc ": " negative ",
        "cute": " dễ thương ",
        "huhu": " negative ",
        " vs ": " với ",
        "wa": " quá ",
        "wá": " quá",
        "j": " gì ",
        "“": " ",
        " sz ": " cỡ ",
        "size": " cỡ ",
        " đx ": " được ",
        "dk": " được ",
        "dc": " được ",
        "đk": " được ",
        "đc": " được ",
        "authentic": " chuẩn chính hãng ",
        " aut ": " chuẩn chính hãng ",
        " auth ": " chuẩn chính hãng ",
        "thick": " positive ",
        "store": " cửa hàng ",
        "shop": " cửa hàng ",
        "sp": " sản phẩm ",
        "gud": " tốt ",
        "god": " tốt ",
        "wel done": " tốt ",
        "good": " tốt ",
        "gút": " tốt ",
        "sấu": " xấu ",
        "gut": " tốt ",
        " tot ": " tốt ",
        " nice ": " tốt ",
        "perfect": "rất tốt",
        "bt": " bình thường ",
        "time": " thời gian ",
        "qá": " quá ",
        " ship ": " giao hàng ",
        " m ": " mình ",
        " mik ": " mình ",
        "ể": "ể",
        "product": "sản phẩm",
        "quality": "chất lượng",
        "chat": " chất ",
        "excelent": "hoàn hảo",
        "bad": "tệ",
        "fresh": " tươi ",
        "sad": " tệ ",
        "date": " hạn sử dụng ",
        "hsd": " hạn sử dụng ",
        "quickly": " nhanh ",
        "quick": " nhanh ",
        "fast": " nhanh ",
        "delivery": " giao hàng ",
        " síp ": " giao hàng ",
        "beautiful": " đẹp tuyệt vời ",
        " tl ": " trả lời ",
        " r ": " rồi ",
        " shopE ": " cửa hàng ",
        " order ": " đặt hàng ",
        "chất lg": " chất lượng ",
        " sd ": " sử dụng ",
        " dt ": " điện thoại ",
        " nt ": " nhắn tin ",
        " tl ": " trả lời ",
        " sài ": " xài ",
        "bjo": " bao giờ ",
        "thik": " thích ",
        " sop ": " cửa hàng ",
        " fb ": " facebook ",
        " face ": " facebook ",
        " very ": " rất ",
        "quả ng ": " quảng  ",
        "dep": " đẹp ",
        " xau ": " xấu ",
        "delicious": " ngon ",
        "hàg": " hàng ",
        "qủa": " quả ",
        "iu": " yêu ",
        "fake": " giả mạo ",
        "trl": "trả lời",
        "><": " positive ",
        " por ": " tệ ",
        " poor ": " tệ ",
        "ib": " nhắn tin ",
        "rep": " trả lời ",
        "fback": " feedback ",
        "fedback": " feedback ",
        # dưới 3* quy về 1*, trên 3* quy về 5*
        "6 sao": " 5star ",
        "6 star": " 5star ",
        "5star": " 5star ",
        "5 sao": " 5star ",
        "5sao": " 5star ",
        "starstarstarstarstar": " 5star ",
        "1 sao": " 1star ",
        "1sao": " 1star ",
        "2 sao": " 1star ",
        "2sao": " 1star ",
        "2 starstar": " 1star ",
        "1star": " 1star ",
        "0 sao": " 1star ",
        "0star": " 1star ",
    }

    for k, v in replace_list.items():
        text = text.replace(k, v)

    # chuyen punctuation thành space
    translator = str.maketrans(
        string.punctuation, " " * len(string.punctuation))
    text = text.translate(translator)

    text = ViTokenizer.tokenize(text)
    texts = text.split()
    # texts = [txt for txt in texts if txt not in stw_list]
    len_text = len(texts)

    # texts = [t.replace("_", " ") for t in texts]
    for i in range(len_text):
        cp_text = texts[i]
        if (
            cp_text in not_list
        ):  # Xử lý vấn đề phủ định (VD: áo này chẳng đẹp--> áo này notpos)
            numb_word = 2 if len_text - i - 1 >= 4 else len_text - i - 1

            for j in range(numb_word):
                if texts[i + j + 1] in pos_list:
                    texts[i] = "notpos"
                    texts[i + j + 1] = ""

                if texts[i + j + 1] in neg_list:
                    texts[i] = "notneg"
                    texts[i + j + 1] = ""
        # Thêm feature cho những sentiment words (áo này đẹp--> áo này đẹp positive)
        else:
            if cp_text in pos_list:
                texts.append("positive")
            elif cp_text in neg_list:
                texts.append("negative")

    text = " ".join(texts)

    # remove nốt những ký tự thừa thãi
    text = text.replace('"', " ").replace("️", "").replace(
        "🏻", "").replace(")", "").replace("\n", " ")
    text = text.strip()
    return text


def preprocessing_2(text):
    # Remove các ký tự kéo dài: vd: đẹppppppp
    text = re.sub(
        r"([A-Z])\1+", lambda m: m.group(1).upper(), text, flags=re.IGNORECASE
    )

    # Chuyển thành chữ thường
    text = text.lower()

    # Chuẩn hóa tiếng Việt, xử lý emoj, chuẩn hóa tiếng Anh, thuật ngữ
    replace_list = {
        "òa": "oà",
        "óa": "oá",
        "ỏa": "oả",
        "õa": "oã",
        "ọa": "oạ",
        "òe": "oè",
        "óe": "oé",
        "ỏe": "oẻ",
        "õe": "oẽ",
        "ọe": "oẹ",
        "ùy": "uỳ",
        "úy": "uý",
        "ủy": "uỷ",
        "ũy": "uỹ",
        "ụy": "uỵ",
        "uả": "ủa",
        "ả": "ả",
        "ố": "ố",
        "u´": "ố",
        "ỗ": "ỗ",
        "ồ": "ồ",
        "ổ": "ổ",
        "ấ": "ấ",
        "ẫ": "ẫ",
        "ẩ": "ẩ",
        "ầ": "ầ",
        "ỏ": "ỏ",
        "ề": "ề",
        "ễ": "ễ",
        "ắ": "ắ",
        "ủ": "ủ",
        "ế": "ế",
        "ở": "ở",
        "ỉ": "ỉ",
        "ẻ": "ẻ",
        "àk": " à ",
        "aˋ": "à",
        "iˋ": "ì",
        "ă´": "ắ",
        "ử": "ử",
        "e˜": "ẽ",
        "y˜": "ỹ",
        "a´": "á",
        # Quy các icon về 2 loại emoj: Tích cực hoặc tiêu cực
        "👹": "negative",
        "👻": "positive",
        "💃": "positive",
        "🤙": " positive ",
        "👍": " positive ",
        "💄": "positive",
        "💎": "positive",
        "💩": "positive",
        "😕": "negative",
        "😱": "negative",
        "😸": "positive",
        "😾": "negative",
        "🚫": "negative",
        "🤬": "negative",
        "🧚": "positive",
        "🧡": "positive",
        "🐶": " positive ",
        "👎": " negative ",
        "😣": " negative ",
        "✨": " positive ",
        "❣": " positive ",
        "☀": " positive ",
        "♥": " positive ",
        "🤩": " positive ",
        "like": " positive ",
        "💌": " positive ",
        "🤣": " positive ",
        "🖤": " positive ",
        "🤤": " positive ",
        ":(": " negative ",
        "😢": " negative ",
        "❤": " positive ",
        "😍": " positive ",
        "😘": " positive ",
        "😪": " negative ",
        "😊": " positive ",
        "?": " ? ",
        "😁": " positive ",
        "💖": " positive ",
        "😟": " negative ",
        "😭": " negative ",
        "💯": " positive ",
        "💗": " positive ",
        "♡": " positive ",
        "💜": " positive ",
        "🤗": " positive ",
        "^^": " positive ",
        "😨": " negative ",
        "☺": " positive ",
        "💋": " positive ",
        "👌": " positive ",
        "😖": " negative ",
        "😀": " positive ",
        ":((": " negative ",
        "😡": " negative ",
        "😠": " negative ",
        "😒": " negative ",
        "🙂": " positive ",
        "😏": " negative ",
        "😝": " positive ",
        "😄": " positive ",
        "😙": " positive ",
        "😤": " negative ",
        "😎": " positive ",
        "😆": " positive ",
        "💚": " positive ",
        "✌": " positive ",
        "💕": " positive ",
        "😞": " negative ",
        "😓": " negative ",
        "️🆗️": " positive ",
        "😉": " positive ",
        "😂": " positive ",
        ":v": "  positive ",
        "=))": "  positive ",
        "😋": " positive ",
        "💓": " positive ",
        "😐": " negative ",
        ":3": " positive ",
        "😫": " negative ",
        "😥": " negative ",
        "😃": " positive ",
        "😬": " 😬 ",
        "😌": " 😌 ",
        "💛": " positive ",
        "🤝": " positive ",
        "🎈": " positive ",
        "😗": " positive ",
        "🤔": " negative ",
        "😑": " negative ",
        "🔥": " negative ",
        "🙏": " negative ",
        "🆗": " positive ",
        "😻": " positive ",
        "💙": " positive ",
        "💟": " positive ",
        "😚": " positive ",
        "❌": " negative ",
        "👏": " positive ",
        ";)": " positive ",
        "<3": " positive ",
        "🌝": " positive ",
        "🌷": " positive ",
        "🌸": " positive ",
        "🌺": " positive ",
        "🌼": " positive ",
        "🍓": " positive ",
        "🐅": " positive ",
        "🐾": " positive ",
        "👉": " positive ",
        "💐": " positive ",
        "💞": " positive ",
        "💥": " positive ",
        "💪": " positive ",
        "💰": " positive ",
        "😇": " positive ",
        "😛": " positive ",
        "😜": " positive ",
        "🙃": " positive ",
        "🤑": " positive ",
        "🤪": " positive ",
        "☹": " negative ",
        "💀": " negative ",
        "😔": " negative ",
        "😧": " negative ",
        "😩": " negative ",
        "😰": " negative ",
        "😳": " negative ",
        "😵": " negative ",
        "😶": " negative ",
        "🙁": " negative ",
        # Chuẩn hóa 1 số sentiment words/English words
        ":))": "  positive ",
        ":)": " positive ",
        "ô kêi": " ok ",
        "okie": " ok ",
        " o kê ": " ok ",
        "okey": " ok ",
        "ôkê": " ok ",
        "oki": " ok ",
        " oke ": " ok ",
        " okay": " ok ",
        "okê": " ok ",
        " tks ": " cám ơn ",
        "thks": " cám ơn ",
        "thanks": " cám ơn ",
        "ths": " cám ơn ",
        "thank": " cám ơn ",
        "⭐": "star ",
        "*": "star ",
        "🌟": "star ",
        "🎉": " positive ",
        "kg ": " không ",
        "not": " không ",
        " kg ": " không ",
        '"k ': " không ",
        " kh ": " không ",
        "kô": " không ",
        "hok": " không ",
        " kp ": " không phải ",
        " kô ": " không ",
        '"ko ': " không ",
        " ko ": " không ",
        " k ": " không ",
        "khong": " không ",
        " hok ": " không ",
        "he he": " positive ",
        "hehe": " positive ",
        "hihi": " positive ",
        "haha": " positive ",
        "hjhj": " positive ",
        " lol ": " negative ",
        " cc ": " negative ",
        "cute": " dễ thương ",
        "huhu": " negative ",
        " vs ": " với ",
        "wa": " quá ",
        "wá": " quá",
        "j": " gì ",
        "“": " ",
        " sz ": " cỡ ",
        "size": " cỡ ",
        " đx ": " được ",
        "dk": " được ",
        "dc": " được ",
        "đk": " được ",
        "đc": " được ",
        "authentic": " chuẩn chính hãng ",
        " aut ": " chuẩn chính hãng ",
        " auth ": " chuẩn chính hãng ",
        "thick": " positive ",
        "store": " cửa hàng ",
        "shop": " cửa hàng ",
        "sp": " sản phẩm ",
        "gud": " tốt ",
        "god": " tốt ",
        "wel done": " tốt ",
        "good": " tốt ",
        "gút": " tốt ",
        "sấu": " xấu ",
        "gut": " tốt ",
        " tot ": " tốt ",
        " nice ": " tốt ",
        "perfect": "rất tốt",
        "bt": " bình thường ",
        "time": " thời gian ",
        "qá": " quá ",
        " ship ": " giao hàng ",
        " m ": " mình ",
        " mik ": " mình ",
        "ể": "ể",
        "product": "sản phẩm",
        "quality": "chất lượng",
        "chat": " chất ",
        "excelent": "hoàn hảo",
        "bad": "tệ",
        "fresh": " tươi ",
        "sad": " tệ ",
        "date": " hạn sử dụng ",
        "hsd": " hạn sử dụng ",
        "quickly": " nhanh ",
        "quick": " nhanh ",
        "fast": " nhanh ",
        "delivery": " giao hàng ",
        " síp ": " giao hàng ",
        "beautiful": " đẹp tuyệt vời ",
        " tl ": " trả lời ",
        " r ": " rồi ",
        " shopE ": " cửa hàng ",
        " order ": " đặt hàng ",
        "chất lg": " chất lượng ",
        " sd ": " sử dụng ",
        " dt ": " điện thoại ",
        " nt ": " nhắn tin ",
        " tl ": " trả lời ",
        " sài ": " xài ",
        "bjo": " bao giờ ",
        "thik": " thích ",
        " sop ": " cửa hàng ",
        " fb ": " facebook ",
        " face ": " facebook ",
        " very ": " rất ",
        "quả ng ": " quảng  ",
        "dep": " đẹp ",
        " xau ": " xấu ",
        "delicious": " ngon ",
        "hàg": " hàng ",
        "qủa": " quả ",
        "iu": " yêu ",
        "fake": " giả mạo ",
        "trl": "trả lời",
        "><": " positive ",
        " por ": " tệ ",
        " poor ": " tệ ",
        "ib": " nhắn tin ",
        "rep": " trả lời ",
        "fback": " feedback ",
        "fedback": " feedback ",
        # dưới 3* quy về 1*, trên 3* quy về 5*
        "6 sao": " 5star ",
        "6 star": " 5star ",
        "5star": " 5star ",
        "5 sao": " 5star ",
        "5sao": " 5star ",
        "starstarstarstarstar": " 5star ",
        "1 sao": " 1star ",
        "1sao": " 1star ",
        "2 sao": " 1star ",
        "2sao": " 1star ",
        "2 starstar": " 1star ",
        "1star": " 1star ",
        "0 sao": " 1star ",
        "0star": " 1star ",
    }

    for k, v in replace_list.items():
        text = text.replace(k, v)

    # chuyen punctuation thành space
    translator = str.maketrans(
        string.punctuation, " " * len(string.punctuation))
    text = text.translate(translator)

    text = ViTokenizer.tokenize(text)

    # remove nốt những ký tự thừa thãi
    text = text.replace('"', " ").replace("️", "").replace(
        "🏻", "").replace(")", "").replace("\n", " ")
    return text


dir_path = os.path.dirname(os.path.realpath(os.getcwd()))


def get_data(folder_path):
    # dirs = os.listdir(folder_path)
    X = []
    y = []
    for file_path in os.listdir(folder_path):
        if file_path.startswith("neg"):
            label = 0
        elif file_path.startswith("neu"):
            label = 2
        else:
            label = 1
        path = os.path.join(folder_path, file_path)
        with open(path, "r") as f:
            lines = f.read().split("\n")
            lines = [preprocessing(line) for line in lines]
            X.append(line for line in lines)
            y.append([label] * len(lines))

    return X, y


# train_path = os.path.join(dir_path, "data")
# print(os.listdir(train_path))
# X, y = get_data(train_path)
# # print(len(X))
# print(y)


def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))


def test(model, test_path):
    data = {}
    with open(test_path, encoding="utf-8") as fp:
        for line in fp.readlines():
            line = line.strip()
            words = line.split()
            label = words[0]
            pred = model.predict(" ".join(words[1:]))[0][0]
            if label not in data:
                data[label] = {}
                data[label]["correct"] = 0
                data[label]["total"] = 0
            data[label]["total"] += 1
            if label == pred:
                data[label]["correct"] += 1
    summaries = {}
    for key in data:
        summaries[key] = round(data[key]["correct"] / data[key]["total"], 2)
    return summaries, data


def predict_results(model, sentence):
    res = model.predict(preprocessing(sentence))
    return res[0][0]


if __name__ == "__main__":
    current_dir = os.getcwd()
    data_path = os.path.join(current_dir, "data")
    train_data = "../data_preprocessed/train.txt"
    valid_data = "../data_preprocessed/test.txt"
    model = train_supervised(
        input=train_data,
        epoch=150,
        lr=0.05,
        wordNgrams=2,
        verbose=2,
        loss="softmax",
        label="__lb__",
    )
    print_results(*model.test(valid_data))
    summaries, details = test(model, valid_data)
    print(summaries)
    print(details)
    model.save_model("model/ft.li.1701.bin")
    # model = load_model("model/ft.li.1701.bin")
    # with open(valid_data, "r") as f:
    #     lines = f.read().split("\n")
    #     lines = [str(model.predict((line))[0]).replace(
    #         "('", "").replace("',)", "") + " " + line for line in lines]
    # with open("test4.txt", "w") as wf:
    #     for line in lines:
    #         wf.write(line + "\n")
