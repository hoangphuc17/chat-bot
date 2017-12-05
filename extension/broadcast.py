# -*- coding: utf-8 -*-
import os
import sys
import threading
from ApiMessenger import Attachment, Template
from ApiMessenger.payload import QuickReply
from ApiMessenger.fbmq import Page
import CoreChatbot.Preparation.messenger
from CoreChatbot.Preparation.config import CONFIG
from CoreChatbot.Preparation.fbpage import page
from CoreChatbot.TheVoiceKid.database import *


import datetime
import time
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
USER = db.USER
FAQ = db.FAQ
NEWS = db.NEWS

id_phuc = "1588973231176132"
id_phuc2 = "1370330196399177"
id_chau = "1318278091631838"
id_duc = "1627683190629761"
url = "http://210.211.109.211/weqbfyretnccbsaf/"


def broadcast_message(sender_id, text):
    buttons = [
        Template.ButtonPostBack("Home", "home")
    ]
    page.send(sender_id, Template.Buttons(text, buttons))


def broadcast_message_link_button(sender_id, text, link):
    buttons = [
        Template.ButtonWeb('👉 Xem tiết mục', link),
        Template.ButtonPostBack("Home", "home")
    ]
    page.send(sender_id, Template.Buttons(text, buttons))


def broadcast_image(sender_id, image_name):
    page.send(sender_id, Attachment.Image(url + image_name))


def broadcast_video(sender_id, video_name):
    page.send(sender_id, Attachment.Video(url + video_name))


def broadcast(list_user_broadcast):
    # broadcast_image(id_phuc2, "broadcast0111.jpg")
    # text = "Chào tháng 11, tháng của những yêu thương ngọt ngào, tháng chuyển mình khi đông tới. Nếu sợ lẻ loi khi đông về hãy để Giọng Hát Việt Nhí mang tới cho bạn những lời ca thật ấm, bài hát thật hay 💖💖💖\nĐừng quên đón xem Tập 12 đầy cảm xúc vào lúc 21h00 Thứ Bảy Ngày 4/11/2017 trên kênh VTV3 các bạn nhé!"
    # broadcast_message(id_phuc2, text)

    for id_user in list_user_broadcast:
        # broadcast_image(id_user, "broadcast0111.jpg")
        text = "Cổng bình chọn Chiếc vé may mắn sẽ đóng lại vào lúc 12h trưa ngày 19/11/2017 và kết quả sẽ được công bố trên fanpage của chương trình.\nVà đặc biệt, ở mùa giải năm nay, mỗi đội sẽ có 1 chiếc vé may mắn, đồng nghĩa là sẽ có thêm 3 gương mặt quay trở lại đêm chung kết!!\nHÃY BÌNH CHỌN CHO THÍ SINH XUẤT SẮC CỦA CHÚNG TA NHÉ!!\n✔Và đừng quên đón xem BÁN KẾT vào tối nay 21h30 trên kênh VTV3 cùng với top 6 sẽ biểu diễn cùng Đông Nhi, Đức Phúc, Ali Hoàng Dương nhé! ❤"
        broadcast_message(id_user, text)
        print('Co ', len(list_user_broadcast), ' user')
        print('Da gui broadcast cho user thu:',
              list_user_broadcast.index(id_user))


# get user from database USER
list_user = []
for user in USER.find():
    list_user.append(user['id_user'])


# chia user thanh n groups
def partition(lst, n):
    division = len(lst) / n
    return [lst[round(division * i):round(division * (i + 1))]
            for i in range(n)]


list_thread = []
list_group_user = partition(list_user, 100)

for group in list_group_user:
    thread = threading.Thread(target=broadcast, args=(group,))
    list_thread.append(thread)

second = time.time()

for t in list_thread:
    t.start()

for t in list_thread:
    t.join()


minutes = (time.time() - second) / 60
print('Done in:', minutes, 'minutes')
