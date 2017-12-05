# -*- coding: utf-8 -*-
import os
import sys

from ApiMessenger import Attachment, Template
from ApiMessenger.payload import QuickReply
from ApiMessenger.fbmq import Page

import CoreChatbot.Preparation.messenger
from CoreChatbot.Preparation.config import CONFIG
from CoreChatbot.Preparation.fbpage import page
# from CoreChatbot.TheVoiceKid.database import *

from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash
from flask_pymongo import PyMongo, ObjectId
import bcrypt
from werkzeug.utils import secure_filename
# import datetime
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'Phuc'
app.config['MONGO_URI'] = 'mongodb://cb.saostar.vn:27017/Phuc'
mongo = PyMongo(app)

UPLOAD_FOLDER = '/home/hoangphuc/Bot_Pictures'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# BROADCAST API: message, image, video, message+button, news
@app.route('/broadcast/message', methods=['POST'])
def broadcast_message():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        message = request.form['message']
        dt = request.form['timestamp']
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')

        # for user in USER.find():
        #     page.send(user['id_user'], message)

        page.send("1370330196399177", message)
        page.send("1437973719614452", message)

        # luu broadcast
        new_bc = {
            'type': 'message',
            'content': message,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)

        return 'True'
    else:
        return 'False'


@app.route('/broadcast/message_button', methods=['POST'])
def broadcast_message_button():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        # for user in USER.find():
        #     message = request.form['message']
        #     buttons = [
        #         Template.ButtonPostBack("Home", "home")
        #     ]
        #     page.send(user['id_user'], Template.Buttons(message, buttons))

        message = request.form['message']
        dt = request.form['timestamp']
        # 'Jun 1 2005  1:33PM'
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        buttons = [
            Templatsae.ButtonPostBack("Home", "home")
        ]
        page.send("1370330196399177", Template.Buttons(message, buttons))
        page.send("1437973719614452", Template.Buttons(message, buttons))
        # luu broadcast
        new_bc = {
            'type': 'message_button',
            'content': message,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)
        return 'True'
    else:
        return 'False'


@app.route('/broadcast/image', methods=['POST'])
def broadcast_image():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        url = request.form['url']
        dt = request.form['timestamp']
        # 'Jun 1 2005  1:33PM'
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        # for user in USER.find():
        #     page.send(user['id_user'], Attachment.Image(url))

        page.send("1370330196399177", Attachment.Image(url))
        page.send("1437973719614452", Attachment.Image(url))
        # luu broadcast
        new_bc = {
            'type': 'image',
            'content': url,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)
        return 'True'
    else:
        return 'False'


@app.route('/broadcast/video', methods=['POST'])
def broadcast_video(url):
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        url = request.form['url']
        dt = request.form['timestamp']
        # 'Jun 1 2005  1:33PM'
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        # for user in USER.find():
        #     page.send(user['id_user'], Attachment.Video(url))

        page.send("1370330196399177", Attachment.Video(url))
        page.send("1437973719614452", Attachment.Video(url))

        # luu broadcast
        new_bc = {
            'type': 'video',
            'content': url,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)
        return 'True'
    else:
        return 'False'


@app.route('/broadcast/news', methods=['POST'])
def broadcast_news():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        element = Template.GenericElement(
            title=request.form['title'],
            subtitle=request.form['subtitle'],
            image_url=request.form['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', request.form['item_url']),
                Template.ButtonPostBack('Về Home', 'home')
            ])
        # dt = request.form['timestamp']
        # # 'Jun 1 2005  1:33PM'
        # datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        # page.send(sender_id, Template.Generic(element))
        page.send("1370330196399177", Template.Generic(element))
        page.send("1437973719614452", Template.Generic(element))
        # luu broadcast
        new_bc = {
            'type': 'news',
            'content': item_url,
            'timestamp': bc['timestamp']
        }
        bc.insert_one(new_bc)
        return 'True'
    else:
        return 'False'


@app.route('/broadcast/get/<path:activation_key>', methods=['GET'])
def broadcast_get(activation_key):

    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST

    check_user_activation_key = users.find_one(
        {'user_activation_key': activation_key})

    if bool(check_user_activation_key):

        output = []
        for bc in bc.find().sort([("timestamp", -1)]):
            output.append({
                'type': bc['type'],
                'content': bc['content'],
                'timestamp': bc['timestamp']
            })
        return jsonify({'result': output})
    else:
        return 'False'


@app.route('/broadcast/get_broadcsast_by_time/<path:time>', methods=['GET'])
def get_broadcsast_by_time(time):
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    output = []
    time = datetime.strptime(time, '%Y-%m-%d %H:%M')
    a = bc.find({'timestamp': time})

    if bool(a):
        for i in a:
            output.append({
                'type': i['type'],
                'content': i['content'],
                'timestamp': i['timestamp']
            })
        return jsonify({'result': output})
    else:
        return 'False'


@app.route('/broadcast/message/save', methods=['POST'])
def broadcast_message_save():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        message = request.form['message']
        dt = request.form['timestamp']
        datetime_object = datetime.strptime(
            dt, '%Y-%m-%d %H:%M')  # 2017-11-20 16:10

        # luu broadcast
        new_bc = {
            'type': 'message',
            'content': message,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)

        return 'True'
    else:
        return 'False'


@app.route('/broadcast/message/broadcast', methods=['POST'])
def broadcast_message_broadcast():
    users = mongo.db.USER_CMS
    # check_user_activation_key = users.find_one(
    #     {'user_activation_key': request.form['user_activation_key']})
    username = users.find_one({'username': request.form['username']})
    password = users.find_one({'password': request.form['password']})
    if bool(password):
        if bool(username):
            message = request.form['message']

            # for user in USER.find():
            #     page.send(user['id_user'], message)

            page.send("1370330196399177", message)
            page.send("1437973719614452", message)

            return 'True'
        else:
            return 'False'
    else:
        return 'False'


@app.route('/broadcast/message_button/save', methods=['POST'])
def broadcast_message_button_save():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        # for user in USER.find():
        #     message = request.form['message']
        #     buttons = [
        #         Template.ButtonPostBack("Home", "home")
        #     ]
        #     page.send(user['id_user'], Template.Buttons(message, buttons))

        message = request.form['message']
        dt = request.form['timestamp']
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        buttons = [
            Templatsae.ButtonPostBack("Home", "home")
        ]
        # page.send("1370330196399177", Template.Buttons(message, buttons))
        # page.send("1437973719614452", Template.Buttons(message, buttons))
        # luu broadcast
        new_bc = {
            'type': 'message_button',
            'content': message,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)
        return 'True'
    else:
        return 'False'


@app.route('/broadcast/message_button/broadcast', methods=['POST'])
def broadcast_message_button_broadcast():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    # check_user_activation_key = users.find_one(
    #     {'user_activation_key': request.form['user_activation_key']})
    username = users.find_one({'username': request.form['username']})
    password = users.find_one({'password': request.form['password']})
    if bool(password):
        if bool(username):
            # for user in USER.find():
            #     message = request.form['message']
            #     buttons = [
            #         Template.ButtonPostBack("Home", "home")
            #     ]
            #     page.send(user['id_user'], Template.Buttons(message, buttons))

            message = request.form['message']
            dt = request.form['timestamp']
            datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
            buttons = [
                Templatsae.ButtonPostBack("Home", "home")
            ]
            page.send("1370330196399177", Template.Buttons(message, buttons))
            page.send("1437973719614452", Template.Buttons(message, buttons))
            # luu broadcast
            # new_bc = {
            #     'type': 'message_button',
            #     'content': message,
            #     'timestamp': datetime_object
            # }
            # bc.insert_one(new_bc)
            return 'True'
        else:
            return 'False'
    else:
        return 'False'


@app.route('/broadcast/image/save', methods=['POST'])
def broadcast_image_save():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        url = request.form['url']
        dt = request.form['timestamp']
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        # for user in USER.find():
        #     page.send(user['id_user'], Attachment.Image(url))

        # page.send("1370330196399177", Attachment.Image(url))
        # page.send("1437973719614452", Attachment.Image(url))
        # luu broadcast
        new_bc = {
            'type': 'image',
            'content': url,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)
        return 'True'
    else:
        return 'False'


@app.route('/broadcast/image/broadcast', methods=['POST'])
def broadcast_image_broadcast():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    # check_user_activation_key = users.find_one(
    #     {'user_activation_key': request.form['user_activation_key']})
    username = users.find_one({'username': request.form['username']})
    password = users.find_one({'password': request.form['password']})
    if bool(password):
        if bool(username):

            url = request.form['url']
            dt = request.form['timestamp']
            # 'Jun 1 2005  1:33PM'
            datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
            # for user in USER.find():
            #     page.send(user['id_user'], Attachment.Image(url))

            page.send("1370330196399177", Attachment.Image(url))
            page.send("1437973719614452", Attachment.Image(url))
            # luu broadcast
            # new_bc = {
            #     'type': 'image',
            #     'content': url,
            #     'timestamp': datetime_object
            # }
            # bc.insert_one(new_bc)
            return 'True'
        else:
            return 'False'
    else:
        return 'False'


@app.route('/broadcast/video/save', methods=['POST'])
def broadcast_video_save():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        url = request.form['url']
        dt = request.form['timestamp']
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        # for user in USER.find():
        #     page.send(user['id_user'], Attachment.Video(url))

        # page.send("1370330196399177", Attachment.Video(url))
        # page.send("1437973719614452", Attachment.Video(url))

        # luu broadcast
        new_bc = {
            'type': 'video',
            'content': url,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)
        return 'True'
    else:
        return 'False'


@app.route('/broadcast/video/broadcast', methods=['POST'])
def broadcast_video_broadcast():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    # check_user_activation_key = users.find_one(
    #     {'user_activation_key': request.form['user_activation_key']})
    username = users.find_one({'username': request.form['username']})
    password = users.find_one({'password': request.form['password']})
    if bool(password):
        if bool(username):

            url = request.form['url']
            dt = request.form['timestamp']
            # 'Jun 1 2005  1:33PM'
            datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
            # for user in USER.find():
            #     page.send(user['id_user'], Attachment.Video(url))

            page.send("1370330196399177", Attachment.Video(url))
            page.send("1437973719614452", Attachment.Video(url))

            # luu broadcast
            # new_bc = {
            #     'type': 'video',
            #     'content': url,
            #     'timestamp': datetime_object
            # }
            # bc.insert_one(new_bc)
            return 'True'
        else:
            return 'False'
    else:
        return 'False'


@app.route('/broadcast/news/save', methods=['POST'])
def broadcast_news_save():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    check_user_activation_key = users.find_one(
        {'user_activation_key': request.form['user_activation_key']})
    if bool(check_user_activation_key):
        element = Template.GenericElement(
            title=request.form['title'],
            subtitle=request.form['subtitle'],
            image_url=request.form['image_url'],
            buttons=[
                Template.ButtonWeb('Đọc tin', request.form['item_url']),
                Template.ButtonPostBack('Về Home', 'home')
            ])
        dt = request.form['timestamp']
        # # 'Jun 1 2005  1:33PM'
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
        # page.send(sender_id, Template.Generic(element))
        # page.send("1370330196399177", Template.Generic(element))
        # page.send("1437973719614452", Template.Generic(element))
        # luu broadcast
        new_bc = {
            'type': 'news',
            'content': item_url,
            'timestamp': datetime_object
        }
        bc.insert_one(new_bc)
        return 'True'
    else:
        return 'False'


@app.route('/broadcast/news/broadcast', methods=['POST'])
def broadcast_news_broadcast():
    users = mongo.db.USER_CMS
    bc = mongo.db.BROADCAST
    # check_user_activation_key = users.find_one(
    #     {'user_activation_key': request.form['user_activation_key']})
    username = users.find_one({'username': request.form['username']})
    password = users.find_one({'password': request.form['password']})
    if bool(password):
        if bool(username):
            element = Template.GenericElement(
                title=request.form['title'],
                subtitle=request.form['subtitle'],
                image_url=request.form['image_url'],
                buttons=[
                    Template.ButtonWeb('Đọc tin', request.form['item_url']),
                    Template.ButtonPostBack('Về Home', 'home')
                ])
            # dt = request.form['timestamp']
            # datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M')
            # page.send(sender_id, Template.Generic(element))
            page.send("1370330196399177", Template.Generic(element))
            page.send("1437973719614452", Template.Generic(element))
            # luu broadcast
            # new_bc = {
            #     'type': 'news',
            #     'content': item_url,
            #     'timestamp': bc['timestamp']
            # }
            # bc.insert_one(new_bc)
            return 'True'
        else:
            return 'False'
    else:
        return 'False'
