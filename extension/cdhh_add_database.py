# -*- coding: utf-8 -*-
import os
import sys
from ApiMessenger import Attachment, Template
from ApiMessenger.payload import QuickReply
from ApiMessenger.fbmq import Page

import CoreChatbot.Preparation.messenger
from CoreChatbot.Preparation.config import CONFIG

from CoreChatbot.Preparation.fbpage import cdhh
from CoreChatbot.CapDoiHoanHao.cdhh_database import *


def insert_new_news():
    insert_news('Cố vấn Cẩm Ly tim đập ‘loạn xạ’ trước cách hát Bolero mới mẻ của Erik ', ' Việc Erik giữ chất riêng của mình khi hát Bolero khiến cố vấn Cẩm Ly và Ngọc Sơn hoàn toàn bất ngờ. ',
                'https://img.saostar.vn/265x149/2017/10/26/1713015/ava.jpg', 'https://saostar.vn/tv-show/co-van-cam-ly-tim-dap-loan-xa-truoc-cach-hat-bolero-moi-cua-erik-1713015.html')
    insert_news('Cao Công Nghĩa tiết lộ lý do từ chối Tiêu Châu Như Quỳnh, Erik để chọn Đức Phúc ', ' Cao Công Nghĩa đã khiến hai cố vấn và dàn thí sinh Cặp đôi hoàn hảo 2017 ngỡ ngàng khi chọn song ca cùng Đức Phúc. Hãy cùng tìm hiểu lý do vì sao giải Vàng Thần tượng Bolero lại có quyết định bất ngờ và khá mạo hiểm này. ',
                'https://img.saostar.vn/265x149/2017/10/19/1690021/ccn.jpg', 'https://saostar.vn/tv-show/cao-cong-nghia-tiet-lo-ly-tu-choi-tieu-chau-nhu-quynh-erik-de-chon-duc-phuc-1690021.html')
    insert_news('Tiêu Châu Như Quỳnh: ‘Thánh nhọ Bolero’ hay phải chờ gặp Triều Quân như ‘định mệnh’? ', ' Sau nhiều phen "lận đận" bị khách mời từ chối thì Tiêu Châu Như Quỳnh đã có kết cục "viên mãn" khi bắt cặp thành công cùng Triều Quân tại tập 2 Cặp đôi Hoàn hảo - Trữ tình & Bolero vừa qua. ',
                'https://img.saostar.vn/530x298/2017/10/19/1690065/tcnq.jpg', 'https://saostar.vn/tv-show/tieu-chau-nhu-quynh-thanh-nho-bolero-hay-phai-cho-gap-trieu-quan-nhu-dinh-menh-1690065.html')
    insert_news('Chưa kịp ‘kết đôi’ cùng trai đẹp, Hoà Minzy đã đòi ‘về một nhà’ với Mai Tiến Dũng sau hậu trường ', ' Dù chỉ là những khoảnh khắc vui đùa trong hậu trường. Song, đây chính là những giờ phút thoải mái nhất của cả hai trước áp lực của cuộc thi đang cận kề. ',
                'https://img.saostar.vn/530x298/2017/10/19/1689973/a-nh-chu-p-ma-n-hi-nh-2017-10-20-lu-c-00-12-43.png', 'https://saostar.vn/tv-show/chua-kip-ket-doi-cung-trai-dep-hoa-minzy-da-doi-ve-mot-nha-voi-mai-tien-dung-sau-hau-truong-1689973.html')
    # insert_news('', '', '', '')


insert_new_news()
