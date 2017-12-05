# -*- coding: utf-8 -*-
import os
import sys
import json
import requests

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

from flask import Flask, request, send_from_directory, render_template

from messenger_platform.messenger_api import Attachment, Template
from messenger_platform.messenger_api.payload import *
# from messenger_platform.messenger_api import QuickReply
# from messenger_platform.messenger_api import Page

from messenger_platform.config.config import CONFIG

from messenger_platform.config.fbpage import ghvn
from core.db import *

import PIL
from PIL import Image, ImageDraw, ImageFont

import datetime
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
USER = db.CDHH_USER
FAQ = db.CDHH_FAQ
NEWS = db.CDHH_NEWS


danh_sach_hinh_anh_HLV = {
    "Vũ Cát Tường": "hinh5_minigame.jpg",
    "Tiên Cookie và Hương Tràm": "hinh6_minigame.jpg",
    "Soobin": "hinh7_minigame.jpg"
}


danh_sach_HLV = ["Vũ Cát Tường", "Tiên Cookie và Hương Tràm", "Soobin"]
subscribe_options = ["yes1", "yes2", "no"]
fansign_list = ["vct", "sb", "ht", "tc"]


def ghvn_greeting(sender_id):
    user_profile = ghvn.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]
    check_customer_by_id('ghvn', sender_id)
    space = " "
    a = "Chào"
    b = "đến với Giọng Hát Việt Nhí. Tại đây, bạn có thể đặt câu hỏi, chơi Mini game và theo dõi những tin tức “nóng hổi” nhất từ chương trình. Còn chần chừ gì mà không bắt đầu cuộc “trò chuyện thân mật” ngay nào !!! ;) ;)\n⏩⏩⏩ Quay về tính năng chính bằng cách ấn phím “Home” hoặc gõ vào chữ “Home” hoặc “Menu” 👇\n⏩⏩⏩ Chương trình “Giọng Hát Việt Nhí” 2017 sẽ được phát sóng vào lúc 21h10 thứ 7 hằng tuần trên kênh VTV3📺 "
    seq = (a, last, first, b)
    text = space.join(seq)
    buttons = [
        Template.ButtonPostBack(
            "Home", "ghvn_home")
    ]
    ghvn.send(sender_id, Template.Buttons(text, buttons))


def ghvn_home(sender_id):
    elements = [
        Template.GenericElement("Fansign",
                                subtitle="Cùng đón nhận những lời chúc từ các huấn luyện viên Giọng Hát Việt Nhí 2017!!!",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/home_hinh1_tin_tuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Lấy Fansign", "ghvn_fansign")
                                ]),
        Template.GenericElement("Tin tức mới nhất từ chương trình “Giọng Hát Việt Nhí” 2017",
                                subtitle="Nơi cập nhật những tin tức mới nhất từ chương trình “Giọng Hát Việt Nhí” 2017",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/home_hinh1_tin_tuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Xem tin tức 👓", "ghvn_read_news"),
                                    Template.ButtonPostBack(
                                        "Theo dõi tin tức 📸", "ghvn_subscribe_news")
                                ]),
        Template.GenericElement("Video Full - The Voice Kids 2017 | Giọng Hát Việt Nhí mùa 5",
                                subtitle="Xem lại bản đầy dủ các tập đã được phát sóng trên Youtube, Live Streaming",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/home_hinh2_xem_video.jpg",
                                buttons=[
                                    Template.ButtonWeb(
                                        "Xem lại tập đã phát", "https://www.youtube.com/user/btcgionghatvietnhi"),
                                    Template.ButtonWeb(
                                        "Oh my kids", "https://www.youtube.com/playlist?list=PLEhBV4sOYnBml5RPOlILDvj5DqNwmG9AI"),
                                    Template.ButtonWeb(
                                        "Off the air", "https://www.youtube.com/playlist?list=PLEhBV4sOYnBk1BX8Jks9152rkNTIZQWuK")
                                ]),

        Template.GenericElement("Dự đoán kết quả và giành lấy cơ hội nhận quà",
                                subtitle="Tham gia dự đoán kết quả của cuộc thi để nhận được những phần quà hấp dẫn nhất từ ban tổ chức",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/home_hinh3_du_doan.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Minigame 1", "ghvn_minigame1"),
                                    Template.ButtonPostBack(
                                        "Minigame 2", "ghvn_minigame2")
                                ]),
        Template.GenericElement("About us",
                                subtitle="Theo dõi chương trình Giọng Hát Việt Nhí 2017 tại các kênh truyền thông",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/home_hinh4_about_us.jpg",
                                buttons=[
                                    Template.ButtonWeb(
                                        "Facebook", "https://www.facebook.com/gionghatvietnhi/"),
                                    Template.ButtonPostBack(
                                        "Giờ phát sóng", "ghvn_timeline"),
                                    Template.ButtonPostBack(
                                        "Giới thiệu", "ghvn_introduce")
                                ])
    ]
    ghvn.send(sender_id, Template.Generic(elements))


def ghvn_minigame1(sender_id):
    text = "Minigame 1:\n   Dự đoán đội quán quân"
    buttons = [
        Template.ButtonPostBack(
            "Tham gia dự đoán 👍", "ghvn_minigame1_menu"),
        Template.ButtonPostBack(
            "Thể lệ dự đoán 📜", "ghvn_minigame1_rule")
    ]
    ghvn.send(sender_id, Template.Buttons(text, buttons))
    return


def ghvn_minigame2(sender_id):
    text = "Minigame 2:\n   Đoán từ khóa nhận Sticker"
    buttons = [
        Template.ButtonPostBack(
            "Tham gia dự đoán 👍", "ghvn_minigame2_menu"),
        Template.ButtonPostBack(
            "Thể lệ dự đoán 📜", "ghvn_minigame2_rule")
    ]

    ghvn.send(sender_id, Template.Buttons(text, buttons))
    return


def ghvn_subscribe_news(sender_id):
    question = "Bằng cách đồng ý theo dõi tin tức dưới đây, bạn sẽ nhận được thông báo mỗi khi tin tức mới của chương trình “Giọng Hát Việt Nhí” 2017 được cập nhật.\nBạn muốn nhận thông báo chứ?"
    quick_replies = [
        QuickReply(title="1 tuần 1 lần 😋", payload="yes1"),
        QuickReply(title="1 tuần 2 lần 😈", payload="yes2"),
        QuickReply(title="Nhắc lại sau 😜", payload="no")
    ]
    ghvn.send(sender_id,
              question,
              quick_replies=quick_replies,
              metadata="DEVELOPER_DEFINED_METADATA")


def ghvn_handle_subscribe_news(sender_id, quick_reply_payload):
    if quick_reply_payload == 'no':
        text = "Okey. Bất cứ khi nào bạn cần đăng ký nhận tin tức thì quay lại đây nhé!"
        buttons = [
            Template.ButtonPostBack("Home", "ghvn_home")
        ]

        ghvn.send(sender_id, Template.Buttons(text, buttons))
        USER.update_one(
            {'id_user': sender_id},
            {'$set': {'subscribe_news': quick_reply_payload}}
        )
    else:
        text = "Bạn đã đăng ký nhận thông báo thành công.\nMỗi khi có thông báo mới về chương trình The Voice Kid 2017, mình sẽ gửi tới bạn."
        buttons = [
            Template.ButtonPostBack("Home", "ghvn_home")
        ]

        ghvn.send(sender_id, Template.Buttons(text, buttons))
        USER.update_one(
            {'id_user': sender_id},
            {'$set': {'subscribe_news': quick_reply_payload}}
        )


def ghvn_read_news(sender_id):
    elements = []
    for news in NEWS.find():
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'ghvn_home')
            ])
        elements.append(element)
    ghvn.send(sender_id, Template.Generic(elements))


def ghvn_minigame1_vote(sender_id):
    question = "Bạn dự đoán thí sinh thuộc đội của huấn luyện viên nào sẽ xuất sắc giành lấy ngôi vị quán quân của chương trình?"
    quick_replies = [
        QuickReply(title="#teamcôTường", payload="Vũ Cát Tường"),
        QuickReply(title="#teamcôTiênvàcôTràm",
                   payload="Tiên Cookie và Hương Tràm"),
        QuickReply(title="#teamchúSoobin", payload="Soobin")
    ]
    ghvn.send(sender_id,
              question,
              quick_replies=quick_replies,
              metadata="DEVELOPER_DEFINED_METADATA")


def ghvn_minigame1_menu(sender_id):
    check_vote = USER.find_one({'id_user': sender_id})

    if check_vote["HLV_da_binh_chon"] == "":
        # user chua binh chon
        ghvn_minigame1_vote(sender_id)
    else:
        # user da binh chon
        space = " "
        a = "Bạn đã dự đoán dự đoán thành công đội có thí sinh đạt được vị trí cao nhất của chương trình. Dự đoán của bạn đang dành cho team của"
        # a = a.decode('utf-8')
        b = check_vote["HLV_da_binh_chon"]
        seq = (a, b)
        text = space.join(seq)

        buttons = [
            Template.ButtonPostBack("Bình chọn lại", "ghvn_minigame1_vote"),
            Template.ButtonPostBack("Home", "ghvn_home")
        ]

        ghvn.send(sender_id, Template.Buttons(text, buttons))
    return


def ghvn_minigame1_handle_quick_reply(sender_id, quick_reply_payload):
    hinh_hlv = "http://210.211.109.211/weqbfyretnccbsaf/" + \
        danh_sach_hinh_anh_HLV[quick_reply_payload]
    ghvn.send(sender_id, Attachment.Image(hinh_hlv))

    space = " "
    a = "Bạn đã dự đoán dự đoán thành công đội có thí sinh đạt được vị trí cao nhất của chương trình. Dự đoán của bạn đang dành cho team của"
    seq = (a, quick_reply_payload)
    text = space.join(seq)
    buttons = [
        Template.ButtonPostBack("Bình chọn lại", "ghvn_minigame1_vote"),
        Template.ButtonPostBack("Home", "ghvn_home")
    ]
    ghvn.send(sender_id, Template.Buttons(text, buttons))

    USER.update_one(
        {'id_user': sender_id},
        {'$set': {'HLV_da_binh_chon': quick_reply_payload}}
    )


def ghvn_minigame1_rule(sender_id):
    text = "- Mỗi bạn tham gia sẽ có 01 lựa chọn cho việc dự đoán đội huấn luyện viên có thí sinh đạt được giải quán quân 🎊 của chương trình.\n- Nếu bạn thay đổi ý kiến, dự đoán được BTC ghi nhận là dự đoán cuối cùng mà bạn chọn.\n- Nếu dự đoán đúng và may mắn, bạn sẽ nhận được 01 phần quà 🎁 hấp dẫn từ ban tổ chức.\n Hãy tận dụng “giác quan thứ 6” của mình để 'rinh' quà về nhà nào!\n👉👉👉 “Giọng Hát Việt Nhí” 2017 sẽ chính thức được phát sóng vào lúc 21h10 thứ 7 hằng tuần trên kênh VTV3"
    buttons = [
        Template.ButtonPostBack("Home", "ghvn_home")
    ]
    ghvn.send(sender_id, Template.Buttons(text, buttons))


def ghvn_minigame2_rule(sender_id):
    text = "- Mỗi bạn tham gia được dự đoán không giới hạn ‘Từ khóa’ may mắn để nhận được trọn bộ Sticker hình vẽ HLV Giọng Hát Việt Nhí 2017.\n- ‘Từ khóa’ có thể gồm 1 từ hoặc 1 cụm từ miêu tả gần giống với các HLV nhất.\n- Nếu dự đoán đúng từ khóa. Bạn sẽ nhận được những Sticker ‘Siêu Đáng Yêu’.\nNgại gì không thử??\n\n👉👉👉 “Giọng Hát Việt Nhí” 2017 sẽ chính thức được phát sóng vào lúc 21h10 thứ 7 hằng tuần (từ ngày 12/8/2017) trên kênh VTV3"
    buttons = [
        Template.ButtonPostBack("Home", "ghvn_home")
    ]
    ghvn.send(sender_id, Template.Buttons(text, buttons))
    return


def ghvn_timeline(sender_id):
    text = "📣📣📣 Chương trình “Giọng Hát Việt Nhí” 2017 sẽ được phát sóng vào lúc 9h10 tối thứ 7 hằng tuần từ (ngày 12/08/2017) trên kênh VTV3"
    buttons = [
        Template.ButtonPostBack("Home", "ghvn_home")
    ]

    ghvn.send(sender_id, Template.Buttons(text, buttons))
    return


def ghvn_introduce(sender_id):
    text = "Đến hẹn lại lên, 'Giọng Hát Việt Nhí' đã trở lại và lợi hại hơn bao giờ hết. Với dàn huấn luyện viên là những nghệ sỹ trẻ nổi tiếng tài năng và sở hữu lượng fan hùng hậu nhất nhì làng giải trí Việt. Đó là cặp đôi Hương Tràm –Tiên Cookie, ca sĩ – nhạc sĩ Vũ Cát Tường, ca sĩ Soobin Hoàng Sơn. Họ hứa hẹn sẽ mang đến cho Giọng Hát Việt Nhí mùa 5 nhiều điều thú vị với độ cạnh tranh, “chặt chém” quyết liệt trên ghế nóng.\n📣📣📣 21h10 thứ 7 hằng tuần trên kênh VTV3 - Giọng Hát Việt Nhí 2017 với những bất ngờ đang chờ bạn khám phá!"
    buttons = [
        Template.ButtonPostBack("Home", "ghvn_home")
    ]

    ghvn.send(sender_id, Template.Buttons(text, buttons))
    return


def ghvn_handle_subscribe_1(sender_id):
    question = "Bằng cách đồng ý theo dõi, để nhận các tin tức mới nhất của Giọng Hát Việt Nhí 2017, các nhắc nhở giờ phát sóng của tập mới, bạn muốn nhận thông báo chứ?"
    quick_replies = [
        QuickReply(title="1 tuần 1 lần 😋", payload="yes1"),
        QuickReply(title="1 tuần 2 lần 😈", payload="yes2"),
        QuickReply(title="Nhắc lại sau 😜", payload="no")
    ]
    ghvn.send(sender_id,
              question,
              quick_replies=quick_replies,
              metadata="DEVELOPER_DEFINED_METADATA")

    return


# def handle_subscribe_2():


# def handle_subscribe_3():
def ghvn_minigame2_menu(sender_id):
    text = "Nhập một từ khóa bất kỳ để có cơ hội nhận Sticker 'Siêu Đáng Yêu' hình vẽ các HLV mà bạn yêu thích !! Ngại gì không thử ?? 👇👇.\n=> Gợi ý: Những từ/cụm từ được các HLV sử dụng nhiều nhất trong chương trình Giọng Hát Việt Nhí 2017."
    ghvn.send(sender_id, text)
    return


def ghvn_minigame2_handle_result(message, sender_id):
    message = message.lower()
    huong_tram = ["đỉnh", "xinh", "bánh bèo"]
    vu_cat_tuong = ["chất", "cá tính", "phũ"]
    soobin = ["đẹp trai", "ế", "cao"]
    tien_cookie = ["hit", "cute", "nhọ"]
    if message in huong_tram:
        game2_hlv_url = "http://210.211.109.211/weqbfyretnccbsaf/game2_huongtram.jpg"
        ghvn.send(sender_id, Attachment.Image(game2_hlv_url))
        text = "Chính xác!!!!!!!!"
        buttons = [
            Template.ButtonPostBack(
                "Đoán thêm lần nữa 😻", "ghvn_minigame2_menu"),
            Template.ButtonPostBack("Home", "ghvn_home")
        ]
        ghvn.send(sender_id, Template.Buttons(text, buttons))
    elif message in vu_cat_tuong:
        game2_hlv_url = "http://210.211.109.211/weqbfyretnccbsaf/game2_vucattuong.jpg"
        ghvn.send(sender_id, Attachment.Image(game2_hlv_url))
        text = "Chính xác!!!!!!!!"
        buttons = [
            Template.ButtonPostBack(
                "Đoán thêm lần nữa 😻", "ghvn_minigame2_menu"),
            Template.ButtonPostBack("Home", "ghvn_home")
        ]
        ghvn.send(sender_id, Template.Buttons(text, buttons))
    elif message in soobin:
        game2_hlv_url = "http://210.211.109.211/weqbfyretnccbsaf/game2_soobin.jpg"
        ghvn.send(sender_id, Attachment.Image(game2_hlv_url))
        text = "Chính xác!!!!!!!!"
        buttons = [
            Template.ButtonPostBack(
                "Đoán thêm lần nữa 😻", "ghvn_minigame2_menu"),
            Template.ButtonPostBack("Home", "ghvn_home")
        ]
        ghvn.send(sender_id, Template.Buttons(text, buttons))
    elif message in tien_cookie:
        game2_hlv_url = "http://210.211.109.211/weqbfyretnccbsaf/game2_tiencookie.jpg"
        ghvn.send(sender_id, Attachment.Image(game2_hlv_url))
        text = "Chính xác!!!!!!!!"
        buttons = [
            Template.ButtonPostBack(
                "Đoán thêm lần nữa 😻", "ghvn_minigame2_menu"),
            Template.ButtonPostBack("Home", "ghvn_home")
        ]
        ghvn.send(sender_id, Template.Buttons(text, buttons))


# def receive_feedback:
    # template để hiện nút và hình cho user gửi feedback
def ghvn_fansign_menu(sender_id):
    user_profile = ghvn.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]
    # id_user = user_profile["id"]
    print(last + ' ' + first)

    space = " "
    a = "ơi, bạn muốn nhận fansign từ HLV nào?"
    seq = (last, first, a)
    question = space.join(seq)

    quick_replies = [
        QuickReply(title="Soobin", payload="sb"),
        QuickReply(title="Vũ Cát Tường", payload="vct"),
        QuickReply(title="Hương Tràm", payload="ht"),
        QuickReply(title="Tiên Cookie", payload="tc")
    ]
    ghvn.send(sender_id, question, quick_replies=quick_replies,
              metadata="DEVELOPER_DEFINED_METADATA")


def ghvn_image_fs(sender_id, sizeFont, hlv, first, last, x_Text, y_Text):
    userName = last + ' ' + first
    font = ImageFont.truetype(
        "./resource/font_fansign/ghvn/font_fansign.ttf", sizeFont)
    imageFile = "image/" + hlv + ".jpg"
    im = Image.open(imageFile)
    draw = ImageDraw.Draw(im)
    draw.text((x_Text, y_Text), userName, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(im)
    name_fansigned = "/home/hoangphuc/Bot_Pictures/fs_" + hlv + \
        sender_id + ".jpg"
    im.save(name_fansigned)

    hlv_dict = {
        'sb': 'Soobin',
        'vct': 'Vũ Cát Tường',
        'ht': 'Hương Tràm',
        'tc': 'Tiên Cookie'
    }

    text1 = hlv_dict.get(
        hlv) + " đang viết lời chúc dành cho bạn. " + userName + " chờ xíu nhé 😉"
    ghvn.send(sender_id, text1)

    ghvn.send(sender_id, Attachment.Image(
        "http://210.211.109.211/weqbfyretnccbsaf/fs_" + hlv + sender_id + ".jpg"))
    text2 = 'Phía trên là hình fansign của ' + \
        hlv_dict.get(
            hlv) + ' dành riêng cho bạn. Hãy chia sẻ món quà này ngay kèm hashtag #gionghatvietnhifansign nha bạn ơi'
    buttons = [
        Template.ButtonPostBack("Fansign khác", "fansign"),
        Template.ButtonPostBack("Home", "ghvn_home")
    ]
    ghvn.send(sender_id, Template.Buttons(text2, buttons))
    print('da gui hinh fansign')


def ghvn_fansign_handle_quick_reply(sender_id, quickreply):
    user_profile = ghvn.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]
    userName = last + ' ' + first

    def fs_vct():
        if len(userName) < 11:
            ghvn_image_fs(sender_id, 90, "vct", first, last, 180, 370)
        else:
            ghvn_image_fs(sender_id, 80, "vct", first, last, 90, 370)

    def fs_ht():
        if len(userName) < 11:
            ghvn_image_fs(sender_id, 80, "ht", first, last, 180, 330)
        else:
            ghvn_image_fs(sender_id, 65, "ht", first, last, 180, 330)

    def fs_tc():
        if len(userName) < 11:
            ghvn_image_fs(sender_id, 90, "tc", first, last, 180, 390)
        else:
            ghvn_image_fs(sender_id, 80, "tc", first, last, 90, 380)

    def fs_sb():
        if len(userName) < 11:
            ghvn_image_fs(sender_id, 85, "sb", first, last, 30, 450)
        else:
            ghvn_image_fs(sender_id, 70, "sb", first, last, 30, 455)

    fs_hlv_list = {
        'sb': fs_sb,
        'vct': fs_vct,
        'ht': fs_ht,
        'tc': fs_tc
    }

    if quickreply in fs_hlv_list:
        fs_hlv_list[quickreply]()


# FROM MESSAGE_HANDLE
# def ghvn_answer(message, sender_id):
#     if message is not None:
#         found_question = False

#         for data in FAQ.find():
#             final_data = {}
#             count = 0
#             metadata = data['metadata']
#             for word in metadata:
#                 if word in message:
#                     count = count + 1

#             if count == len(data['metadata']):
#                 final_data = data
#                 found_question = True
#                 break

#         if found_question:
#             ghvn.send(sender_id, final_data['answer'])
#         else:
#             new_nofaq = {'message': message}
#             NOFAQ.insert_one(new_nofaq)
#             print('khong tim thay cau hoi trong FAQ, vao nofaq de xem')
#             text = "Oops..!Hiện tại mình chưa có dữ liệu câu hỏi của bạn, mình sẽ cập nhật và trả lời bạn sớm nhất. Hãy tiếp tục kết nối với chương trình qua các tính năng khác bạn nhé!"
#             buttons = [
#                 Template.ButtonPostBack(
#                     "Home", "home")
#             ]
#             ghvn.send(sender_id, Template.Buttons(text, buttons))

#     else:
#         pass

#     return


# def ghvn_find_cat(sender_id, word_dict, message):
#     dict_cat = {}
#     count_word_in_cat = 0
#     chosen_cat = {}
#     for cat_document in FAQ2.find({'level': '1'}):
#         for word in word_dict:
#             if word in cat_document['cat_keyword']:
#                 count_word_in_cat = count_word_in_cat + 1
#         dict_cat.update({cat_document['cat_title']: count_word_in_cat})
#         count_word_in_cat = 0
#         # print (dict_cat)

#     # gom cac cat_title co count_word_in_cat giong nhau lai
#     flipped = {}
#     for key, value in dict_cat.items():
#         if value not in flipped:
#             flipped[value] = [key]
#         else:
#             flipped[value].append(key)
#     # print(flipped)

#     # xep lai de thanh maximum
#     maximum_key = max(flipped)
#     maximum_value = flipped[maximum_key]
#     # print('maximum value cua find_cat la ', maximum_value, maximum_key)

#     if len(maximum_value) == 1 and maximum_key > 0:  # chi co 1 cat co so luong keyword la max
#         # print(maximum_value[0])
#         chosen_cat = FAQ2.find_one(
#             {'level': '1', 'cat_title': maximum_value[0]})
#         # text = 'da chon dc cat ' + chosen_cat['cat_title']
#         # ghvn.send(sender_id, text)
#         # return chosen_cat

#     # co nhieu cat co so luong keyword max bang nhau
#     elif len(maximum_value) > 1 and maximum_key > 0:
#         question = 'Giúp mình tìm câu trả lời nhé, bạn muốn tìm biết về mục nào của chương trình 😜'
#         quick_replies = []
#         for cat_title in maximum_value:
#             payload = '>' + \
#                 FAQ2.find_one({'level': '1', 'cat_title': cat_title})['cat_id']
#             quick_replies.append(QuickReply(
#                 title=cat_title, payload=payload))
#         ghvn.send(sender_id,
#                   question,
#                   quick_replies=quick_replies,
#                   metadata="DEVELOPER_DEFINED_METADATA")

#     else:  # khong co cat nao, max = 0
#         new_nofaq = {'message': message, 'id_user': sender_id}
#         NOFAQ.insert_one(new_nofaq)
#         print('khong tim thay cau hoi trong FAQ2, vao NOFAQ de xem')
#         text = "Oops..!Hiện tại mình chưa có dữ liệu câu hỏi của bạn, mình sẽ cập nhật và trả lời bạn sớm nhất. Hãy tiếp tục kết nối với chương trình qua các tính năng khác bạn nhé!😬😬"
#         buttons = [
#             Template.ButtonPostBack(
#                 "Home", "home")
#         ]
#         ghvn.send(sender_id, Template.Buttons(text, buttons))

#     return chosen_cat


# def ghvn_find_subcat(sender_id, word_dict, chosen_cat):
#     dict_subcat = {}
#     count_word_in_subcat = 0
#     chosen_subcat = {}
#     # print('chosen_cat ', chosen_cat)
#     for subcat_document in FAQ2.find({'level': '2', 'cat_id': chosen_cat['cat_id']}):
#         for word in word_dict:
#             if word in subcat_document['subcat_keyword']:
#                 count_word_in_subcat = count_word_in_subcat + 1
#         dict_subcat.update(
#             {subcat_document['subcat_title']: count_word_in_subcat})
#         count_word_in_subcat = 0
#         # print (dict_subcat)

#     # gom cac cat_title co count_word_in_cat giong nhau lai
#     flipped = {}
#     for key, value in dict_subcat.items():
#         if value not in flipped:
#             flipped[value] = [key]
#         else:
#             flipped[value].append(key)
#     # print(flipped)

#     # xep lai de thanh maximum
#     maximum_key = max(flipped)
#     maximum_value = flipped[maximum_key]
#     # print('maximum value la ', maximum_value)

#     if len(maximum_value) == 1:  # chi co 1 cat co so luong keyword la max
#         # print(maximum_value[0])
#         chosen_subcat = FAQ2.find_one(
#             {'level': '2', 'subcat_title': maximum_value[0], 'cat_id': chosen_cat['cat_id']})
#         # text = 'da chon dc subcat ' + chosen_subcat['subcat_id']
#         # ghvn.send(sender_id, text)
#         # return chosen_subcat

#     else:  # len(maximum_value) > 1
#         question = 'Hee, câu hỏi nào sẽ giúp mình giải đáp thắc mắc của bạn 😇'
#         quick_replies = []
#         for subcat_title in maximum_value:
#             subcat = FAQ2.find_one(
#                 {'level': '2', 'cat_id': chosen_cat['cat_id'], 'subcat_title': subcat_title})
#             payload = '>' + chosen_cat['cat_id'] + '>' + subcat['subcat_id']
#             quick_replies.append(QuickReply(
#                 title=subcat_title, payload=payload))
#         ghvn.send(sender_id,
#                   question,
#                   quick_replies=quick_replies,
#                   metadata="DEVELOPER_DEFINED_METADATA")
#     return chosen_subcat


# def ghvn_find_qa(sender_id, word_dict, chosen_subcat):
#     dict_qa = {}
#     count_word_in_qa = 0
#     chosen_qa = {}
#     # print('chosen_subcat trong find_qa', chosen_subcat)
#     for qa_document in FAQ2.find({'level': '3', 'cat_id': chosen_subcat['cat_id'], 'subcat_id': chosen_subcat['subcat_id']}):
#         for word in word_dict:
#             if word in qa_document['qa_keyword']:
#                 count_word_in_qa = count_word_in_qa + 1
#         dict_qa.update(
#             {qa_document['question']: count_word_in_qa})
#         count_word_in_qa = 0
#     # print ('dict_qa ', dict_qa)

#     # gom cac cat_title co count_word_in_cat giong nhau lai
#     flipped = {}
#     for key, value in dict_qa.items():
#         if value not in flipped:
#             flipped[value] = [key]
#         else:
#             flipped[value].append(key)
#     # print('flipped trong find_qa ', flipped)

#     # xep lai de thanh maximum
#     maximum_key = max(flipped)
#     maximum_value = flipped[maximum_key]
#     # print('maximum value cua qa la ', maximum_value)

#     if len(maximum_value) == 1:  # chi co 1 cat co so luong keyword la max
#         # print(maximum_value[0])
#         chosen_qa = FAQ2.find_one(
#             {'level': '3', 'question': maximum_value[0]})
#         text = chosen_qa['answer']
#         ghvn.send(sender_id, text)
#         # return chosen_qa

#     else:  # len(maximum_value) > 1
#         text = 'Câu hỏi nào giống với ý của nhất? 😋'
#         quick_replies = []
#         for question in maximum_value:
#             text = text + \
#                 ('\n' + str(maximum_value.index(question) + 1) + '. ' + question)
#             qa = FAQ2.find_one(
#                 {'level': '3', 'cat_id': chosen_subcat['cat_id'], 'subcat_id': chosen_subcat['subcat_id']})
#             payload = '>' + chosen_subcat['cat_id'] + '>' + \
#                 chosen_subcat['subcat_id'] + '>' + qa['qa_id']
#             quick_replies.append(QuickReply(
#                 title=str(maximum_value.index(question) + 1), payload=payload))
#         ghvn.send(sender_id,
#                   text,
#                   quick_replies=quick_replies,
#                   metadata="DEVELOPER_DEFINED_METADATA")
#     return chosen_qa


# def ghvn_handle_faq_quickreply(sender_id, quickreply_dict):
#     length = len(quickreply_dict)
#     print('length of quick_reply_dict ', length)
#     print(quickreply_dict)

#     if length > 3:
#         # length = 4
#         cat_id = quickreply_dict[1]
#         subcat_id = quickreply_dict[2]
#         qa_id = quickreply_dict[3]
#         result = FAQ2.find_one(
#             {'level': '3', 'cat_id': cat_id, 'subcat_id': subcat_id, 'qa_id': qa_id})
#         # print(result)
#         text = result['answer']
#         buttons = [
#             Template.ButtonPostBack(
#                 "Home", "home")
#         ]
#         ghvn.send(sender_id, Template.Buttons(text, buttons))

#     elif length > 2:
#         # length = 3
#         print('quick_reply: co cat_id, co subcat_id, khong co qa_id')
#         cat_id = quickreply_dict[1]
#         subcat_id = quickreply_dict[2]
#         question = 'Hee, câu hỏi nào sẽ giúp mình giải đáp thắc mắc của bạn 😇'
#         cursor_qa = FAQ2.find(
#             {'level': '3', 'cat_id': cat_id, 'subcat_id': subcat_id})
#         dict_qa = []
#         for i in cursor_qa:
#             dict_qa.append(i)
#         # print('dict_qa la ', dict_qa)
#         quick_replies = []
#         for qa in dict_qa:
#             question = question + \
#                 ('\n' + str(dict_qa.index(qa) + 1) + '. ' + qa['question'])
#             payload = '>' + cat_id + '>' + subcat_id + '>' + qa['qa_id']
#             quick_replies.append(QuickReply(
#                 title=str(dict_qa.index(qa) + 1), payload=payload))
#         ghvn.send(sender_id,
#                   question,
#                   quick_replies=quick_replies,
#                   metadata="DEVELOPER_DEFINED_METADATA")
#     else:
#         # length = 2
#         print('quick_reply: co cat_id, khong co subcat_id')
#         cat_id = quickreply_dict[1]
#         dict_subcat = FAQ2.find({'level': '2', 'cat_id': cat_id})
#         question = 'Giúp mình tìm câu trả lời nhé, bạn muốn tìm biết về mục nào của chương trình 😜'
#         quick_replies = []
#         for subcat in dict_subcat:
#             payload = '>' + cat_id + '>' + subcat['subcat_id']
#             quick_replies.append(QuickReply(
#                 title=subcat['subcat_title'], payload=payload))
#         ghvn.send(sender_id,
#                   question,
#                   quick_replies=quick_replies,
#                   metadata="DEVELOPER_DEFINED_METADATA")


# def ghvn_handle_faq_message(sender_id, message):
#     if message is not None:

#         # TACH TU (word_segmentation)
#         word_dict = word_sent(message)
#         print('Word Segmentation: ', word_dict)

#         chosen_cat = find_cat(sender_id, word_dict, message)
#         if chosen_cat != {}:
#             print('da tim thay chosen_cat')
#             chosen_subcat = find_subcat(sender_id, word_dict, chosen_cat)
#             if chosen_subcat != {}:
#                 print('da tim thay chosen_subcat')
#                 chosen_qa = find_qa(sender_id, word_dict, chosen_subcat)

#                 if chosen_qa != {}:
#                     print('da tim thay chosen_qa')
#                 else:
#                     print(
#                         'tim thay chosen_cat,tim thay chosen_subcat, khong tim thay chosen_qa')
#             else:
#                 print('tim thay chosen_cat, khong tim thay chosen_subcat')
#         else:
#             print('khong tim thay chosen_cat')
#     else:
#         print('Message is None')


def ghvn_message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload

    if message is not None:
        message = message.lower()
    else:
        pass

    quickreply_dict = quickreply.split('>')

    keyword_list = {
        'home': ghvn_home,
        'hello': ghvn_greeting,
        'hi': ghvn_greeting,
        'chào': ghvn_greeting,
        'alo': ghvn_greeting,
        'chao': ghvn_greeting,
        'xin chào': ghvn_greeting,
        'xin chao': ghvn_greeting,
        'Xin chào': ghvn_greeting,
        'giờ phát sóng': ghvn_timeline,
        'lịch phát sóng': ghvn_timeline,
        'giới thiệu': ghvn_introduce,
        'subscribe': ghvn_handle_subscribe_1,
        'fansign': ghvn_fansign_menu
    }
    minigame2_keyword_list = ["đỉnh", "xinh", "bánh bèo", "chất",
                              "phũ", "cá tính", "đẹp trai", "ế", "cao", "hit", "cute", "nhọ"]

    if message in keyword_list:
        # message = message.lo
        keyword_list[message](sender_id)
        return

    elif message in minigame2_keyword_list:
        ghvn_minigame2_handle_result(message, sender_id)
        return

    elif danh_sach_HLV.count(quickreply) == 1:
        ghvn_minigame1_handle_quick_reply(sender_id, quickreply)
        return

    elif subscribe_options.count(quickreply) == 1:
        ghvn_handle_subscribe_news(sender_id, quickreply)
        return

    elif fansign_list.count(quickreply) == 1:
        ghvn_fansign_handle_quick_reply(sender_id, quickreply)
        return
    # elif quickreply_dict[0] == '' and len(quickreply_dict) > 1:
    #     ghvn_handle_faq_quickreply(sender_id, quickreply_dict)

    else:
        print('khong tra loi duoc tin nhan')
        # luu tin nhan
        # ghvn_save_message(sender_id, message)
        # tra loi tin nhan
        # ghvn_handle_faq_message(sender_id, message)


def ghvn_postback_handler(event):
    sender_id = event.sender_id
    postback = event.postback_payload

    postback_list = {
        'ghvn_greeting': ghvn_greeting,
        'ghvn_home': ghvn_home,
        'ghvn_read_news': ghvn_read_news,
        'ghvn_subscribe_news': ghvn_subscribe_news,
        'ghvn_minigame1': ghvn_minigame1,
        'ghvn_minigame1_menu': ghvn_minigame1_menu,
        'ghvn_minigame1_vote': ghvn_minigame1_vote,
        'ghvn_minigame1_rule': ghvn_minigame1_rule,
        'ghvn_minigame2': ghvn_minigame2,
        'ghvn_minigame2_rule': ghvn_minigame2_rule,
        'ghvn_minigame2_menu': ghvn_minigame2_menu,
        'ghvn_time line': ghvn_timeline,
        'ghvn_introduce': ghvn_introduce,
        'ghvn_fansign': ghvn_fansign_menu
    }

    if postback in postback_list:
        postback_list[postback](sender_id)
