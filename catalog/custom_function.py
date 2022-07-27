from django.core.paginator import Paginator
import requests

# Пагинатор
def Custom_paginator(request, orders, order_in_page=20):
    paginator = Paginator(orders, order_in_page)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return page

# Отправляет сообщение в телеграмм
def send_mesage_to_telegramm(text: str, channel_id='@mmo_lvl_channel'):
    token = "843984589:AAFXGdrstr8h_S52aNdbXIqTtoYzr7IKQwA"
    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")