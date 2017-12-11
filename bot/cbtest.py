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

from messenger_platform.config.fbpage import cbtest
from core.db import *

import datetime
import random
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
# USER = db.CDHH_USER
FAQ = db.FAQ
NEWS = db.NEWS

# cbtest_home
# cbtest_greeting

# cbtest_menu_upload
# cbtest_implement_upload
# cbtest_upload_success_continue

# cbtest_get_news_general
# cbtest_get_news_giai_tri
# cbtest_get_news_am_nhac


def cbtest_greeting(sender_id):
    user_profile = cbtest.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]

    check_customer_by_id('cbtest', sender_id)
    print(sender_id)
    text = 'chao'
    buttons = [
        Template.ButtonPostBack(
            "Home", "cbtest_home")
    ]
    cbtest.send(sender_id, Template.Buttons(text, buttons))


def cbtest_home(sender_id):
    elements = [
        Template.GenericElement("Đóng góp hình ảnh",
                                subtitle="Saostar",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_tintuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Upload", "cbtest_menu_upload")

                                ]),
        Template.GenericElement("Tin tức",
                                subtitle="Saostar",
                                image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_xemtintuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Xem tin tức", "cbtest_get_news_general")
                                ])
    ]
    cbtest.send(sender_id, Template.Generic(elements))


# UPLOAD
def cbtest_menu_upload(sender_id):
    text = 'nhấn chọn nút ở dưới để bắt đầu quy trình upload'
    buttons = [
        Template.ButtonPostBack(
            "Upload", "cbtest_implement_upload")
    ]
    cbtest.send(sender_id, Template.Buttons(text, buttons))


def cbtest_implement_upload(sender_id):
    # text = 'hãy chọn hình ảnh để upload cho'
    text = 'chọn hình và gửi'

    # update upload_status = yes
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id, 'upload_status': 'on'}}}
    )

    cbtest.send(sender_id, text)


def cbtest_upload_success_continue(chatbot, sender_id, attachment_link):
    # check upload status
    # save hình đó lại
    # hiển thị thông báo đã upload thành công
    # hỏi upload tiếp tục không
    cus = CUSTOMER.find_one({'id_user': sender_id})
    if bool(cus):
        if cus['SCRIPT']['upload_status'] == 'on':
            save_attachments(chatbot, sender_id, attachment_link)
            cbtest.send(sender_id, 'da luu thanh cong')

    # check_upload_status = CUSTOMER.find_one({
    #     'SCRIPT': {'id_user': sender_id}
    # })

    # if bool(check_upload_status):
    #     save_attachments(chatbot, sender_id, attachment_link)
    #     cbtest.send(sender_id, 'da luu hinh anh thanh cong')
    # else:
    #     cbtest.send(sender_id, 'chua vao che do save')


# NEWS
def cbtest_get_news_general(sender_id):
    elements = []
    news_list = []
    for news in NEWS.find({'chatbot': 'saostar'}):
        news_list.append(news)

    for news in news_list:
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'cbtest_home')
            ])
        elements.append(element)

    short_list_elements = random.sample(elements, 10)
    cbtest.send(sender_id, Template.Generic(short_list_elements))

    question = 'Xem thêm'
    quick_replies = [
        QuickReply(title="Giải trí", payload="giai_tri"),
        QuickReply(title="Âm nhạc", payload="am_nhac")
    ]
    cbtest.send(sender_id,
                question,
                quick_replies=quick_replies,
                metadata="DEVELOPER_DEFINED_METADATA")


def cbtest_get_news_giai_tri(sender_id):
    elements = []
    news_list = []
    for news in NEWS.find({'chatbot': 'saostar', 'category': 'giai_tri'}):
        news_list.append(news)

    for news in news_list:
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'cbtest_home')
            ])
        elements.append(element)

    short_list_elements = random.sample(elements, 10)
    cbtest.send(sender_id, Template.Generic(short_list_elements))

    question = 'Xem thêm'
    quick_replies = [
        QuickReply(title="Âm nhạc", payload="am_nhac")
    ]
    cbtest.send(sender_id,
                question,
                quick_replies=quick_replies,
                metadata="DEVELOPER_DEFINED_METADATA")


def cbtest_get_news_am_nhac(sender_id):
    elements = []
    news_list = []
    for news in NEWS.find({'chatbot': 'saostar', 'category': 'am_nhac'}):
        news_list.append(news)

    for news in news_list:
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'cbtest_home')
            ])
        elements.append(element)

    short_list_elements = random.sample(elements, 10)
    cbtest.send(sender_id, Template.Generic(short_list_elements))

    question = 'Xem thêm'
    quick_replies = [
        QuickReply(title="Âm nhạc", payload="giai_tri")
    ]
    cbtest.send(sender_id,
                question,
                quick_replies=quick_replies,
                metadata="DEVELOPER_DEFINED_METADATA")


def cbtest_postback_handler(event):
    print('POSTBACK HANDLER CBTEST')
    sender_id = event.sender_id
    postback = event.postback_payload
    postback_list = {
        # 'cbtest_upload_image': cbtest_upload_image,
        'cbtest_home': cbtest_home,
        'cbtest_menu_upload': cbtest_menu_upload,
        'cbtest_implement_upload': cbtest_implement_upload,
        'cbtest_get_news_general': cbtest_get_news_general
    }

    if postback in postback_list:
        postback_list[postback](sender_id)


def cbtest_message_handler(event):
    print('MESSAGE HANDLER CBTEST')
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload
    attachment_link = event.attachment_link

    if message is not None:
        message = message.lower()
        message_list = {
            'hi': cbtest_greeting,
            'home': cbtest_home
        }
        if message in message_list:
            message_list[message](sender_id)

    elif quickreply is not None:
        list_category = {
            'giai_tri': cbtest_get_news_giai_tri,
            'am_nhac': cbtest_get_news_am_nhac
        }
        if quickreply in list_category:
            list_category[quickreply](sender_id)

    elif attachment_link is not None:
        if attachment_link != []:
            print(attachment_link)
            cbtest.send(sender_id, 'thanks bro')
            cbtest_upload_success_continue(
                'cbtest', sender_id, attachment_link)
            # save_attachments('cbtest', sender_id, attachment_link)
    else:
        pass
