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

from messenger_platform.config.fbpage import ghvn, cdhh, cbtest, saostar

from bot.ghvn import *
from bot.cdhh import *
from bot.cbtest import *

app = Flask(__name__)


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
    if payload_dict['entry'][0]['id'] == "344510328981706":
        print('GIONG HAT VIET NHI')
        ghvn.handle_webhook(payload, message=ghvn_message_handler,
                            postback=ghvn_postback_handler, attachments_message=ghvn_attachments_message_handler)
        return 'ok', 200

    # XU LY WEBHOOK CHATBOT CDHH
    elif payload_dict['entry'][0]['id'] == "693691134038165":
        print('CAP DOI HOAN HAO')
        cdhh.handle_webhook(payload, message=cdhh_message_handler,
                            postback=cdhh_postback_handler)
        return "ok", 200

    # XU LY WEBHOOK CHATBOT CBTEST
    elif payload_dict['entry'][0]['id'] == "1987057708238038":
        print('CBTEST')
        cbtest.handle_webhook(
            payload, message=cbtest_message_handler, postback=cbtest_postback_handler)
        return "cbtest ok", 200

    else:
        return 'no app correspondent'


if __name__ == '__main__':
    app.run(host='210.211.109.211', port=5000, debug=True, threaded=True)
