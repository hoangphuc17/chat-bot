# xử lý các vấn đề liên quan tới lưu, xoá, insert database
from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash

from messenger_platform.messenger_api import Attachment, Template
# from messenger_platform.messenger_api import QuickReply
# from messenger_platform.messenger_api import Page

from messenger_platform.config.config import CONFIG

from messenger_platform.config.fbpage import ghvn, cdhh, cbtest, saostar, ttb

import datetime
from pymongo import MongoClient
client = MongoClient('cb.saostar.vn', 27017)
db = client.Phuc

FAQ = db.FAQ
NEWS = db.NEWS
CUSTOMER = db.CUSTOMER
BROADCAST = db.BROADCAST
CONVERSATION = db.CONVERSATION

CONTRIBUTION = db.CONTRIBUTION


bot_dict = {
    'ghvn': ghvn,
    'cdhh': cdhh,
    'cbtest': cbtest,
    'saostar': saostar,
    'ttb': ttb

}


# CONTRIBUTION
def save_attachments(chatbot, sender_id, link):
    check_cus = CONTRIBUTION.find_one({'id_user': sender_id})
    if bool(check_cus):
        CONTRIBUTION.update_one(
            {'id_user': sender_id},
            {'$push': {'links': {'link': link, 'timestamp': datetime.datetime.now()}}}
        )
    else:
        new_contribution = {
            'chatbot': chatbot,
            'id_user': sender_id,
            'links': [{
                'link': link,
                'timestamp': datetime.datetime.now()
            }]
        }
        CONTRIBUTION.insert_one(new_contribution)


# CONVERSATION
def save_mess(chatbot, sender_id, mess):
    if check_customer_by_id(chatbot, sender_id):
        # update document
        CONVERSATION.update_one(
            {'id_user': sender_id},
            {'$push': {'message': {'content': mess,
                                   'timestamp': datetime.datetime.now()}}}
        )
    else:
        new_mess = {
            'chatbot': chatbot,
            'id_user': sender_id,
            'mess': [{
                'content': mess,
                'timestamp': datetime.datetime.now()
            }]
        }
        CONVERSATION.insert_one(new_mess)


# def save_message(sender_id, message):
#     user_profile = page.get_user_profile(sender_id)
#     first = user_profile["first_name"]
#     last = user_profile["last_name"]
#     id_user = user_profile["id"]

#     if message is not None:
#         check_user = USER.find_one({'id_user': sender_id})
#         if bool(check_user):
#             print("Day la ham save_message(). User da co trong database")
#         else:
#             insert_new_user(first, last, id_user)

        # USER.update_one(
        #     {'id_user': sender_id},
        #     {'$push': {'message': {'content': message,
        #                            'time': datetime.datetime.now()}}}
        # )
#     else:
#         pass


# CUSTOMER
def ghvn_customer(sender_id):
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id,
                             'subscribe_news': 'no', 'HLV_da_binh_chon': ''}}}
    )


def cdhh_customer(sender_id):
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id, 'subscribe': 'no', 'vote': ''}}}
    )


def ttb_customer(sender_id):
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id, 'subscribe': 'no', 'vote': ''}}}
    )


def cbtest_customer(sender_id):
    CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id, 'upload_status': 'off'}}}
    )


bot_customer_dict = {
    'ghvn': ghvn_customer,
    'cdhh': cdhh_customer,
    'cbtest': cbtest_customer,
    'ttb': ttb_customer
}


def add_customer(chatbot, id_user, first_name, last_name, gender):
    new_customer = {
        'id_user': id_user,
        'chatbot': chatbot,
        'ATTRIBUTES': {
            'chatbot': chatbot,
            'id_user': id_user,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'address': '',
            'birthday': '',
            'education': '',
            'relationship_status': '',
            'family_member': '',
            'workplace': '',
            'university': '',
            'high_school': ''
        },
        'FRIENDS': [
            # ban be thuong xuyen nhan tin
            {
                'id_friend': '',
                'name': '',
                'so_luong_tin_nhan': '',
                'muc_do_than_thiet': ''
            }
        ],
        'TALKLINES': {
            'chatbot': '',
            'time': '',
            'message': '',
            'bot_message_previous': '',
            'bot_message_next': ''

        },
        'HOBBIES': {
            'sport': [{
                'rate': '',
                'details': [{
                    'football': '',
                    'tennis': ''
                }]
            }],
            'entertainment': [{
                'rate': '',
                'details': [{
                    'music': '',
                    'film': ''
                }]
            }],
            'travelling': [{
                'rate': '',
                'details': [{
                    'place': ''
                }]
            }],
            'politic': ''
        },
        'ADVERTISEMENT': {
            'clicked_ads': ''
        }
    }
    CUSTOMER.insert_one(new_customer)


def update_info_customer(sender_id, info, value):
    check_customer = CUSTOMER.find_one({'id_user': sender_id})
    if bool(check_customer):
        return False
    else:
        CUSTOMER.update_one(
            {'id_user': sender_id},
            {'$set': {info: value}}
        )
        return True


def check_customer_by_id(chatbot, sender_id):
    if chatbot in bot_dict:
        user_profile = bot_dict[chatbot].get_user_profile(sender_id)
        first_name = user_profile["first_name"]
        last_name = user_profile["last_name"]
        gender = user_profile["gender"]

        found_customer = CUSTOMER.find_one({'id_user': sender_id})
        # found_customer = CUSTOMER.find_one(
        #     {'ATTRIBUTES': {'id_user': sender_id}})
        if bool(found_customer):
            print(last_name, first_name, 'is already in database')

        else:
            print('khong tim thay user')
            add_customer(chatbot, sender_id, first_name, last_name, gender)
            if chatbot in bot_customer_dict:
                bot_customer_dict[chatbot](sender_id)


def get_customer_by_id(sender_id):
    found_customer = CUSTOMER.find_one({'id_user': sender_id})
    if bool(found_customer):
        return found_customer
    else:
        return False


# NEWS
def add_news(chatbot, title, subtitle, image_url, item_url):
    check_news = NEWS.find_one({'item_url': item_url})
    if bool(check_news):
        return False
    else:
        new_news = {
            'chatbot': chatbot,
            'title': title,
            'subtitle': subtitle,
            'image_url': image_url,
            'item_url': item_url
        }
        NEWS.insert_one(new_news)
        return True


def delete_news(chatbot, item_url):
    check_news = NEWS.find_one({'item_url': item_url, 'chatbot': chatbot})
    if bool(check_news):
        return False
    else:
        NEWS.delete_many({'item_url': item_url, 'chatbot': chatbot})
        return True


def get_all_news(chatbot, item_url):
    cursor_all_news = NEWS.find({'item_url': item_url, 'chatbot': chatbot})
    all_news = []
    for item in cursor_all_news:
        all_news.append(item)
    return jsonify({'result': all_news})


# BROADCAST
# text
def send_message_broadcast(chatbot, message):
    cursor_list_customer = CUSTOMER.find({'chatbot': chatbot})
    list_customer = []
    for item in cursor_list_customer:
        list_customer.append(item)
    for customer in list_customer:
        chatbot.send(customer['id_user'], message)


def save_message_broadcast(chatbot, content, timestamp):
    new_broadcast = {
        'chatbot': chatbot,
        'type_message': 'text',
        'content': content,
        'timestamp': timestamp
    }
    BROADCAST.insert_one(new_broadcast)


def send_and_save_message_broadcast(chatbot, message, content, timestamp):
    # send
    cursor_list_customer = CUSTOMER.find({'chatbot': chatbot})
    list_customer = []
    for item in cursor_list_customer:
        list_customer.append(item)
    for customer in list_customer:
        chatbot.send(customer['id_user'], message)
    # save
    new_broadcast = {
        'chatbot': chatbot,
        'type_message': 'text',
        'content': content,
        'timestamp': timestamp
    }
    BROADCAST.insert_one(new_broadcast)


# image
def send_image_broadcast(chatbot, image_url):
    cursor_list_customer = CUSTOMER.find({'chatbot': chatbot})
    list_customer = []
    for item in cursor_list_customer:
        list_customer.append(item)
    for customer in list_customer:
        chatbot.send(customer['id_user'], Attachment.Image(image_url))


def save_image_broadcast(chatbot, image_url, timestamp):
    new_broadcast = {
        'chatbot': chatbot,
        'type_message': 'image',
        'content': image_url,
        'timestamp': timestamp
    }
    BROADCAST.insert_one(new_broadcast)


def send_and_save_image_broadcast(chatbot, message, image_url, timestamp):
    # send
    cursor_list_customer = CUSTOMER.find({'chatbot': chatbot})
    list_customer = []
    for item in cursor_list_customer:
        list_customer.append(item)
    for customer in list_customer:
        chatbot.send(customer['id_user'], message)
    # save
    new_broadcast = {
        'type_message': 'image',
        'content': image_url,
        'timestamp': timestamp
    }
    BROADCAST.insert_one(new_broadcast)


class Node:
    def __init__(self, chatbot, level, id_node, list_id_node_parents, list_keyword, answer):
        self.chatbot = chatbot
        self.level = level
        self.id_node = id_node
        self.list_id_node_parents = list_id_node_parents
        self.list_keyword = list_keyword
        self.answer = answer

    # def find_node_in_message():

    # def find_branch():

    # def check_a_perfect_branch():

    # def get_answer():
