import time
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.forms import PayPalPaymentsForm
from django.dispatch import receiver
from catalog.custom_function import send_mesage_to_telegramm
from catalog.models import Order, Driver, Payment_system_settings, Invoice, ProjectSettings
from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from payment.UnitPay import *
from django.http import JsonResponse
import requests
import ast
import time
from decimal import Decimal
from payment.paysera import generate_data_and_sing
from django.views.decorators.clickjacking import xframe_options_sameorigin


def check_country(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    start_time = time.time()
    delay = 5
    country = ''
    while (start_time + delay) > time.time():
        try:
            url = "https://ip-geo-location.p.rapidapi.com/ip/" + ip
            querystring = {"format": "json", "filter": "country"}
            headers = {
                'x-rapidapi-key': "1228477997msh7f9935387a5b96cp1a7d1cjsn1808e5454c93",
                'x-rapidapi-host': "ip-geo-location.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            a = str(response.text)
            a = a.replace('false', 'False')
            a = a.replace('true', 'True')
            c = ast.literal_eval(a)
            country = c['country']['name']
            return country
        except:
            time.sleep(0.2)
    return country

# Обработчик платежей unitpay
def check_unitpay(request):
    # remote_address = request.META.get('REMOTE_ADDR')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip == '31.186.100.49' or ip == '178.132.203.105' or ip == '52.29.152.23' or ip == '52.19.56.234':
        # print('+++++++++++++')
        # print('То что нам пришло')
        # print(request.GET['method'])
        # print(request.GET['params[orderCurrency]'])
        # print(request.GET['params[orderSum]'])
        # print(request.GET['params[account]'])
        # print('+++++++++++')



        if request.GET['method'] == 'pay':
            order = Order.objects.get(pk=int(request.GET['params[account]']))
            # print('Информация из ордера')
            # print(str(order.invoice.amount))
            # print('+++++++++++++++++++++')
            if request.GET['params[orderCurrency]'] == 'EUR' and request.GET['params[orderSum]'] == str(order.invoice.amount):
                order.status = 'Paid'
                order.save()
                send_mesage_to_telegramm('Заказ ' + str(order.pk) + ' был успешно оплачен', '@wowspam')

        return JsonResponse({"result":{"message":"Запрос успешно обработан"}})
    else:
        return HttpResponseNotFound("You do not have permission to view this page.")


# После того как покупатель выбрал из списка предложений по заказу нужный ему,
# его прекидует на эту страницу, где он его может оплатить
# Проверка на то являейтся ли ордер который пытались открыть по ссылке ордером текущего клиента, выполнена во вьюхе
@login_required()
def pay_for_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    product = order.product
    country = check_country(request)

    if order.user_buyer == request.user:
        label1 = None
        label2 = None
        label3 = None
        label4 = None
        label5 = None
        first_label_is_private = product.first_label_is_private
        second_label_is_private = product.second_label_is_private
        third_label_is_private = product.third_label_is_private
        fourth_label_is_private = product.fourth_label_is_private
        fifth_label_is_private = product.fifth_label_is_private

        if first_label_is_private == True:
            label1 = product.first_label_name
        if second_label_is_private == True:
            label2 = product.second_label_name
        if third_label_is_private == True:
            label3 = product.third_label_name
        if fourth_label_is_private == True:
            label4 = product.fourth_label_name
        if fifth_label_is_private == True:
            label5 = product.fifth_label_name

        label1_required = order.product.first_label_required
        label2_required = order.product.second_label_required
        label3_required = order.product.third_label_required
        label4_required = order.product.fourth_label_required
        label5_required = order.product.fifth_label_required

        label1_is_private = order.product.first_label_is_private
        label2_is_private = order.product.second_label_is_private
        label3_is_private = order.product.third_label_is_private
        label4_is_private = order.product.fourth_label_is_private
        label5_is_private = order.product.fifth_label_is_private

        data_format = "%Y-%m-%d %H.%M " + str(ProjectSettings.objects.get(pk=1).time_prefix)
        schedule1 = order.schedule_value1
        schedule2 = order.schedule_value2
        schedule3 = order.schedule_value3
        schedule4 = order.schedule_value4

        try:
            driv_card = Driver.objects.get(user_driver=order.user_driver)
        except:
            driv_card = Driver()
            driv_card.user_driver = order.user_driver
            driv_card.rating = None
            driv_card.number_done_orders = 0
            driv_card.save()

        class PrePaymentForm(forms.Form):
            payment_system = []
            payment_system_q = Payment_system_settings.objects.all().filter(status=True)
            for i in payment_system_q:
                z = None
                if i.name == 'PayPal':
                    if country !='' and country != 'Russia' and country != 'Ukraine':
                        z = (i.name, i.name)
                if i.name == 'Visa and Mastercard':
                    z = (i.name, i.name)
                if i.name == 'PaySera':
                    z = (i.name, i.name)
                if z != None:
                    payment_system.append(z)
            schedule_choices = []


            if schedule1 != None:
                schedule1_list = (schedule1, str(schedule1.strftime(data_format)))
                schedule_choices.append(schedule1_list)
            if schedule2 != None:
                schedule2_list = (schedule2, str(schedule2.strftime(data_format)))
                schedule_choices.append(schedule2_list)
            if schedule3 != None:
                schedule3_list = (schedule3, str(schedule3.strftime(data_format)))
                schedule_choices.append(schedule3_list)
            if schedule4 != None:
                schedule4_list = (schedule4, str(schedule4.strftime(data_format)))
                schedule_choices.append(schedule4_list)
            payment_system = forms.ChoiceField(
                choices=payment_system,
                label=_('Select payment method:'),
                required=True
            )
            if order.product.schedule == True:
                schedule = forms.ChoiceField(
                    choices=schedule_choices,
                    label=_('Select schedule:'),
                    required=True
                )
            if label1_is_private == True:
                if label1 is not None:
                    label1_text = forms.CharField(
                        label=label1,
                        max_length=100,
                        required=label1_required
                    )
            if label2_is_private == True:
                if label2 is not None:
                    label2_text = forms.CharField(
                        label=label2,
                        max_length=100,
                        required=label2_required
                    )
            if label3_is_private == True:
                if label3 is not None:
                    label3_text = forms.CharField(
                        label=label3,
                        max_length=100,
                        required=label3_required
                    )
            if label4_is_private == True:
                if label4 is not None:
                    label4_text = forms.CharField(
                        label=label4,
                        max_length=100,
                        required=label4_required
                    )
            if label5_is_private == True:
                if label5 is not None:
                    label5_text = forms.CharField(
                        label=label5,
                        max_length=100,
                        required=label5_required
                    )
        if request.method == 'POST':
            form = PrePaymentForm(request.POST)
            if form.is_valid():
                if order.product.schedule == True:
                    print(form.cleaned_data['schedule'])
                    order.schedule_value_final = datetime.strptime(form.cleaned_data['schedule'], '%Y-%m-%d %H:%M:%S%z')
                label1_text = ''
                label2_text = ''
                label3_text = ''
                label4_text = ''
                label5_text = ''
                order.status = 'Pending'
                invoice = Invoice()
                invoice.amount = order.total
                invoice.payment_system = form.cleaned_data['payment_system']
                invoice.save()
                order.invoice = invoice
                if label1 is not None:
                    label1_text = str(label1) + ': ' + str(form.cleaned_data['label1_text']) + '<br>'
                if label2 is not None:
                    label2_text = str(label2) + ': ' + str(form.cleaned_data['label2_text']) + '<br>'
                if label3 is not None:
                    label3_text = str(label3) + ': ' + str(form.cleaned_data['label3_text']) + '<br>'
                if label4 is not None:
                    label4_text = str(label4) + ': ' + str(form.cleaned_data['label4_text']) + '<br>'
                if label5 is not None:
                    label5_text = str(label5) + ': ' + str(form.cleaned_data['label5_text']) + '<br>'
                label_sum_text = label1_text + label2_text + label3_text + label4_text + label5_text
                order.label_value_private = order.label_value_private + label_sum_text
                order.driver_name = order.user_driver.username
                order.driver_skype = Driver.objects.get(user_driver=order.user_driver).skype
                order.driver_telegram = Driver.objects.get(user_driver=order.user_driver).telegram

                order.save()
                if invoice.payment_system == 'PayPal':
                    paypal_email = Payment_system_settings.objects.get(name='PayPal').email
                    invoice.payment_system_email = paypal_email
                    invoice.save()
                    # test = invoice.order_invoice.total
                    # print(test)
                    paypal_dict = {
                        "business": str(paypal_email),
                        "amount": invoice.amount,
                        "item_name": 'Order №' + str(order.pk) + ' ' + str(order.product.name) + ' ' + str(
                            order.label_value),
                        "invoice": invoice.pk,
                        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                        "return": request.build_absolute_uri(reverse('successfully_payment')),
                        "cancel_return": request.build_absolute_uri(reverse('unsuccessful_payment')),
                        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
                        "currency_code": "EUR",
                    }
                    form = PayPalPaymentsForm(initial=paypal_dict)
                    if order.product.schedule == True:
                        schedule_final = order.schedule_value_final.strftime(data_format)
                    else:
                        schedule_final = None
                    context = {
                        'form': form,
                        'product': order.product.name,
                        'amount': invoice.amount,
                        'Driver': order.user_driver.username,
                        'Payment_method': invoice.payment_system,
                        'order': order,
                        'schedule': schedule_final
                    }
                    return render(request, "payment/payment.html", context)
                elif invoice.payment_system == 'Visa and Mastercard':
                    unitpay_progect_settings = Payment_system_settings.objects.get(name='Visa and Mastercard')
                    domain = unitpay_progect_settings.domain
                    secretKey = unitpay_progect_settings.secretKey
                    publicId = unitpay_progect_settings.publicId
                    orderCurrency = 'EUR'
                    unitpay = UnitPay(domain, secretKey)
                    orderSum = invoice.amount
                    orderId = order.pk
                    orderDesc = 'Order №' + str(order.pk) + ' ' + str(order.product.name) + ' ' + str(
                            order.label_value) + str(order.label_value_private)
                    orderDesc = orderDesc.replace('<br>', ' ')
                    redirectUrl = unitpay.form(publicId, orderSum, orderId, orderDesc, orderCurrency)
                    response = HttpResponseRedirect(redirectUrl)
                    return response
                elif invoice.payment_system == 'PaySera':
                    paysera_project_settings = Payment_system_settings.objects.get(name='PaySera')
                    paytext = (order.label_value + order.label_value_private).replace('<br>', ' ')[0:255]
                    data = {
                        'projectid': paysera_project_settings.projectId,
                        'accepturl': 'https://nstopboost.com/payment/success/',
                        'cancelurl': 'https://nstopboost.com/payment/unsuccessful/',
                        'callbackurl': 'https://nstopboost.com/payment/check_paysera/',
                        'version': '1.6',
                        'test': '0',
                        'frame': '0',
                        'payment': 'code',
                        'amount': (invoice.amount*100).quantize(Decimal("1")),
                        'currency': 'EUR',
                        'p_email': request.user.email,
                        'orderid': order.pk,
                        'buyer_consent': '0',
                        'paytext': paytext
                    }
                    data1, sign1 = generate_data_and_sing(data)

                    class PayseraPaymentForm(forms.Form):
                        data = forms.CharField(widget=forms.HiddenInput(), initial=data1)
                        sign = forms.CharField(widget=forms.HiddenInput(), initial=sign1)

                    PayseraPaymentForm = PayseraPaymentForm()

                    if order.product.schedule == True:
                        schedule_final = order.schedule_value_final.strftime(data_format)
                    else:
                        schedule_final = None
                    context = {
                        'PayseraPaymentForm': PayseraPaymentForm,
                        'product': order.product.name,
                        'amount': invoice.amount,
                        'Driver': order.user_driver.username,
                        'Payment_method': invoice.payment_system,
                        'order': order,
                        'schedule': schedule_final,
                        'data': data1,
                        'sign': sign1
                    }
                    return render(request, "payment/paysera_payment.html", context)

        form = PrePaymentForm()
        context = {
            'order': order,
            'form': form,
            "driv_card": driv_card,
            'schedule1': schedule1,
            'schedule2': schedule2,
            "schedule3": schedule3,
            "schedule4": schedule4,
        }
        return render(request, 'payment/pre_payment.html', context)
    else:
        return HttpResponseNotFound("You do not have permission to view this page.")


# Функция обработки сигнала после получения транзакции от пейпал
@receiver(valid_ipn_received)
def show_me_the_money(sender, **kwargs):
    print('Im in show_me_the_money')
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print('ST_PP_COMPLETED==True')
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        # В это место необходимо вписать все наши валидные пейпал имейлы
        if ipn_obj.receiver_email != Payment_system_settings.objects.get(name='PayPal').email:
            print('receiver_email!=' + str(Payment_system_settings.objects.get(name='PayPal').email))
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.
        # Undertake some action depending upon `ipn_obj`.

        all_invoice = Invoice.objects.all()
        invoice_id_UUIDField = all_invoice.get(pk=ipn_obj.invoice)
        if invoice_id_UUIDField != None:
            print('invoice_id_UUIDField!=None')
            print('Значения в сигнале')
            print(ipn_obj.mc_gross)
            print(ipn_obj.mc_currency)
            print('Значения с которыми мы сравниваем')
            print(invoice_id_UUIDField.amount)
            print('EUR')
            print(type(ipn_obj.mc_gross))
            # print(ipn_obj.mc_gross/course_to_usd.objects.get(currency='RUB').course_value)
            # print(type(invoice_id_UUIDField.amount))
            # print(invoice_id_UUIDField.amount)
            # Проверяем совпадает ли валюта и амаунт в заказе и в ответе пейпала
            if ipn_obj.mc_gross == invoice_id_UUIDField.amount and ipn_obj.mc_currency == 'EURO':
                print('Амаунт и тип валюты верны')
                invoice_id_UUIDField.status = 'COMPLETED'
                order = invoice_id_UUIDField.order_invoice
                order.status = 'Paid'
                invoice_id_UUIDField.save()
                order.save()
                send_mesage_to_telegramm('Заказ ' + str(order.pk) + ' был успешно оплачен', '@wowspam')
    else:
        return


# Успешная оплата
@login_required()
def success(request):
    var1 = _('Your order has been successfully paid. Please write your order id to the operator in online chat (bottom left corner). ')
    context = {'var1': var1}
    return render(request, 'payment/payment_successful_and_payment_unsuccessful.html', context)


# Не успешная оплата
@login_required()
def unsuccessful(request):
    var1 = _('Sorry, Your payment was not successful, please try again or contact our support.')
    context = {'var1': var1}
    return render(request, 'payment/payment_successful_and_payment_unsuccessful.html', context)