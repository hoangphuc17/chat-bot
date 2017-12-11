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

from messenger_platform.config.fbpage import cbtest
from core.db import *

import datetime
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
USER = db.CDHH_USER
FAQ = db.CDHH_FAQ
NEWS = db.CDHH_NEWS

# cbtest_home
# cbtest_greeting

# cbtest_menu_upload
# cbtest_implement_upload
# cbtest_upload_success_continue

# cbtest_get_news_general
# cbtest_get_news_giai_tri
# cbtest_get_news_am_nhac


# list_category = {
#     'giải trí': cbtest_get_news_giai_tri
# }


def cbtest_greeting(sender_id):
    user_profile = cbtest.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]
    check_customer_by_id('cbtest', sender_id)

    text = 'chao'
    buttons = [
        Template.ButtonPostBack(
            "Home", "cbtest_home")
    ]
    ghvn.send(sender_id, Template.Buttons(text, buttons))


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


def cbtest_implement_upload():
    text = 'hãy chọn hình ảnh để upload cho'
    text = 'chọn hình và gửi'

    # update upload_status = yes
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id, 'upload_status': 'on'}}}
    )


def cbtest_upload_success_continue(sender_id, attachment_link):
    # check upload status
    # save hình đó lại
    # hiển thị thông báo đã upload thành công
    # hỏi upload tiếp tục không
    check_upload_status = CUSTOMER.find_one({
        'SCRIPT': {'id_user': sender_id}
    })

    if bool(check_upload_status):
        save_attachments('cbtest', sender_id, attachment_link)
        cbtest.send(sender_id, 'da luu hinh anh thanh cong')
    else:
        cbtest.send(sender_id, 'chua vao che do save')


# NEWS
# def cbtest_get_news_general():


# def cbtest_get_news_giai_tri():


# def cbtest_get_news_am_nhac():


def cbtest_postback_handler(event):
    print('POSTBACK HANDLER CBTEST')
    sender_id = event.sender_id
    postback = event.postback_payload
    postback_list = {
        'cbtest_upload_image': cbtest_upload_image,
        'cbtest_home': cbtest_home
    }

    if postback in postback_list:
        postback_list[postback](sender_id)


def cbtest_message_handler(event):
    print('MESSAGE HANDLER CBTEST')
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload
    attachment_link = event.attachment_link

    if attachment_link is not None:
        if attachment_link != []:
            print(attachment_link)
            cbtest.send(sender_id, 'thanks bro')
            save_attachments('cbtest', sender_id, attachment_link)
    elif message is not None:
        message = message.lower()
        message_list = {
            'up': cbtest_upload_image_menu,
            'hi': cbtest_greeting
        }
        if message in message_list:
            message_list[message](sender_id)
    else:
        pass
