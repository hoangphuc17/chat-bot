# -*- coding: utf-8 -*-
import os
import sys
import json
import requests

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

from flask import Flask, request, send_from_directory, render_template

from messenger_platform.messenger_api import Attachment, Template

from messenger_platform.config.config import CONFIG

from messenger_platform.config.fbpage import cdhh
from core.db import *

import datetime
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
USER = db.CDHH_USER
FAQ = db.CDHH_FAQ
NEWS = db.CDHH_NEWS

cdhh_vote_list = ['Team Mai Tiến Dũng', 'Team Giang Hồng Ngọc', 'Team Đào Bá Lộc',
                  'Team Tiêu Châu Như Quỳnh', 'Team Erik', 'Team Hòa Mizy', 'Team Đức Phúc']
subscribe_options = ["yes1", "yes2", "no"]


def cdhh_greeting(sender_id):
    user_profile = cdhh.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]
    # gender = user_profile["gender"]

    check_customer_by_id('cdhh', sender_id)

    space = " "
    a = "Chào"
    b = "đến với Cặp Đôi Hoàn Hảo - Trữ Tình & Bolero.\nMình là LERO, rất vui được gặp bạn. Bạn có thể cùng mình cập nhật thông tin về chương trình một cách nhanh nhất. Cùng khám phá nào! 👇👇"
    seq = (a, last, first, b)
    text = space.join(seq)
    buttons = [
        Template.ButtonPostBack(
            "Home", "cdhh_home")
    ]
    cdhh.send(sender_id, Template.Buttons(text, buttons))


def cdhh_home(sender_id):
    elements = [
        Template.GenericElement("Tin tức",
                                subtitle="Tin tức mới nhất từ Cặp Đôi Hoàn Hảo - Trữ Tình & Bolero",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/cdhh_tintuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Xem tin tức 👓", "cdhh_news"),
                                    Template.ButtonPostBack(
                                        "Theo dõi tin tức 📸", "cdhh_subscribe")
                                ]),
        Template.GenericElement("Xem chương trình",
                                subtitle="Chương trình phát sóng 20:30 thứ 5 hàng tuần trên VTV3.\nBạn có thế xem lại tập Full với các bản tình ca siêu ngọt ngào tại đây nha!",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/cdhh_xemtintuc.jpg",
                                buttons=[
                                    Template.ButtonWeb(
                                        "Tập 2", "https://www.youtube.com/watch?v=Ynu6u0WSxrU"),
                                    Template.ButtonWeb(
                                        "Tập 1", "https://www.youtube.com/watch?v=6xE6VOkRr4Qv")
                                ]),
        Template.GenericElement("Bình chọn thí sinh",
                                subtitle="Tin tức mới nhất từ Cặp Đôi Hoàn Hảo - Trữ Tình & Bolero",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/cdhh_binhchon.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Bình chọn", "cdhh_vote")

                                ]),
        Template.GenericElement("Tìm hiểu thêm thông tin",
                                subtitle="Theo dõi Cặp Đôi Hoàn Hảo ngay nhé",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/cdhh_lienhe.jpg",
                                buttons=[
                                    Template.ButtonWeb(
                                        "Facebook", "https://www.facebook.com/capdoihoanhaotrutinhbolero/"),
                                    Template.ButtonWeb(
                                        "Youtube", "https://www.youtube.com/channel/UCF5RuEuoGrqGtscvLGLOMew/featured")

                                ])
    ]
    cdhh.send(sender_id, Template.Generic(elements))


def cdhh_news(sender_id):
    elements = []
    for item in NEWS.find():
        element = Template.GenericElement(
            title=item['title'],
            subtitle=item['subtitle'],
            image_url=item['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', item['item_url']),
                Template.ButtonPostBack('Về Home', 'cdhh_home')
            ])
        elements.append(element)

    cdhh.send(sender_id, Template.Generic(elements))


def cdhh_subscribe(sender_id):
    question = "Bằng cách đồng ý theo dõi tin tức dưới đây, bạn sẽ nhận được thông báo mỗi khi tin tức mới của chương trình được cập nhật.\nBạn muốn nhận thông báo chứ?"
    quick_replies = [
        QuickReply(title="1 tuần 1 lần 😋", payload="yes1"),
        QuickReply(title="1 tuần 2 lần 😈", payload="yes2"),
        QuickReply(title="Nhắc lại sau 😜", payload="no")
    ]
    cdhh.send(sender_id,
              question,
              quick_replies=quick_replies,
              metadata="DEVELOPER_DEFINED_METADATA")


def cdhh_subscribe_handler(sender_id, quick_reply_payload):
    if quick_reply_payload == 'no':
        text = "Okey. Bất cứ khi nào bạn cần đăng ký nhận tin tức thì quay lại đây nhé!"
        buttons = [
            Template.ButtonPostBack("Home", "cdhh_home")
        ]

        cdhh.send(sender_id, Template.Buttons(text, buttons))
        USER.update_one(
            {'id_user': sender_id},
            {'$set': {'subscribe': quick_reply_payload}}
        )
    else:
        text = "Bạn đã đăng ký nhận thông báo thành công. \nMỗi khi có thông báo mới về chương trình, mình sẽ gửi tới bạn."
        buttons = [
            Template.ButtonPostBack("Home", "cdhh_home")
        ]

        cdhh.send(sender_id, Template.Buttons(text, buttons))
        USER.update_one(
            {'id_user': sender_id},
            {'$set': {'subscribe': quick_reply_payload}}
        )


def cdhh_vote(sender_id):
    check_vote = USER.find_one({'id_user': sender_id})

    if check_vote['vote'] == '':
        # user chua binh chon
        cdhh_vote_menu(sender_id)
    else:
        # user da binh chon
        space = " "
        a = "Bạn đã dự đoán thành công. Dự đoán của bạn đang dành cho"
        b = check_vote["vote"]
        seq = (a, b)
        text = space.join(seq)

        buttons = [
            Template.ButtonPostBack("Bình chọn lại", "vote_menu"),
            Template.ButtonPostBack("Home", "home")
        ]

        cdhh.send(sender_id, Template.Buttons(text, buttons))


def cdhh_vote_menu(sender_id):
    question = 'Bình chọn ngay cho thí sinh bạn yêu thích nhất ngay nào! Bạn thuộc'
    quick_replies = [
        QuickReply(title="Team Mai Tiến Dũng", payload="Team Mai Tiến Dũng"),
        QuickReply(title="Team Giang Hồng Ngọc",
                   payload="Team Giang Hồng Ngọc"),
        QuickReply(title="Team Đào Bá Lộc", payload="Team Đào Bá Lộc"),
        QuickReply(title='Team Tiêu Châu Như Quỳnh',
                   payload='Team Tiêu Châu Như Quỳnh'),
        QuickReply(title='Team Erik', payload='Team Erik'),
        QuickReply(title='Team Hòa Mizy', payload='Team Hòa Mizy'),
        QuickReply(title='Team Đức Phúc', payload='Team Đức Phúc')
    ]
    cdhh.send(sender_id,
              question,
              quick_replies=quick_replies,
              metadata="DEVELOPER_DEFINED_METADATA")


def cdhh_vote_handler(sender_id, quickreply):
    space = " "
    a = "Bạn đã dự đoán thành công. Dự đoán của bạn đang dành cho"
    seq = (a, quickreply)
    text = space.join(seq)
    buttons = [
        Template.ButtonPostBack("Bình chọn lại", "cdhh_vote_menu"),
        Template.ButtonPostBack("Home", "cdhh_home")
    ]
    cdhh.send(sender_id, Template.Buttons(text, buttons))

    USER.update_one(
        {'id_user': sender_id},
        {'$set': {'vote': quickreply}}
    )


def cdhh_postback_handler(event):
    print('POSTBACK HANDLER CDHH')
    sender_id = event.sender_id
    postback = event.postback_payload

    postback_list = {
        'cdhh_greeting': cdhh_greeting,
        'cdhh_home': cdhh_home,
        'cdhh_news': cdhh_news,
        'cdhh_subscribe': cdhh_subscribe,
        'cdhh_vote': cdhh_vote,
        'cdhh_vote_menu': cdhh_vote_menu
    }

    if postback in postback_list:
        postback_list[postback](sender_id)


def cdhh_message_handler(event):
    print('MESSAGE HANDLER CDHH')
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload

    if message is not None:
        message = message.lower()
    else:
        pass

    # quickreply_dict = quickreply.split('>')

    keyword_list = {
        'hello': cdhh_greeting,
        'hi': cdhh_greeting,
        'home': cdhh_home,
        'bình chọn': cdhh_vote,
        'binh chon': cdhh_vote,
        'vote': cdhh_vote,
        'dang ky': cdhh_subscribe,
        'dang ki': cdhh_subscribe,
        'subscribe': cdhh_subscribe,
        'đăng ký': cdhh_subscribe,
        'đăng kí': cdhh_subscribe
    }

    if message in keyword_list:
        keyword_list[message](sender_id)
    elif cdhh_vote_list.count(quickreply) == 1:
        cdhh_vote_handler(sender_id, quickreply)
    elif subscribe_options.count(quickreply) == 1:
        cdhh_subscribe_handler(sender_id, quickreply)
