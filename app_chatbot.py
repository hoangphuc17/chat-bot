# -*- coding: utf-8 -*-
import os
import sys
import json
import requests

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

from flask import Flask, request, send_from_directory, render_template

from messenger_platform.messenger_api import Attachment, Template
# from messenger_platform.messenger_api import QuickReply
# from messenger_platform.messenger_api import Page

from messenger_platform.config.config import CONFIG

from messenger_platform.config.fbpage import cbtest, ghvn, cdhh, ttb, saostar, svtv

from bot.cbtest import *  # demo chatbot saostar

from bot.ghvn import *
from bot.cdhh import *
from bot.ttb import *
from bot.saostar import *
from bot.svtv import *

app = Flask(__name__)

id_page_cbtest = '1987057708238038'

id_page_ghvn = '344510328981706'
id_page_cdhh = '693691134038165'
id_page_ttb = '932322753471323'
id_page_saostar = '1281407545241725'
id_page_svtv = '1654988921425352'


# Verify
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == CONFIG['VERIFY_TOKEN']:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    else:
        return "trouble in hub.mode or hub.challenge", 200

    return "verify successfully", 200


# Webhook
@app.route('/', methods=['POST'])
def webhook():
    payload = request.get_data(as_text=True)
    payload_dict = json.loads(payload)

    # XU LY WEBHOOK CHATBOT GHVN
    # if payload_dict['entry'][0]['id'] == id_page_ghvn:
    #     print('GIONG HAT VIET NHI')
    #     ghvn.handle_webhook(payload, message=ghvn_message_handler,
    #                         postback=ghvn_postback_handler)
    #     return 'ok', 200

    # # XU LY WEBHOOK CHATBOT CDHH
    # elif payload_dict['entry'][0]['id'] == id_page_cdhh:
    #     print('CAP DOI HOAN HAO')
    #     cdhh.handle_webhook(payload, message=cdhh_message_handler,
    #                         postback=cdhh_postback_handler)
    #     return "ok", 200

    # # XU LY WEBHOOK CHATBOT CBTEST
    # elif payload_dict['entry'][0]['id'] == id_page_cbtest:
    #     print('CBTEST')
    #     cbtest.handle_webhook(
    #         payload, message=cbtest_message_handler, postback=cbtest_postback_handler)
    #     return "cbtest ok", 200

    # # XU LY WEBHOOK CHATBOT TTB
    # elif payload_dict['entry'][0]['id'] == id_page_ttb:
    #     print('THAN TUONG BOLERO')
    #     cbtest.handle_webhook(
    #         payload, message=ttb_message_handler, postback=ttb_postback_handler)
    #     return "ok", 200

    # # XU LY WEBHOOK CHATBOT SAOSTAR
    # elif payload_dict['entry'][0]['id'] == id_page_saostar:
    #     print('SAOSTAR')
    #     cbtest.handle_webhook(
    #         payload, message=saostar_message_handler, postback=saostar_postback_handler)
    #     return "saostar ok", 200

    # XU LY WEBHOOK CHATBOT SVTV
    if payload_dict['entry'][0]['id'] == id_page_svtv:
        print('SINH VIEN TV')
        cbtest.handle_webhook(
            payload, message=svtv_message_handler, postback=svtv_postback_handler)
        return "svtv ok", 200

    else:
        return 'no app correspondent'


if __name__ == '__main__':
    app.run(host='210.211.109.211', port=5000, debug=True, threaded=True)
