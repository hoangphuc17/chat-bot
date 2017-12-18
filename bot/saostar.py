import datetime
import random

from messenger_platform.messenger_api import Attachment, Template
from messenger_platform.messenger_api.payload import *

from messenger_platform.config.config import CONFIG
from messenger_platform.messenger_api.payload import *

from messenger_platform.config.fbpage import saostar
from core.db import *

from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
FAQ = db.FAQ
NEWS = db.NEWS

# BASIC
# saostar_home
# saostar_greeting

# UPLOAD
# saostar_menu_upload
# saostar_implement_upload
# saostar_upload_success_continue

# NEWS
# saostar_get_news_general
# saostar_get_news_giai_tri
# saostar_get_news_am_nhac
# saostar_get_news_phim_anh
# saostar_get_news_xa_hoi
# saostar_get_news_thoi_trang

# QUANG CAO
# saostar_ads


def saostar_greeting(sender_id):
    user_profile = saostar.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]

    check_customer_by_id('saostar', sender_id)
    print(sender_id)
    text = 'Chào ' + first + ' ' + last + \
        '. Nhấn nút home bên dưới để tìm hiểu các tính năng Saostar có nhé'
    buttons = [
        Template.ButtonPostBack(
            "Home", "saostar_home")
    ]
    saostar.send(sender_id, Template.Buttons(text, buttons))


def saostar_home(sender_id):
    elements = [
        Template.GenericElement("Đóng góp hình ảnh",
                                subtitle="Saostar",
                                # image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_tintuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Upload", "saostar_menu_upload")

                                ]),
        Template.GenericElement("Tin tức",
                                subtitle="Saostar",
                                # image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_xemtintuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Xem tin tức", "saostar_get_news_general")
                                ])
    ]
    saostar.send(sender_id, Template.Generic(elements))


# UPLOAD
def saostar_menu_upload(sender_id):
    text = 'nhấn chọn nút ở dưới để bắt đầu quy trình upload'
    buttons = [
        Template.ButtonPostBack(
            "Upload", "saostar_implement_upload")
    ]
    saostar.send(sender_id, Template.Buttons(text, buttons))


def saostar_implement_upload(sender_id):
    # text = 'hãy chọn hình ảnh để upload cho'
    text = 'chọn hình và gửi'

    # update upload_status = yes
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id, 'upload_status': 'on'}}}
    )

    saostar.send(sender_id, text)


def saostar_upload_success_continue(chatbot, sender_id, attachment_link):
    # check upload status
    # save hình đó lại
    # hiển thị thông báo đã upload thành công
    # hỏi upload tiếp tục không
    cus = CUSTOMER.find_one({'id_user': sender_id})
    if bool(cus):
        if cus['SCRIPT']['upload_status'] == 'on':
            save_attachments(chatbot, sender_id, attachment_link)
            saostar.send(sender_id, 'da luu thanh cong')

    # check_upload_status = CUSTOMER.find_one({
    #     'SCRIPT': {'id_user': sender_id}
    # })

    # if bool(check_upload_status):
    #     save_attachments(chatbot, sender_id, attachment_link)
    #     saostar.send(sender_id, 'da luu hinh anh thanh cong')
    # else:
    #     saostar.send(sender_id, 'chua vao che do save')


# NEWS
def saostar_get_news_general(sender_id):
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
                Template.ButtonPostBack('Về Home', 'saostar_home')
            ])
        elements.append(element)

    short_list_elements = random.sample(elements, 5)
    saostar.send(sender_id, Template.Generic(short_list_elements))

    question = 'Xem thêm'
    quick_replies = [
        QuickReply(title="Giải trí", payload="giai_tri"),
        QuickReply(title="Âm nhạc", payload="am_nhac"),
        QuickReply(title="Xem thêm", payload="xem_them")

    ]
    saostar.send(sender_id,
                 question,
                 quick_replies=quick_replies,
                 metadata="DEVELOPER_DEFINED_METADATA")


def saostar_get_news_giai_tri(sender_id):
    elements = []
    news_list = []
    for news in NEWS.find({'chatbot': 'saostar', 'category': 'giai tri'}):
        news_list.append(news)

    for news in news_list:
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'saostar_home')
            ])
        elements.append(element)

    short_list_elements = random.sample(elements, 5)
    saostar.send(sender_id, Template.Generic(short_list_elements))

    question = 'Xem thêm'
    quick_replies = [
        QuickReply(title="Âm nhạc", payload="am_nhac")
    ]
    saostar.send(sender_id,
                 question,
                 quick_replies=quick_replies,
                 metadata="DEVELOPER_DEFINED_METADATA")


def saostar_get_news_am_nhac(sender_id):
    elements = []
    news_list = []
    for news in NEWS.find({'chatbot': 'saostar', 'category': 'am nhac'}):
        news_list.append(news)

    for news in news_list:
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'saostar_home')
            ])
        elements.append(element)

    short_list_elements = random.sample(elements, 5)
    saostar.send(sender_id, Template.Generic(short_list_elements))

    question = 'Xem thêm'
    quick_replies = [
        QuickReply(title="Giải trí", payload="giai_tri")
    ]
    saostar.send(sender_id,
                 question,
                 quick_replies=quick_replies,
                 metadata="DEVELOPER_DEFINED_METADATA")


# QUANG CAO
def saostar_ads(sender_id):
    text = 'Liên hệ hợp tác quảng cáo & xuất bản nội dung: marketing@saostar.vn ❤'
    buttons = [
        Template.ButtonPostBack(
            "Home", "saostar_home")
    ]
    saostar.send(sender_id, Template.Buttons(text, buttons))


def saostar_postback_handler(event):
    print('POSTBACK HANDLER saostar')
    sender_id = event.sender_id
    postback = event.postback_payload
    postback_list = {
        'saostar_greeting': saostar_greeting,
        'saostar_home': saostar_home,
        'saostar_menu_upload': saostar_menu_upload,
        'saostar_implement_upload': saostar_implement_upload,
        'saostar_get_news_general': saostar_get_news_general,
        'saostar_ads': saostar_ads
    }

    if postback in postback_list:
        postback_list[postback](sender_id)


def saostar_message_handler(event):
    print('MESSAGE HANDLER saostar')
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload
    attachment_link = event.attachment_link

    message_list = {
        'hi': saostar_greeting,
        'home': saostar_home
    }
    quickreply_list = {
        'giai_tri': saostar_get_news_giai_tri,
        'am_nhac': saostar_get_news_am_nhac
    }

    if message is not None:
        message = message.lower()

        if message in message_list:
            message_list[message](sender_id)
        elif quickreply in quickreply_list:
            quickreply_list[quickreply](sender_id)

    elif attachment_link is not None:
        if attachment_link != []:
            print(attachment_link)
            saostar.send(sender_id, 'thanks bro')
            saostar_upload_success_continue(
                'saostar', sender_id, attachment_link)
    else:
        pass
