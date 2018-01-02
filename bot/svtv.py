import datetime
import random

from messenger_platform.messenger_api import Attachment, Template
from messenger_platform.messenger_api.payload import *

from messenger_platform.config.config import CONFIG
from messenger_platform.messenger_api.payload import *

from messenger_platform.config.fbpage import svtv
from core.db import *
from core.chatible import *

from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
FAQ = db.FAQ
NEWS = db.NEWS

# BASIC
# svtv_home
# svtv_greeting
# svtv_default_message

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
    text = 'Chào ' + first + ' ' + last + \
        '. Nhấn nút home bên dưới để tìm hiểu các tính năng Sinh viên TV có nhé'
    buttons = [
        Template.ButtonPostBack(
            "HOME", "svtv_home")
    ]
    svtv.send(sender_id, Template.Buttons(text, buttons))

def svtv_default_message(sender_id):
    text = 'Chào bạn! Sinh Viên TV có thể giúp gì cho bạn?'
    buttons = [
        Template.ButtonPostBack(
            "HOME", "svtv_home")
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
                                        "Xem tin tức", "svtv_get_news"),
                                    Template.ButtonPostBack(
                                        "Theo dõi tin tức", "svtv_menu_subscribe")
                                ])
    ]
    svtv.send(sender_id, Template.Generic(elements))


# UPLOAD
def svtv_menu_upload(sender_id):
    # text = 'nhấn chọn nút ở dưới để bắt đầu quy trình upload'
    text = 'Chào bạn, bạn muốn đóng góp nội dung gì cho Sinh Viên TV? Chọn nút bên dưới để bắt đầu Upload'
    buttons = [
        Template.ButtonPostBack(
            "Upload", "svtv_implement_upload")
    ]
    svtv.send(sender_id, Template.Buttons(text, buttons))


def svtv_implement_upload(sender_id):
    # text = 'hãy chọn hình ảnh để upload cho'
    text = 'hãy chọn 📷Ảnh – 🎬Video'

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

            text = 'Cảm ơn bạn đã đóng góp cho Sinh Viên TV nhé!'
            buttons = [
                Template.ButtonPostBack(
                    "HOME", "svtv_home")
            ]
            svtv.send(sender_id, Template.Buttons(text, buttons))
            
            # svtv.send(sender_id, 'da luu thanh cong')

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


# QUANG CAO
def svtv_ads(sender_id):
    text = 'Liên hệ hợp tác quảng cáo & xuất bản nội dung: sinhvientv.channel@gmail.com\nhoặc Hotline: 097.674.6263 (Mr Dương).'
    buttons = [
        Template.ButtonPostBack(
            "Home", "svtv_home")
    ]
    svtv.send(sender_id, Template.Buttons(text, buttons))


# SUBSCRIBE NEWS
def svtv_menu_subscribe(sender_id):
    question = "Bằng cách đồng ý theo dõi tin tức dưới đây, bạn sẽ nhận được thông báo mỗi khi tin tức mới của chương trình được cập nhật.\nBạn muốn nhận thông báo chứ?"
    quick_replies = [
        QuickReply(title="1 tuần 1 lần 😋", payload="yes1"),
        QuickReply(title="1 tuần 2 lần 😈", payload="yes2"),
        QuickReply(title="Nhắc lại sau 😜", payload="no")
    ]
    svtv.send(sender_id,
             question,
             quick_replies=quick_replies,
             metadata="DEVELOPER_DEFINED_METADATA")


def svtv_handle_subscribe(sender_id, quick_reply_payload):
    if quick_reply_payload == 'no':
        text = "Okey. Bất cứ khi nào bạn cần đăng ký nhận tin tức thì quay lại đây nhé!"
        buttons = [
            Template.ButtonPostBack("HOME", "svtv_home")
        ]
        svtv.send(sender_id, Template.Buttons(text, buttons))

        user = CUSTOMER.find_one({'id_user': sender_id})
        new_script = {
            'upload_status': user['SCRIPT']['upload_status'],
            'subscribe': quick_reply_payload
        }
        CUSTOMER.update_one(
            {'id_user': sender_id},
            {'$set': {'SCRIPT': new_script}}
        )
    else:
        text = "Bạn đã đăng ký nhận thông báo thành công.\nMỗi khi có thông báo mới về chương trình, mình sẽ gửi tới bạn."
        buttons = [
            Template.ButtonPostBack("HOME", "svtv_home")
        ]
        svtv.send(sender_id, Template.Buttons(text, buttons))

        user = CUSTOMER.find_one({'id_user': sender_id})
        new_script = {
            'upload_status': user['SCRIPT']['upload_status'],
            'subscribe': quick_reply_payload
        }
        CUSTOMER.update_one(
            {'id_user': sender_id},
            {'$set': {'SCRIPT': new_script}}
        )



# HANDLE POSTBACK AND MESSAGE
def svtv_postback_handler(event):
    print('POSTBACK HANDLER svtv')
    sender_id = event.sender_id
    postback = event.postback_payload
    postback_list = {
        'svtv_greeting': svtv_greeting,
        'svtv_home': svtv_home,
        # 'svtv_menu_upload': svtv_menu_upload,
        # 'svtv_implement_upload': svtv_implement_upload,
        'svtv_get_news': svtv_get_news,
        'svtv_ads': svtv_ads,
        'svtv_menu_subscribe': svtv_menu_subscribe

    }

    if postback in postback_list:
        postback_list[postback](sender_id)


def svtv_message_handler(event):
    print('MESSAGE HANDLER svtv')
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload
    attachment_link = event.attachment_link

    subscribe_options = ["yes1", "yes2", "no"]

    message_list = {
        'hi': svtv_greeting,
        'home': svtv_home
    }
    quickreply_list = {
        'svtv_get_news': svtv_get_news
    }

    if message is not None:
        message = message.lower()
        if check_chatible_status(sender_id):
            chatible_bat_dau(chatbot, sender_id)
        else:
            if message in message_list:
                message_list[message](sender_id)
            elif quickreply in quickreply_list:
                quickreply_list[quickreply](sender_id)
            # xu ly subscribe option
            elif subscribe_options.count(quickreply) == 1:
                svtv_handle_subscribe(sender_id, quickreply)
            else:
                svtv_default_message(sender_id)

    elif attachment_link is not None:
        if attachment_link != []:
            print(attachment_link)
            svtv_upload_success_continue(
                'svtv', sender_id, attachment_link)
    else:
        pass
