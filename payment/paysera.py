import base64
import hashlib
from urllib.parse import urlencode
from django.http import JsonResponse
import urllib.parse
from catalog.models import Order, Payment_system_settings
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.http import HttpResponse


# Используя документацию с https://developers.paysera.com/ru/checkout/integrations/integration-specification генерируем data и sign
def generate_data_and_sing(data):
    message = urlencode(data)
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    base64_message_replaset = base64_message.replace('/', '_')
    data = base64_message_replaset.replace('+', '-')

    pasword = '018a6e33594cb40f782e50f71cf3c87f'

    sign = hashlib.md5((data + pasword).encode())
    sign = sign.hexdigest()
    return data, sign

#Декодирование даты полученной от Пайсеры
def data_decode(data):
    data = data.replace('-', '+')
    data = data.replace('_', '/')
    data = data.encode('ascii')
    data = base64.b64decode(data)
    data = data.decode('ascii')
    # Словарь даты
    data = urllib.parse.parse_qs(data)
    return data

#Генерация подписи исходя из переданной даты и пароля из бд
def generate_sing(data):
    pasword = Payment_system_settings.objects.get(name='PaySera').secretKey
    sign = hashlib.md5((data + pasword).encode())
    sign = sign.hexdigest()
    return sign

# Проверка ответа по платежу от пайсеры
def check_paysera_payment_status(request):
    data = data_decode((request.GET['data']))
    ss1 = (request.GET['ss1'])
    ss2 = (request.GET['ss2'])
    sign = generate_sing(request.GET['data'])

    currency = data['currency'][0]
    amount = data['amount'][0]
    orderid = data['orderid'][0]
    status = data['status'][0]

    if orderid != None:
        order = get_object_or_404(Order, pk=int(orderid))
        if currency == 'EUR' and int(amount) == int((order.total*100).quantize(Decimal("1"))) and ss1 == sign and status == '1' :
            order.status = 'Paid'
            order.save()

    return HttpResponse("OK")



