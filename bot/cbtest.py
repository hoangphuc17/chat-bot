
def cbtest_postback_handler(event):
    print('POSTBACK HANDLER CBTEST')
    sender_id = event.sender_id
    postback = event.postback_payload
    postback_list = {
        'upload_image': upload_image
    }

    if postback in postback_list:
        postback_list[postback](sender_id)


def cbtest_message_handler(event):
    print('MESSAGE HANDLER CBTEST')
    sender_id = event.sender_id
    message = event.message_text
    quickreply = event.quick_reply_payload

    if message is not None:
        message = message.lower()
    else:
        pass

    # handle_mess(sender_id, message)


def upload_image(sender_id):
    print('a')
