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

from messenger_platform.config.config import CONFIG

from messenger_platform.config.fbpage import ttb
from core.db import *

import random
import datetime
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc

CUSTOMER = db.CUSTOMER
FAQ = db.FAQ
NEWS = db.NEWS

# ttb_vote_list = ['Team Mai Tiến Dũng', 'Team Giang Hồng Ngọc', 'Team Đào Bá Lộc',
#                   'Team Tiêu Châu Như Quỳnh', 'Team Erik', 'Team Hòa Mizy', 'Team Đức Phúc']


# các function cần thực hiện
# 1. tin tức
#     - func(menu tin tức)
#     - theo dõi tin tức:
#         - func(menu xác nhận)
#         - func(xử lý kết quả)

# 2. game
#     - func(thể lệ)
#     - tham gia:
#         - func(menu tham gia)
#         - func(xử lý kết quả)
# 3. about
#     - func(about)
#     - func(timeline)
# 4. xem video
#     - func(video hot)


# func phụ
# - func(greeting)
# - func(home)

def ttb_greeting(sender_id):
    user_profile = ttb.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]

    check_customer_by_id('ttb', sender_id)

    space = " "
    a = "Chào"
    b = "đã đến với Chatbot Thần Tượng Bolero 2018. Tại đây, các bạn có thể đặt câu hỏi, chơi Mini game và theo dõi những tin tức 'nóng' nhất từ chương trình. Còn chần chừ gì mà không bắt đầu cuộc 'trò chuyện thân mật' ngay nào !!! ;) ;)\n⏩ Quay về tính năng chính bằng cách ấn phím 'Home' hoặc gõ vào chữ 'Home' hoặc 'Menu'👇\n⏩ Chương trình Thần Tượng Bolero 2018 sẽ được phát sóng vào lúc 20h30 thứ 5 hằng tuần trên kênh VTV3 bắt đầu từ ngày 25.1.2018"
    seq = (a, last, first, b)
    text = space.join(seq)
    buttons = [
        Template.ButtonPostBack(
            "Home", "ttb_home")
    ]
    ttb.send(sender_id, Template.Buttons(text, buttons))


def ttb_home(sender_id):
    elements = [
        Template.GenericElement("Tin tức",
                                subtitle="Tin tức mới nhất từ Thần tượng Bolero",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_tintuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Xem tin tức 👓", "ttb_news"),
                                    Template.ButtonPostBack(
                                        "Theo dõi tin tức 📸", "ttb_subscribe")
                                ])
        # Template.GenericElement("Xem video thần tượng bolero mùa 3 - 2018",
        #                         subtitle="Chương trình phát sóng 20:30 thứ 5 hàng tuần trên VTV3.\nBạn có thế xem lại tập Full với các bản tình ca siêu ngọt ngào tại đây nha!",
        #                         image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_xemtintuc.jpg",
        #                         buttons=[
        #                             Template.ButtonWeb(
        #                                 "Tập 2", "https://www.youtube.com/watch?v=Ynu6u0WSxrU"),
        #                             Template.ButtonWeb(
        #                                 "Tập 1", "https://www.youtube.com/watch?v=6xE6VOkRr4Qv")
        #                         ]),
        # Template.GenericElement("Minigame",
        #                         subtitle="Tham gia dự đoán kết quả của cuộc thi để nhận được những phần quà hấp dẫn nhất từ ban tổ chức",
        #                         image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_binhchon.jpg",
        #                         buttons=[
        #                             Template.ButtonPostBack(
        #                                 "Bình chọn", "ttb_vote")
        #                         ]),
        # Template.GenericElement("About us",
        #                         subtitle="Theo dõi Cặp Đôi Hoàn Hảo ngay nhé",
        #                         image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_lienhe.jpg",
        #                         buttons=[
        #                             Template.ButtonWeb(
        #                                 "Facebook", "https://www.facebook.com/capdoihoanhaotrutinhbolero/"),
        #                             Template.ButtonWeb(
        #                                 "Youtube", "https://www.youtube.com/channel/UCF5RuEuoGrqGtscvLGLOMew/featured")
        #                         ])
    ]
    ttb.send(sender_id, Template.Generic(elements))


def ttb_news(sender_id):
    elements = []
    news_list = []
    for news in NEWS.find({'chatbot': 'ttb'}):
        news_list.append(news)

    for news in news_list:
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'ttb_home')
            ])
        elements.append(element)
    short_list_elements = random.sample(elements, 10)
    cbtest.send(sender_id, Template.Generic(short_list_elements))


def ttb_menu_subscribe(sender_id):
    question = "Bằng cách đồng ý theo dõi tin tức dưới đây, bạn sẽ nhận được thông báo mỗi khi tin tức mới của chương trình được cập nhật.\nBạn muốn nhận thông báo chứ?"
    quick_replies = [
        QuickReply(title="1 tuần 1 lần 😋", payload="yes1"),
        QuickReply(title="1 tuần 2 lần 😈", payload="yes2"),
        QuickReply(title="Nhắc lại sau 😜", payload="no")
    ]
    ttb.send(sender_id,
             question,
             quick_replies=quick_replies,
             metadata="DEVELOPER_DEFINED_METADATA")


def ttb_handle_subscribe(sender_id, quick_reply_payload):
    if quick_reply_payload == 'no':
        text = "Okey. Bất cứ khi nào bạn cần đăng ký nhận tin tức thì quay lại đây nhé!"
        buttons = [
            Template.ButtonPostBack("Home", "ttb_home")
        ]

        ttb.send(sender_id, Template.Buttons(text, buttons))
        CUSTOMER.update_one(
            {'id_CUSTOMER': sender_id},
            {'$set': {'subscribe': quick_reply_payload}}
        )
    else:
        text = "Bạn đã đăng ký nhận thông báo thành công.\nMỗi khi có thông báo mới về chương trình, mình sẽ gửi tới bạn."
        buttons = [
            Template.ButtonPostBack("Home", "ttb_home")
        ]

        ttb.send(sender_id, Template.Buttons(text, buttons))
        CUSTOMER.update_one(
            {'id_CUSTOMER': sender_id},
            {'$set': {'subscribe': quick_reply_payload}}
        )


# def ttb_vote(sender_id):
#     check_vote = CUSTOMER.find_one({'id_CUSTOMER': sender_id})

#     if check_vote['vote'] == '':
#         # CUSTOMER chua binh chon
#         ttb_vote_menu(sender_id)
#     else:
#         # CUSTOMER da binh chon
#         space = " "
#         a = "Bạn đã dự đoán thành công. Dự đoán của bạn đang dành cho"
#         b = check_vote["vote"]
#         seq = (a, b)
#         text = space.join(seq)

#         buttons = [
#             Template.ButtonPostBack("Bình chọn lại", "vote_menu"),
#             Template.ButtonPostBack("Home", "home")
#         ]

#         ttb.send(sender_id, Template.Buttons(text, buttons))


# def ttb_vote_menu(sender_id):
#     question = 'Bình chọn ngay cho thí sinh bạn yêu thích nhất ngay nào! Bạn thuộc'
#     quick_replies = [
#         QuickReply(title="Team Mai Tiến Dũng", payload="Team Mai Tiến Dũng"),
#         QuickReply(title="Team Giang Hồng Ngọc",
#                    payload="Team Giang Hồng Ngọc"),
#         QuickReply(title="Team Đào Bá Lộc", payload="Team Đào Bá Lộc"),
#         QuickReply(title='Team Tiêu Châu Như Quỳnh',
#                    payload='Team Tiêu Châu Như Quỳnh'),
#         QuickReply(title='Team Erik', payload='Team Erik'),
#         QuickReply(title='Team Hòa Mizy', payload='Team Hòa Mizy'),
#         QuickReply(title='Team Đức Phúc', payload='Team Đức Phúc')
#     ]
#     ttb.send(sender_id,
#              question,
#              quick_replies=quick_replies,
#              metadata="DEVELOPER_DEFINED_METADATA")


# def ttb_vote_handler(sender_id, quickreply):
#     space = " "
#     a = "Bạn đã dự đoán thành công. Dự đoán của bạn đang dành cho"
#     seq = (a, quickreply)
#     text = space.join(seq)
#     buttons = [
#         Template.ButtonPostBack("Bình chọn lại", "ttb_vote_menu"),
#         Template.ButtonPostBack("Home", "ttb_home")
#     ]
#     ttb.send(sender_id, Template.Buttons(text, buttons))

#     CUSTOMER.update_one(
#         {'id_CUSTOMER': sender_id},
#         {'$set': {'vote': quickreply}}
    # )


def ttb_postback_handler(event):
    print('POSTBACK HANDLER TTB')
    sender_id = event.sender_id
    postback = event.postback_payload

    postback_list = {
        'ttb_greeting': ttb_greeting,
        'ttb_home': ttb_home,
        'ttb_news': ttb_news,
        'ttb_menu_subscribe': ttb_menu_subscribe
        # 'ttb_vote': ttb_vote,
        # 'ttb_vote_menu': ttb_vote_menu
    }

    if postback in postback_list:
        postback_list[postback](sender_id)


def ttb_message_handler(event):
    print('MESSAGE HANDLER TTB')
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload

    subscribe_options = ["yes1", "yes2", "no"]

    message_list = {
        'hi': ttb_greeting,
        'home': ttb_home
    }

    if message is not None:
        message = message.lower()

        if message in message_list:
            message_list[message](sender_id)
        elif subscribe_options.count(quickreply) == 1:
            ttb_handle_subscribe(sender_id, quickreply)

    else:
        pass
