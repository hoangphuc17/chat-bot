# B1: em làm 1 keyword để xác định người đó muốn thực hiện chát
# B2: em lấy id của người muốn chát đó lưu vào db
# b3: vào db vừa lưu tìm xem có 1 id nào khác đang trống không
# nếu có thì tạo 1 cuộc nối chuyện giữa 2 id đó
# Làm 1 thông báo gửi đến 2 id để cho họ biết bắt đầu cuộc hội thoại
# B4: Mỗi khi nhặn tin nhắn từ id trong db thì kiểm tra xem có phải dấu hiệu kết thúc cuộc hội thoại không
# nếu không phải thì lấy nội dung tin nhắn của id đó gửi cho id cặp đôi
# Nếu là dấu hiệu kết thúc cuộc hội thoại thì xóa id đó và id cặp đôi ra khỏi db chát

# FLOW
# bat dau tim kiem
    # update chat_available = on
    # gui thong bao dang tim kiem
    # thuc hien ham tim kiem

# tim kiem
    # return partner

# bat dau chat
    # neu tim kiem duoc partner, thi gui thong bao bat dau chat
    

# chatting
# exit chat
    # xac dinh tu khoa

# HAM PHU
# check chat status
# new chatible



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

def new_chatible(chatbot, sender_id):
    new_chat_user = {
        'chatbot': chatbot,
        'id_user': sender_id,
        'chatting_with_user': '',
        'chatted_with_user': [],
        'message': [{
            'with_user': '',
            'message': '',
            'timestamp':  ''  
        }]
    }
    CHATIBLE.insert_one(new_chat_user)


def exit_chatible(chatbot, sender_id):
    print('ket thuc cuoc tro chuyen, cap nhat chat_status, chatted_user')
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT.chatting_status': 'no', 'SCRIPT.searching_status': 'no'}}
    )

    chatting_with_user = CHATIBLE.find_one({'id_user': sender_id})
    CHATIBLE.update_one(
        {'id_user': sender_id},
        {'$push': {'chatted_with_user': chatting_with_user['chatting_with_user']}},
        {'$set': {'chatting_with_user': ''}}
    )


def check_chatting_status(sender_id):
    chatting_status = CUSTOMER.find_one({'id_user': sender_id, 'SCRIPT.chatting_status': 'yes'})
    if bool(chatting_status):
        print('tin nhan cua nguoi dang su dung tinh nang CHATIBLE')
        return True
    else:
        print('day la tin nhan binh thuong')
        return False
        

def start_to_chat(chatbot, chatible_customer, chatible_partner):
    mess = 'Đã tìm thấy, hãy gửi tin nhắn'
    bot_chatible_dict[chatbot].send(chatible_customer, mess)
    bot_chatible_dict[chatbot].send(chatible_partner, mess)

    CUSTOMER.update_one(
        {'id_user': chatible_customer},
        {'$set': {'SCRIPT.chatting_status': 'yes', 'SCRIPT.searching_status': 'no'}}
    )

    CHATIBLE.update_one(
        {'id_user': chatible_customer},
        {'$set': {'chatting_with_user': chatible_partner}}
    )

    CUSTOMER.update_one(
        {'id_user': chatible_partner},
        {'$set': {'SCRIPT.chatting_status': 'yes', 'SCRIPT.searching_status': 'no'}}
    )

    CHATIBLE.update_one(
        {'id_user': chatible_partner},
        {'$set': {'chatting_with_user': chatible_customer}}
    )

    
def chat(chatbot, sender_id, message):
    chatty = CHATIBLE.find_one({'id_user': sender_id})
    partner = chatty['chatting_with_user']

    bot_chatible_dict[chatbot].send(partner, message)

    CHATIBLE.update_one(
        {'id_user': sender_id},
        {'$push': {'message': {
            'with_user': partner,
            'message': message,
            'timestamp': datetime.datetime.now()
        }}}
    )


def search(chatbot, sender_id):
    check_customer_in_chatible_database = CHATIBLE.find_one({'id_user': sender_id})
    if bool(check_customer_in_chatible_database):
        pass
    else:
        new_chatible(chatbot, sender_id)
    
    array_searching_partner = []
    cursor_searching_partner = CUSTOMER.find({'SCRIPT.searching_partner': 'yes'})
    for searching_partner in cursor_searching_partner:
        array_searching_partner.append(searching_partner)

    chatible_partner = ''
    if array_searching_partner != []:
        chatible_customer = CHATIBLE.find_one({'id_user': sender_id})
        for partner in array_searching_partner:
            if partner['id_user'] not in chatible_customer['chatted_with_user']:
                chatible_partner = partner['id_user']
                break
        if chatible_partner != '':
            start_to_chat(chatbot, chatible_customer, chatible_partner)
        else:
            print('da chat voi tat ca moi nguoi trong danh sach searching partner, cap nhat searching_partner = yes')
            CUSTOMER.update_one(
                {'id_user': sender_id},
                {'$set': {'SCRIPT.searching_partner': 'yes'}}
            )
    else:
        print('array searching partner = [], cap nhat searching_partner = yes')
        CUSTOMER.update_one(
            {'id_user': sender_id},
            {'$set': {'SCRIPT.searching_partner': 'yes'}}
        )
    


