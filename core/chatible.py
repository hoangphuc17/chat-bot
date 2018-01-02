# # B1: em làm 1 keyword để xác định người đó muốn thực hiện chát
# # B2: em lấy id của người muốn chát đó lưu vào db
# # b3: vào db vừa lưu tìm xem có 1 id nào khác đang trống không
# # nếu có thì tạo 1 cuộc nối chuyện giữa 2 id đó
# # Làm 1 thông báo gửi đến 2 id để cho họ biết bắt đầu cuộc hội thoại
# # B4: Mỗi khi nhặn tin nhắn từ id trong db thì kiểm tra xem có phải dấu hiệu kết thúc cuộc hội thoại không
# # nếu không phải thì lấy nội dung tin nhắn của id đó gửi cho id cặp đôi
# # Nếu là dấu hiệu kết thúc cuộc hội thoại thì xóa id đó và id cặp đôi ra khỏi db chát

import datetime
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc
CUSTOMER = db.CUSTOMER
CHATIBLE = db.CHATIBLE

def new_chatible(chatbot, usera, userb):
    new_chat = {
        'chatbot': chatbot,
        'id_user_A': usera,
        'id_user_B': userb
        'message': {
            'sender_id': 
            'message': 
            'timestamp':    
        }
    }
    CHATIBLE.insert_one(new_chat_user)


def chatible(chatbot, sender_id):
    available_customer = CUSTOMER.find_one({'chat_available': 'yes'})    
    if bool(available_customer):
        userb = available_customer['id_user']
        new_chatible(chatbot, sender_id, userb)

    else:
        print('khong co nguoi nao de chat')


def exit_chatible(chatbot, sender_id, message):
    if message == 'pp':
        print('ket thuc cuoc tro chuyen')
        

