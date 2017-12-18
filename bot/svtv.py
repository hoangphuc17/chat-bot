import datetime
import random

from messenger_platform.messenger_api import Attachment, Template
from messenger_platform.messenger_api.payload import *

from messenger_platform.config.config import CONFIG
from messenger_platform.messenger_api.payload import *

from messenger_platform.config.fbpage import svtv
from core.db import *

from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
FAQ = db.FAQ
NEWS = db.NEWS

# BASIC
# svtv_home
# svtv_greeting

# UPLOAD
# svtv_menu_upload
# svtv_implement_upload
# svtv_upload_success_continue

# NEWS
# svtv_get_news

# QUANG CAO
# svtv_ads


def svtv_greeting(sender_id):
    user_profile = svtv.get_user_profile(sender_id)
    first = user_profile["first_name"]
    last = user_profile["last_name"]

    check_customer_by_id('svtv', sender_id)
    print(sender_id)
    text = 'chao'
    buttons = [
        Template.ButtonPostBack(
            "Home", "svtv_home")
    ]
    svtv.send(sender_id, Template.Buttons(text, buttons))


def svtv_home(sender_id):
    elements = [
        Template.GenericElement("Đóng góp hình ảnh",
                                subtitle="svtv",
                                # image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_tintuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Upload", "svtv_menu_upload")

                                ]),
        Template.GenericElement("Tin tức",
                                subtitle="svtv",
                                # image_url="http://210.211.109.211/weqbfyretnccbsaf/ttb_xemtintuc.jpg",
                                buttons=[
                                    Template.ButtonPostBack(
                                        "Xem tin tức", "svtv_get_news")
                                ])
    ]
    svtv.send(sender_id, Template.Generic(elements))


# UPLOAD
def svtv_menu_upload(sender_id):
    text = 'nhấn chọn nút ở dưới để bắt đầu quy trình upload'
    buttons = [
        Template.ButtonPostBack(
            "Upload", "svtv_implement_upload")
    ]
    svtv.send(sender_id, Template.Buttons(text, buttons))


def svtv_implement_upload(sender_id):
    # text = 'hãy chọn hình ảnh để upload cho'
    text = 'chọn hình và gửi'

    # update upload_status = yes
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id, 'upload_status': 'on'}}}
    )

    svtv.send(sender_id, text)


def svtv_upload_success_continue(chatbot, sender_id, attachment_link):
    # check upload status
    # save hình đó lại
    # hiển thị thông báo đã upload thành công
    # hỏi upload tiếp tục không
    cus = CUSTOMER.find_one({'id_user': sender_id})
    if bool(cus):
        if cus['SCRIPT']['upload_status'] == 'on':
            save_attachments(chatbot, sender_id, attachment_link)
            svtv.send(sender_id, 'da luu thanh cong')

    # check_upload_status = CUSTOMER.find_one({
    #     'SCRIPT': {'id_user': sender_id}
    # })

    # if bool(check_upload_status):
    #     save_attachments(chatbot, sender_id, attachment_link)
    #     svtv.send(sender_id, 'da luu hinh anh thanh cong')
    # else:
    #     svtv.send(sender_id, 'chua vao che do save')


# NEWS
def svtv_get_news(sender_id):
    elements = []
    news_list = []
    for news in NEWS.find({'chatbot': 'svtv'}):
        news_list.append(news)

    for news in news_list:
        element = Template.GenericElement(
            title=news['title'],
            subtitle=news['subtitle'],
            image_url=news['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', news['item_url']),
                Template.ButtonPostBack('Về Home', 'svtv_home')
            ])
        elements.append(element)

    short_list_elements = random.sample(elements, 5)
    svtv.send(sender_id, Template.Generic(short_list_elements))

    question = 'Xem thêm'
    quick_replies = [
        QuickReply(title="Xem thêm", payload="svtv_get_news")

    ]
    svtv.send(sender_id,
              question,
              quick_replies=quick_replies,
              metadata="DEVELOPER_DEFINED_METADATA")


def svtv_postback_handler(event):
    print('POSTBACK HANDLER svtv')
    sender_id = event.sender_id
    postback = event.postback_payload
    postback_list = {
        'svtv_greeting': svtv_greeting,
        'svtv_home': svtv_home,
        'svtv_menu_upload': svtv_menu_upload,
        'svtv_implement_upload': svtv_implement_upload,
        'svtv_get_news': svtv_get_news
    }

    if postback in postback_list:
        postback_list[postback](sender_id)


def svtv_message_handler(event):
    print('MESSAGE HANDLER svtv')
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload
    attachment_link = event.attachment_link

    message_list = {
        'hi': svtv_greeting,
        'home': svtv_home
    }
    # quickreply_list = {
    #     'giai_tri': svtv_get_news_giai_tri,
    #     'am_nhac': svtv_get_news_am_nhac
    # }

    if message is not None:
        message = message.lower()

        if message in message_list:
            message_list[message](sender_id)
        # elif quickreply in quickreply_list:
        #     quickreply_list[quickreply](sender_id)

    elif attachment_link is not None:
        if attachment_link != []:
            print(attachment_link)
            svtv.send(sender_id, 'thanks bro')
            svtv_upload_success_continue(
                'svtv', sender_id, attachment_link)
    else:
        pass
