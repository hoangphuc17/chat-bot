# coding: utf-8
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

from messenger_platform.messenger_api.fbmq import Page
from messenger_platform.config.config import CONFIG

ghvn = Page(CONFIG['FACEBOOK_TOKEN_GHVN'])
cdhh = Page(CONFIG['FACEBOOK_TOKEN_CDHH'])
cbtest = Page(CONFIG['FACEBOOK_TOKEN_CBTEST'])
saostar = Page(CONFIG['FACEBOOK_TOKEN_SAOSTAR'])


# @page.after_send
# def after_send(payload, response):
#     # print('AFTER_SEND : ' + payload.to_json())
#     # print('RESPONSE : ' + response.text)
#     print ('day la ham after_send: Preparation/fbpage.py')
