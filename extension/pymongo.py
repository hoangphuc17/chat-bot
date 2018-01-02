# cau lenh update
CUSTOMER.update_one(
        {'id_user': sender_id},
        {'$set': {'SCRIPT': {'id_user': sender_id, 'subscribe': 'no', 'vote': ''}}}
    )