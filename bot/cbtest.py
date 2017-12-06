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


def cbtest_upload_image_menu(sender_id):
    # hiện thị menu để upload
    # chuyển trạng thái người dùng sang đang upload hình ảnh
    text = 'upload image to server'
    buttons = [
        Template.ButtonPostBack(
            "Upload", "cbtest_upload_image")
    ]
    cdhh.send(sender_id, Template.Buttons(text, buttons))

    CUSTOMER.update_one()


def cbtest_upload_image_implement(sender_id):
    # 1. kiểm tra trạng thái có phải là đang cho upload hình vào hay không

    # 2. nếu ok thì sẽ lưu link đó lại
    print('a')


# def cbtest_attachments_handler(event):
#     # event.att
#     event.
#     print('aaaaaaaaaa')


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
        print(attachment_link)
        cbtest.send(sender_id, 'thanks bro')

    if message is not None:
        message = message.lower()
        message_list = {
            'up': cbtest_upload_image_menu,
            'hi': cbtest_greeting
        }
    else:
        pass
