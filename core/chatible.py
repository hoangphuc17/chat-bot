# # B1: em làm 1 keyword để xác định người đó muốn thực hiện chát
# # B2: em lấy id của người muốn chát đó lưu vào db
# # b3: vào db vừa lưu tìm xem có 1 id nào khác đang trống không
# # nếu có thì tạo 1 cuộc nối chuyện giữa 2 id đó
# # Làm 1 thông báo gửi đến 2 id để cho họ biết bắt đầu cuộc hội thoại
# # B4: Mỗi khi nhặn tin nhắn từ id trong db thì kiểm tra xem có phải dấu hiệu kết thúc cuộc hội thoại không
# # nếu không phải thì lấy nội dung tin nhắn của id đó gửi cho id cặp đôi
# # Nếu là dấu hiệu kết thúc cuộc hội thoại thì xóa id đó và id cặp đôi ra khỏi db chát

from messenger_platform.messenger_api import Attachment, Template
from messenger_platform.messenger_api.payload import *

from messenger_platform.config.config import CONFIG
from messenger_platform.messenger_api.payload import *

from messenger_platform.config.fbpage import svtv,saostar

import datetime
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
CUSTOMER = db.CUSTOMER
CHATIBLE = db.CHATIBLE

bot_chatible_dict = {
    'saostar': saostar,
    'svtv': svtv
}

def new_chatible(chatbot, sender_id, user2):
    new_chat_user = {
        'chatbot': chatbot,
        'id_user': sender_id,
        'chatting_with_user': user2,
        'message': {
            'with_user': '',
            'message': '',
            'timestamp':  ''  
        }
    }
    CHATIBLE.insert_one(new_chat_user)

def chatible_tim_kiem(chatbot, sender_id):
    available_customer = CUSTOMER.find_one({'SCRIPT.chat_available': 'yes'})    

    if bool(available_customer):
        user2 = available_customer['id_user']

        new_chatible(chatbot, sender_id, user2)
        new_chatible(chatbot, user2, sender_id)
        
        bot_chatible_dict[chatbot].send(sender_id, 'Đã tìm thấy bạn, hãy gửi tin nhắn')

        CUSTOMER.update_one(
            {'id_user': sender_id},
            {'$set': {'SCRIPT.chat_status': 'on'}}
        )

    else:
        print('khong co nguoi nao de chat')


def chatible_bat_dau(chatbot, sender_id):
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT.chat_available': 'yes'}}
    )

    bot_chatible_dict[chatbot].send(sender_id, 'Đang tìm kiếm bạn')

    chatible_tim_kiem(chatbot, sender_id)


def chatible_chatting(chatbot, sender_id, message):
    chatty = CHATIBLE.find_one({'id_user': sender_id})
    user2 = chatty['chatting_with_user']

    bot_chatible_dict[chatbot].send(user2, message)

    CHATIBLE.update_one(
        {'id_user': sender_id},
        {'$set': {'message.with_user': user2, 'message.message': message, 'message.timestamp': datetime.datetime.now()}}
    )


def exit_chatible(chatbot, sender_id):
    print('ket thuc cuoc tro chuyen')
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT.chat_status': 'off'}}
    )


def check_chatible_status(sender_id):
    check_chat_status = CUSTOMER.find_one({'id_user': sender_id, 'SCRIPT.chat_status': 'on'})
    if bool(check_chat_status):
        print('xu ly tin nhan chatible')
        return True
    else:
        print('xu ly tin nhan binh thuong')
        return False
        



