# -*- coding: utf-8 -*-
import os
import sys

from ApiMessenger import Attachment, Template
from ApiMessenger.payload import QuickReply
from ApiMessenger.fbmq import Page

import CoreChatbot.Preparation.messenger
from CoreChatbot.Preparation.config import CONFIG

from CoreChatbot.Preparation.fbpage import cbtest
from CoreChatbot.cbtest.cbtest_database import *


import datetime
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
FAQ3 = db.FAQ3
FAQ4 = db.FAQ4


def home():
    elements = [
        Template.GenericElement('Tin Hot',
                                subtitle='Xem các tin tức hot từ saostar.vn',
                                image_url="",
                                buttons=[
                                    Template.ButtonPostBack(
                                        'Tin Hot 🔥', 'tin_hot')
                                ]),
        Template.GenericElement('Chuyên mục',
                                subtitle='Các chuyên mục từ saostar.vn',
                                image_url="",
                                buttons=[
                                    Template.ButtonPostBack(
                                        'Chuyên mục ➡', 'chuyen_muc')
                                ]),
        Template.GenericElement('Quảng cáo 🌎',
                                subtitle='Liên hệ quảng cáo',
                                image_url="",
                                buttons=[
                                    Template.ButtonPostBack(
                                        'Liên hệ quảng cáo', 'quang_cao')
                                ]),
        Template.GenericElement('Đóng góp',
                                subtitle='Đóng góp hình ảnh, video, tin tức',
                                image_url="",
                                buttons=[
                                    Template.ButtonPostBack(
                                        'Đóng góp hình ảnh', 'dong_gop_anh'),
                                    Template.ButtonPostBack(
                                        'Đóng góp video clip', 'dong_gop_video'),
                                    Template.ButtonPostBack(
                                        'Đóng góp tin tức', 'dong_gop_tin_tuc')
                                ])
    ]
    cbtest.send(sender_id, Template.Generic(elements))


def tin_hot():
    elements = []
    for news in NEWS.find():
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'home')
            ])
        elements.append(element)

    cbtest.send(sender_id, Template.Generic(elements))


def chuyen_muc():


def quang_cao():


def dong_gop_anh():


def dong_gop_video():


def dong_gop_tin_tuc():
