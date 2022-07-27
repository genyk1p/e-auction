import datetime
from decimal import Decimal

import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.urls import reverse_lazy
from .models import *
from .form import *
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from catalog.custom_function import Custom_paginator, send_mesage_to_telegramm
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


n_customer_orders_preseted = 5  # Максимальное колличество ордеров которое может разместить заказчик
chanal = "@mmo_lvl_channel"  # Каналы куда пишет бот о новом заказе #@mmo_lvl_channel, # @wowspam


# Успешная регистрация
def successful_registration(request):
    return render(request, 'registration/successful_registration.html')


# Главная форма продукта, тут можно из продукта сделать заказ
def show_product_by_category(request, category_slug, product_slug, game_slug):
    user_buyer_rank = ''
    # category = get_object_or_404(Category, slug=category_slug)
    # product1 = category.category_slug.filter(slug=product_slug)
    product = get_object_or_404(Product, slug=product_slug)

    if product.status == False:
        var1 = "This product is disabled"
        context = {'var1': var1, 'notification_class': 'notification is-info'}
        return render(request, 'catalog/standard_message.html', context)

    order = Order()
    order.product = product
    order.product_name = product.name

    first_label_is_private = product.first_label_is_private
    second_label_is_private = product.second_label_is_private
    third_label_is_private = product.third_label_is_private
    fourth_label_is_private = product.fourth_label_is_private
    fifth_label_is_private = product.fifth_label_is_private

    label1_required = order.product.first_label_required
    label2_required = order.product.second_label_required
    label3_required = order.product.third_label_required
    label4_required = order.product.fourth_label_required
    label5_required = order.product.fifth_label_required

    label1 = None
    label2 = None
    label3 = None
    label4 = None
    label5 = None
    selfplaymsg = None

    if first_label_is_private == False:
        label1 = product.first_label_name
    if second_label_is_private == False:
        label2 = product.second_label_name
    if third_label_is_private == False:
        label3 = product.third_label_name
    if fourth_label_is_private == False:
        label4 = product.fourth_label_name
    if fifth_label_is_private == False:
        label5 = product.fifth_label_name

    # Выполняет проверку создан ли инстанс модели Customer для текущего юзера баера
    if request.user.is_authenticated:
        try:
            user_buyer_from_Customer = Customer.objects.get(user_buyer=request.user)
        except:
            customer = Customer()
            customer.user_buyer = request.user
            customer.save()
        user_buyer_rank = Customer.objects.get(user_buyer=request.user).rank
        print(user_buyer_rank)
        if user_buyer_rank == 'New':
            selfplaymsg = _('This order can be done only in SelfPlay')
    else:
        selfplaymsg = _('This order can be done only in SelfPlay')

    # Выбираем данные для формирования первого селекта
    queryset_select_first = Product.objects.get(slug=product_slug).option_select_first.elements.all()
    required_select_first = Product.objects.get(slug=product_slug).required_select_first
    name_select_first = Product.objects.get(slug=product_slug).option_select_first.name

    var2 = OptionSelectFirstSummary.objects.all().filter(option_select=product.option_select_first)
    choices_option_select_first = []
    for i in var2:
        temp = (i.option_select_element.name, (i.option_select_element.name + ' +' + str(i.price) + 'EURO'))
        choices_option_select_first.append(temp)


    # Выбираем данные для формирования второго селекта
    queryset_select_second = Product.objects.get(slug=product_slug).option_select_second.elements.all()
    required_select_second = Product.objects.get(slug=product_slug).required_select_second
    name_select_second = Product.objects.get(slug=product_slug).option_select_second.name
    queryset_max_time = Product.objects.get(slug=product_slug).max_time.all()

    var2 = OptionSelectSecondSummary.objects.all().filter(option_select=product.option_select_second)
    choices_option_select_second = []
    for i in var2:
        temp = (i.option_select_element.name, (i.option_select_element.name + ' +' + str(i.price) + 'EURO'))
        choices_option_select_second.append(temp)

    # Выбираем данные для формирования 3 селекта
    queryset_select_3 = Product.objects.get(slug=product_slug).option_select_3.elements.all()
    required_select_3 = Product.objects.get(slug=product_slug).required_select_3
    name_select_3 = Product.objects.get(slug=product_slug).option_select_3.name

    var2 = OptionSelect3Summary.objects.all().filter(option_select=product.option_select_3)
    choices_option_select_3 = []
    for i in var2:
        temp = (i.option_select_element.name, (i.option_select_element.name + ' +' + str(i.price) + 'EURO'))
        choices_option_select_3.append(temp)

    # Выбираем данные для формирования процентного селекта
    queryset_select_percent = Product.objects.get(slug=product_slug).option_select_percent.elements.all()
    required_select_percent = Product.objects.get(slug=product_slug).required_select_percent
    name_select_percent = Product.objects.get(slug=product_slug).option_select_percent.name

    var2 = OptionSelectPercentSummary.objects.all().filter(option_select=product.option_select_percent)
    choices_option_select_percent = []
    for i in var2:
        if i.price >= 0:
            temp = (i.option_select_element.name, (i.option_select_element.name + ' +' + str(i.price) + '% to total price'))
        else:
            temp = (i.option_select_element.name, (i.option_select_element.name + ' ' + str(i.price) + '% from total price'))
        choices_option_select_percent.append(temp)

    # Выбираем данные для формирования первого чекбокса
    name_checkbox_first = Product.objects.get(slug=product_slug).option_check_box_first.name
    required_checkbox_first = Product.objects.get(slug=product_slug).required_check_box_first

    var2 = OptionCheckBoxFirstSummary.objects.all().filter(option_check_box=product.option_check_box_first)
    choices_option_checkbox_first = []
    for i in var2:
        temp = (i.option_check_box_element.name, (i.option_check_box_element.name + ' +' + str(i.price) + 'EURO'))
        choices_option_checkbox_first.append(temp)

    # Выбираем данные для формирования второго чекбокса
    required_checkbox_second = Product.objects.get(slug=product_slug).required_check_box_second
    name_checkbox_second = Product.objects.get(slug=product_slug).option_check_box_second.name

    var2 = OptionCheckBoxSecondSummary.objects.all().filter(option_check_box=product.option_check_box_second)
    choices_option_checkbox_second = []
    for i in var2:
        temp = (i.option_check_box_element.name, (i.option_check_box_element.name + ' +' + str(i.price) + 'EURO'))
        choices_option_checkbox_second.append(temp)

    FRACTION = [('Aliance', 'Aliance'), ('Horde', 'Horde')]

    # Создаем форму чекбоксов и селектов
    class SimpleForm(forms.Form):
        fraction = forms.ChoiceField(
            choices=FRACTION,
            required=True,
            label=_('Please select your character fraction')
        )

        if request.user.is_authenticated:
            if user_buyer_rank == 'Base':
                if name_select_first != 'None' and len(queryset_select_first) != 0:
                    select_first = forms.ChoiceField(
                        choices=choices_option_select_first,
                        required=required_select_first,
                        label=name_select_first,
                    )

        if name_select_second != 'None' and len(queryset_select_second) != 0:
            select_second = forms.ChoiceField(
                choices=choices_option_select_second,
                required=required_select_second,
                label=name_select_second,
            )
        if name_select_3 != 'None' and len(queryset_select_3) != 0:
            select_3 = forms.ChoiceField(
                choices=choices_option_select_3,
                required=required_select_3,
                label=name_select_3,
            )
        if name_select_percent != 'None' and len(queryset_select_percent) != 0:
            select_percent = forms.ChoiceField(
                choices=choices_option_select_percent,
                required=required_select_percent,
                label=name_select_percent,
            )
        max_time = forms.ModelChoiceField(
            queryset=queryset_max_time,
            required=True,
            label=_('Maximum trading time for an order (minutes)'),
        )
        if request.user.is_authenticated:
            if user_buyer_rank == 'Base':
                CHOICE_DRIVER_RANK = [('Verified', _('Verified drivers')), ('All drivers', _('All drivers'))]
                driver_rank = forms.ChoiceField(
                    choices=CHOICE_DRIVER_RANK,
                    required=True,
                    label=_('Drivers rank:'),
                )

        if name_checkbox_first != 'None':
            check_box_first = forms.MultipleChoiceField(
                required=required_checkbox_first,
                widget=forms.CheckboxSelectMultiple,
                choices=choices_option_checkbox_first,
                label=name_checkbox_first,
            )
        if name_checkbox_second != 'None':
            check_box_second = forms.MultipleChoiceField(
                required=required_checkbox_second,
                widget=forms.CheckboxSelectMultiple,
                choices=choices_option_checkbox_second,
                label=name_checkbox_second,
            )
        if label1 is not None:
            label1_text = forms.CharField(
                label=label1,
                max_length=100,
                required=label1_required
            )
        if label2 is not None:
            label2_text = forms.CharField(
                label=label2,
                max_length=100,
                required=label2_required
            )
        if label3 is not None:
            label3_text = forms.CharField(
                label=label3,
                max_length=100,
                required=label3_required
            )
        if label4 is not None:
            label4_text = forms.CharField(
                label=label4,
                max_length=100,
                required=label4_required
            )
        if label5 is not None:
            label5_text = forms.CharField(
                label=label5,
                max_length=100,
                required=label5_required
            )


    form = SimpleForm()

    if request.method == 'POST':
        if datetime.datetime.now().hour >= 1 and datetime.datetime.now().hour <= 7:
            var1 = _('Unfortunately, the order cannot be placed at the moment. Our service works from 8 am to 1 am (CEST), we will be glad to see you in the morning!')
            context = {'var1': var1, 'notification_class': 'notification is-info'}
            return render(request, 'catalog/standard_message.html', context)
        if request.user.is_authenticated == False:
            return redirect('login')
        n_customer_orders = Order.objects.all().filter(user_buyer=request.user).filter(status='New').count()
        # Тут нужно настроить сколько макимально может быть заказов со статусом New у клиента, я думаю нужно както ограничеть при релизе,
        # чтобы клиенты не могли заспамить чат в телеграмме.
        if n_customer_orders < n_customer_orders_preseted:
            form = SimpleForm(request.POST)
            if form.is_valid():
                # Присваеваем начальные значения переменным, чтобы потом не было проблемм если переменная не существует
                name_select_first = None
                select_name_second = None
                select_name_3 = None
                select_name_percent = None
                check_box_first = None
                check_box_second = None
                select_first_price = 0
                select_second_price = 0
                select_3_price = 0
                check_box_first_price = 0
                check_box_second_price = 0
                select_percent_price = 0
                check_box_first_name = ''
                check_box_second_name = ''
                var1 = ''
                label1_text = ''
                label2_text = ''
                label3_text = ''
                label4_text = ''
                label5_text = ''

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
                order.label_value = order.label_value + label_sum_text

                try:
                    name_select_first = form.cleaned_data['select_first']
                except:
                    pass
                if user_buyer_rank == 'New':
                    order.option_select_first = "SelfPlay"
                if name_select_first is not None:
                    if name_select_first == 'Piloted':
                        order.required_piloted = True
                    name_select_first = form.cleaned_data['select_first']

                    product_select1_objects = OptionSelectFirstSummary.objects.all().filter(
                        option_select=product.option_select_first)
                    for i in product_select1_objects:
                        if i.option_select_element.name == name_select_first:
                            var1 = var1 + i.option_select_element.name + "<br>"
                            select_first_price = i.price
                    order.option_select_first = name_select_first
                    order.option_select_first_price = select_first_price
                    # print(str(name_select_first) + ' ' + str(select_first_price))

                try:
                    select_name_second = form.cleaned_data['select_second']
                except:
                    pass
                if select_name_second is not None:
                    if select_name_second == 'Piloted':
                        order.required_piloted = True
                    select_name_second = form.cleaned_data['select_second']

                    product_select2_objects = OptionSelectSecondSummary.objects.all().filter(
                        option_select=product.option_select_second)
                    for i in product_select2_objects:
                        if i.option_select_element.name == select_name_second:
                            var1 = var1 + i.option_select_element.name + "<br>"
                            select_second_price = i.price

                    order.option_select_second = select_name_second
                    order.option_select_second_price = select_second_price
                    # print(str(select_name_second) + ' ' + str(select_second_price))

                try:
                    select_name_3 = form.cleaned_data['select_3']
                except:
                    pass
                if select_name_3 is not None:
                    if select_name_3 == 'Piloted':
                        order.required_piloted = True
                    select_name_3 = form.cleaned_data['select_3']

                    product_select3_objects = OptionSelect3Summary.objects.all().filter(
                        option_select=product.option_select_3)
                    for i in product_select3_objects:
                        if i.option_select_element.name == select_name_3:
                            var1 = var1 + i.option_select_element.name + "<br>"
                            select_3_price = i.price

                    order.option_select_3 = select_name_3
                    order.option_select_3_price = select_3_price
                    # print(str(select_name_second) + ' ' + str(select_second_price))

                max_time = form.cleaned_data['max_time']

                max_time_str = str(max_time)
                order.max_time = int(max_time_str)
                # print('Время поиска исполнителя =' + ' ' + str(max_time) + ' мин')

                try:
                    select_name_percent = form.cleaned_data['select_percent']
                except:
                    pass
                if select_name_percent is not None:
                    if select_name_percent == 'Piloted':
                        order.required_piloted = True
                    select_name_percent = form.cleaned_data['select_percent']

                    product_select_percent_objects = OptionSelectPercentSummary.objects.all().filter(
                        option_select=product.option_select_percent)
                    for i in product_select_percent_objects:
                        if i.option_select_element.name == select_name_percent:
                            var1 = var1 + i.option_select_element.name + "<br>"
                            select_percent_price = i.price

                    order.option_select_percent = select_name_percent
                    order.option_select_percent_price = select_percent_price
                    # print(str(select_name_second) + ' ' + str(select_second_price))

                try:
                    check_box_first = form.cleaned_data['check_box_first']
                except:
                    pass
                if check_box_first is not None:
                    if check_box_first == 'Piloted':
                        order.required_piloted = True
                    product_checkbox1_objects = OptionCheckBoxFirstSummary.objects.all().filter(
                        option_check_box=product.option_check_box_first)

                    for i in check_box_first:
                        for z in product_checkbox1_objects:
                            if z.option_check_box_element.name == i:
                                var1 = var1 + z.option_check_box_element.name + "<br>"
                                check_box_first_name = str(check_box_first_name) + ' ' + str(i) + ' ' + str(
                                    z.price) + ' EURO;'
                                check_box_first_price = check_box_first_price + z.price
                    # print(str(check_box_first_name) + ' ' + 'total price=' + str(check_box_first_price))

                    order.option_check_box_first = check_box_first_name
                    order.option_check_box_first_price = check_box_first_price

                try:
                    check_box_second = form.cleaned_data['check_box_second']
                except:
                    pass
                if check_box_second is not None:
                    if check_box_second == 'Piloted':
                        order.required_piloted = True
                    product_checkbox2_objects = OptionCheckBoxSecondSummary.objects.all().filter(
                        option_check_box=product.option_check_box_second)
                    for i in check_box_second:
                        for z in product_checkbox2_objects:
                            if z.option_check_box_element.name == i:
                                var1 = var1 + z.option_check_box_element.name + "<br>"
                                check_box_second_name = str(check_box_second_name) + ' ' + str(i) + ' ' + str(
                                    z.price) + ' EURO;'
                                check_box_second_price = check_box_second_price + z.price
                    # print(str(check_box_second_name) + ' ' + 'total price=' + str(check_box_second_price))

                    order.option_check_box_second = check_box_second_name
                    order.option_check_box_second_price = check_box_second_price
                fraction = form.cleaned_data['fraction']
                order.fraction = fraction

                if user_buyer_rank == 'Base':
                    order.driver_rank = form.cleaned_data['driver_rank']

                order_total_initial = product.price + select_first_price + select_second_price + select_3_price + \
                                      check_box_first_price + check_box_second_price
                if select_name_percent is not None:
                    if select_percent_price != 0:
                        xxx = order_total_initial + order_total_initial*select_percent_price/100
                        if xxx <= 0:
                            order.total_initial = order_total_initial
                        else:
                            order.total_initial = xxx
                    if select_percent_price == 0:
                        order.total_initial = order_total_initial
                else:
                    order.total_initial = order_total_initial
                order.total = order.total_initial
                order.user_buyer = request.user

                order.label_value = order.label_value + var1 + order.fraction + "<br>"
                print(order.label_value)

                exchange_rate = ProjectSettings.objects.last().exchange_rate
                if product.need_specific_markup_coefficient == False:
                    markup_coefficient = ProjectSettings.objects.last().markup_coefficient
                else:
                    if order.total_initial < 15.00:
                        markup_coefficient = product.markup_coefficient_before_15_eur
                    elif order.total_initial < 200.00:
                        markup_coefficient = product.markup_coefficient_before_200_eur
                    else:
                        markup_coefficient = product.markup_coefficient_after_200_eur
                order.status = 'New'
                order.markup_coefficient = markup_coefficient
                order.save()
                absolute_url = request.build_absolute_uri(reverse('requested-order', args=[order.pk]))
                mesage = str(order.product.name) + "\n"+'Фракция = ' + str(order.fraction) +"\n"+'Стартовая цена = '+str((order.total_initial*exchange_rate*markup_coefficient).quantize(Decimal("1.00")))+' RUB'+"\n"+'Время торгов по лоту = '+str(order.max_time)+' мин.' + \
                "\n" + 'Тип драйвера = ' + str(order.driver_rank) + "\n" + 'Если вы хотите выполнить данный заказ, перейдите по ссылке' +"\n"+ str(absolute_url)
                send_mesage_to_telegramm(mesage, chanal)
                # @mmo_lvl_channel
                # @wowspam
                return redirect(reverse_lazy(order_successful_add))
        else:
            return redirect(reverse_lazy(order_max_reached))

    else:
        form = SimpleForm()
    context = {'form': form, 'product': product, 'user_buyer_rank': user_buyer_rank, 'selfplaymsg': selfplaymsg}
    return render(request, 'catalog/product.html', context)


# Открывает конкретный заказ клиента
# Для заказа со статусом New и Pending здесь можно выбрать исполнителя заказа и перейти к оплате
# (редиеркт на другую страницу)
# Также здесь написание отзывов
# # Проверка на то являейтся ли ордер который пытались открыть по ссылке ордером текущего клиента, выполнена во вьюхе
@login_required()
def CustomerOrder(request, order_id):

    schedule_marker = False
    order = Order.objects.get(pk=order_id)
    product = order.product
    data_format = "%Y-%m-%d %H.%M " + str(ProjectSettings.objects.get(pk=1).time_prefix)
    if order.user_buyer == request.user:
        if order.status == 'New' or order.status == 'Pending':
            bidedorders = BidedOrder.objects.all().filter(order=order).order_by('total')
            bidedorders_list = []
            for bidedorder in bidedorders:
                bidedorder_dict = (bidedorder.__dict__)
                try:
                    driv_card = Driver.objects.get(user_driver=bidedorder.user_driver)
                except:
                    driv_card = Driver()
                    driv_card.user_driver = bidedorder.user_driver
                    driv_card.rating = None
                    driv_card.number_done_orders = 0
                    driv_card.save()
                print(bidedorder_dict)
                bidedorder_dict['price'] = bidedorder.total
                bidedorder_dict['driver_rating'] = driv_card.rating
                bidedorder_dict['driver_rank'] = driv_card.driver_rank
                bidedorder_dict['driver_number_done_orders'] = driv_card.number_done_orders
                bidedorder_dict['order_product_name'] = bidedorder.order.product.name
                bidedorder_dict['bidedorder_user_driver'] = bidedorder.user_driver.username
                if bidedorder.schedule_value1 != None: schedule_marker = True
                if bidedorder.schedule_value1 != None:
                    bidedorder_dict['schedule1'] = bidedorder.schedule_value1.strftime(data_format)
                if bidedorder.schedule_value2 != None:
                    bidedorder_dict['schedule2'] = bidedorder.schedule_value2.strftime(data_format)
                if bidedorder.schedule_value3 != None:
                    bidedorder_dict['schedule3'] = bidedorder.schedule_value3.strftime(data_format)
                if bidedorder.schedule_value4 != None:
                    bidedorder_dict['schedule4'] = bidedorder.schedule_value4.strftime(data_format)
                bidedorders_list.append(bidedorder_dict)
            # В 21 строках ниже происходит фильтрация bidedorders_list мы оставляем в нем только самые дешовые предложения от драйверов.
            bidedorders_list_id = []
            bidedorders_list_uniq = []
            for i in bidedorders_list:
                drver = i['bidedorder_user_driver']
                price = None
                id_id = 0
                for x in bidedorders_list:
                    if x['bidedorder_user_driver'] == drver:
                        if price == None:
                            id_id = x['id']
                            price = x['price']
                        if price > x['price']:
                            id_id = x['id']
                bidedorders_list_id.append(id_id)
            output = []
            for x in bidedorders_list_id:
                if x not in output:
                    output.append(x)
            for x in output:
                for y in bidedorders_list:
                    if x == y['id']:
                        bidedorders_list_uniq.append(y)
            bidedorders_list = bidedorders_list_uniq

            if request.method == 'POST':
                answer = None
                try:
                    answer = request.POST['answer']
                except:
                    answer = None
                if answer == None:
                    context = {'bidedorders': bidedorders_list, 'var1': 'Please select order driver'}
                    return render(request, 'catalog/customer_order.html', context)
                elif answer == 'Cancel order':
                    order.status = 'Denied'
                    order.save()
                    var1 = _('You have successfully canceled your order.')
                    context = {'var1': var1, 'notification_class': 'notification is-info'}
                    return render(request, 'catalog/standard_message.html', context)
                else:
                    bidedorder_id = answer
                    try:
                        bidedorder = BidedOrder.objects.get(pk=bidedorder_id)
                    except:
                        return redirect(reverse_lazy(deleted_bid_message))

                        # var1 = _('Sorry, the driver canceled the current offer, please try another offer')
                        # context = {'var1': var1,
                        #            'notification_class': "notification is-info"
                        #            }
                        # return render(request, 'information/standard_message.html', context)
                    order.user_driver = bidedorder.user_driver
                    order.total = bidedorder.total
                    order.total_rub = bidedorder.total_rub
                    order.schedule_value1 = bidedorder.schedule_value1
                    order.schedule_value2 = bidedorder.schedule_value2
                    order.schedule_value3 = bidedorder.schedule_value3
                    order.schedule_value4 = bidedorder.schedule_value4
                    order.status = 'Pending'
                    order.save()
                    return redirect(reverse('payment', args=[order.id]))
            if len(bidedorders) == 0:
                var1 = _('Unfortunately, there are no active offers from the drivers for this order yet.')
                context = {'var1': var1, 'notification_class': "notification is-info"}
                return render(request, 'catalog/standard_message.html', context)
            if order.status == 'Pending':
                pending_notification = _("Please note that the bidding for this order has ended and drivers will no longer be able to add their vacancy to this order. If you are not satisfied with the trading results, you can create a new order.")
            else:
                pending_notification = None
            context = {
                'bidedorders': bidedorders_list,
                'var1': None,
                'schedule_marker': schedule_marker,
                'pending_notification': pending_notification,
                'notification_class': 'notification is-info',
            }
            return render(request, 'catalog/customer_order.html', context)

        # Если клиент в своем личном кабинете откроет товар со статусом  Complete, то он сможет написать отзыв к этому
        # заказу
        elif order.status == 'Complete':
            form = ReviewForm()
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    # form.save()
                    last_review = Review()
                    last_review.review_text = form.cleaned_data['review_text']
                    last_review.rating = form.cleaned_data['rating']
                    last_review.user_buyer = order.user_buyer
                    last_review.user_driver = order.user_driver
                    last_review.save()
                    order.review = last_review
                    order.save()

            if order.review is None:
                context_review = _('No reviews available')
                context_rating = _('No rating')
            else:
                context_review = str(order.review.review_text)
                context_rating = str(order.review.rating)
            context = {'order': order, 'form': form, 'review': context_review, 'rating': context_rating}
            return render(request, 'catalog/customer_complited_order.html', context)
        else:
            context = {'order': order}
            return render(request, 'catalog/customer_order_done.html', context)
    else:
        return HttpResponseNotFound("You do not have permission to view this page.")


# Заказ успешно добавлен
@login_required()
def order_successful_add(request):
    return render(request, 'catalog/order_successful_add.html')


# У клиента превышено максимально возможное количество заказов со статусом new
@login_required()
def order_max_reached(request):
    return render(request, 'catalog/maximum_new_order_reached.html')


# Отображает все ордеры клиента
@login_required()
def CustomerOrders(request):
    orders = Order.objects.all().filter(user_buyer=request.user)
    page = Custom_paginator(request, orders)
    context = {'orders': page.object_list, 'page': page}
    return render(request, 'catalog/customer_orders.html', context)


# Отображает ордеры клиента с возможностью фильтрации
@login_required()
def CustomerOrdersFilter(request):
    # Пытаемся из бд получить с каким статусом заказы нам нужно отображать, так как значения в бд может не
    # существовать, используется конструкция трай экспет, которая в случае если не удалось извлечь значение делает
    # новую дефолтную запись.
    try:
        user_order_status = UserSettings.objects.get(user=request.user).current_order_filter
    except:
        user_settings = UserSettings()
        user_settings.current_order_filter = 'New'
        user_settings.user = request.user
        user_settings.save()
        user_order_status = UserSettings.objects.get(user=request.user).current_order_filter

    STATUS = [('Processing', 'Processing'), ('Pending', 'Pending'), ('Complete', 'Complete'),
              ('Denied', 'Denied'), ('New', 'New'), ('Expired', 'Expired'), ('Paid', 'Paid')]

    class StatusForm(forms.Form):
        select_order_status = forms.ChoiceField(
            choices=STATUS,
            label='Select status',
        )

    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            order_status = form.cleaned_data['select_order_status']
            user_settings = UserSettings.objects.get(user=request.user)
            user_settings.current_order_filter = order_status
            user_settings.save()

    orders = Order.objects.all().filter(user_buyer=request.user)

    orders = orders.filter(status=UserSettings.objects.get(user=request.user).current_order_filter)
    form = StatusForm()
    page = Custom_paginator(request, orders=orders)
    user_order_status = UserSettings.objects.get(user=request.user).current_order_filter

    context = {'orders': page.object_list, 'form': form, 'page': page, 'user_order_status': user_order_status}

    return render(request, 'catalog/customer_orders_filter.html', context)


# Функция отрисовывает один выбранный ордер для драйвера если он по нему кликнул
# Проверка на то может ли драйвер смотреть текущий заказ выполнена, если статус новый, то ордер смотреть можно,
# все остальные статусы можно смотреть только если драйвер закреплен как драйвер за этим ордером
@login_required()
def requested_order_for_drivers(request, order_id):
    if not request.user.groups.filter(name='Driver').count():
        var1 = _("Unfortunately, you don't have authorization to see this page. This page is for drivers only. If you want to become a driver please contact the platform's administration.")
        context = {'var1': var1, 'notification_class': 'notification is-warning'}
        return render(request, 'catalog/standard_message.html', context)
    minimal_order_price = 9  #Миниамльная цена заказа.
    current_order = Order.objects.get(pk=order_id)
    product = current_order.product

    # Проверяем может ли драйвер делать заказы в режиме пилотед
    if current_order.required_piloted == True:
        try:
            driver_rank = Driver.objects.get(user_driver=request.user).can_do_piloted
        except:
            driver_card = Driver()
            driver_card.number_done_orders = 0
            driver_card.user_driver = request.user
            driver_card.save()
        driver_rank = Driver.objects.get(user_driver=request.user).can_do_piloted
        if driver_rank == False:
            var1 = _('Unfortunately, you cannot make orders in Piloted mode yet.')
            context = {'var1': var1, 'notification_class': 'notification is-warning'}
            return render(request, 'catalog/standard_message.html', context)

    # Проверяем может ли дравер делать ставки по текущему ордеру.
    print(current_order.driver_rank)
    if current_order.driver_rank == 'Verified':
        if Driver.objects.get(user_driver=request.user).driver_rank == 'New':
            var1 = _("Unfortunately, you cannot place a bid on this order, because the customer selected only 'Verified driver' option, and you status is 'New'.")
            context = {'var1': var1, 'notification_class': 'notification is-warning'}
            return render(request, 'catalog/standard_message.html', context)


    exchange_rate = ProjectSettings.objects.last().exchange_rate
    markup_coefficient = current_order.markup_coefficient
    old_order_total = current_order.total

    # Проверяем есть ли у продукта расписание или нет, и в зависимости от этоо рисуем разные формы
    if current_order.status == 'New':
        if current_order.product.schedule == False:
            form = BidOrderForm()
        else:
            form = BidOrderFormS()

        if request.method == 'POST':
            if current_order.product.schedule == False:
                form = BidOrderForm(request.POST)
            else:
                form = BidOrderFormS(request.POST)
            if form.is_valid():
                newBO = BidedOrder()
                newBO.user_driver = request.user
                newBO.total_rub = form.cleaned_data['total_rub']
                newBO.total = (newBO.total_rub / exchange_rate) / markup_coefficient

                #Проверяем не стал ли заказ меньше минимального и если тсал то устанавливаем нашу ставку из расчета мин заказа
                if newBO.total < minimal_order_price:
                    newBO.total = minimal_order_price
                    newBO.total_rub = minimal_order_price*exchange_rate*markup_coefficient

                # Если у продкта есть расписание, то нужно забрать его из формы
                if current_order.product.schedule == True:
                    data1 = form.cleaned_data['schedule_value1_date']
                    time1 = form.cleaned_data['schedule_value1_time']
                    newBO.schedule_value1 = data1 + timedelta(minutes=time1.minute, hours=time1.hour)
                    # Не обязательные поля расписания могут быть пустыми и привести к ошибке, поэтому
                    # проверяем не пустые ли они прежде чем с ними работать
                    if (form.cleaned_data['schedule_value2_time']) != None:
                        data2 = form.cleaned_data['schedule_value2_date']
                        time2 = form.cleaned_data['schedule_value2_time']
                        newBO.schedule_value2 = data2 + timedelta(minutes=time2.minute, hours=time2.hour)
                    if (form.cleaned_data['schedule_value3_time']) != None:
                        data3 = form.cleaned_data['schedule_value3_date']
                        time3 = form.cleaned_data['schedule_value3_time']
                        newBO.schedule_value3 = data3 + timedelta(minutes=time3.minute, hours=time3.hour)
                    if (form.cleaned_data['schedule_value4_time']) != None:
                        data4 = form.cleaned_data['schedule_value4_date']
                        time4 = form.cleaned_data['schedule_value4_time']
                        newBO.schedule_value4 = data4 + timedelta(minutes=time4.minute, hours=time4.hour)

                newBO.order = current_order
                newBO.save()
                # Если в никто другой паралельно не бидал по продукту, то бид обработанный в текущей функции будет
                # самым низким и его значение будет установленно в модели заказа, также будет заменен драйвер
                if current_order.total > newBO.total:
                    current_order.total = newBO.total
                    current_order.total_rub = newBO.total_rub
                    current_order.user_driver = request.user
                    current_order.save()
                current_order = Order.objects.get(pk=order_id)
                var1 = _('You have successfully added your vacancy to the list of the potential drivers for this order.')
                total_rub = (current_order.total * exchange_rate * markup_coefficient).quantize(Decimal("1.00"))
                minimal_order_price_rub = (minimal_order_price * exchange_rate * markup_coefficient).quantize(Decimal("1.00"))
                context = {
                    'order': current_order,
                    'total_rub': total_rub,
                    'form': form,
                    'var1': var1,
                    'minimal_order_price_rub': minimal_order_price_rub
                }
                return render(request, 'catalog/requested_order_for_drivers.html', context)
        var1 = None

        total_rub = (current_order.total * exchange_rate * markup_coefficient).quantize(Decimal("1.00"))
        context = {'order': current_order, 'total_rub': total_rub, 'form': form, 'var1': var1}
        return render(request, 'catalog/requested_order_for_drivers.html', context)
    elif current_order.status == 'Processing' or current_order.status == 'Complete' \
            or current_order.status == 'Paid':
        if current_order.user_driver == request.user:
            context1 = {'order': current_order}
            return render(request, 'catalog/requested_order_for_drivers_extended.html', context1)
        else:
            return HttpResponseNotFound("You do not have permission to view this page.")
    elif current_order.status == 'Pending':
        var1 = _('This order is waiting for payment, You can see the information after the payment would be done.')
        context = {'var1': var1, 'notification_class': 'notification is-warning'}
        return render(request, 'catalog/standard_message.html', context)

    return HttpResponseNotFound("No template available for order with status" + str(current_order.status))


# Функция которая включается после того как дривер в папке Requested orders нажал по кнопке бид, она забирает 2
# url параметра ордер id и цена товара которая была отрисованна на странице. Цену товара мы берем со страницы
# потому что за время пока наша страница была не обновленна, другие юзеры могли уже побидать продукт, и если бы
# мы взяли цену из модели продукта то она бы была меньше той что на странице, и драйвер не хотя того мог бы
# согласить ся делать продукт по ценее более низкой чем он хотел бы.
@login_required()
@permission_required('catalog.change_order', raise_exception=True)
def bid_order(request, order_id, order_total):
    minimal_order_price = 9  # Миниамльная цена заказа.
    old_order_total = (Decimal(order_total))
    order = Order.objects.get(pk=order_id)
    product = order.product
    # Проверяем может ли драйвер делать заказы в режиме пилотед
    if order.required_piloted == True:
        try:
            driver_rank = Driver.objects.get(user_driver=request.user).can_do_piloted
        except:
            driver_card = Driver()
            driver_card.number_done_orders = 0
            driver_card.user_driver = request.user
            driver_card.save()
        driver_rank = Driver.objects.get(user_driver=request.user).can_do_piloted
        if driver_rank == False:
            var1 = 'Unfortunately, you cannot make orders in Piloted mode yet.'
            context = {'var1': var1, 'notification_class': 'notification is-warning'}
            return render(request, 'catalog/standard_message.html', context)

    # Проверяем может ли дравер делать ставки по текущему ордеру.
    if order.driver_rank == 'Verified':
        if Driver.objects.get(user_driver=request.user).driver_rank == 'New':
            var1 = _(
                "Unfortunately you cannot make bid by this order because customer selected only 'Verified driver' option, and you status is 'New'.")
            context = {'var1': var1, 'notification_class': 'notification is-warning'}
            return render(request, 'catalog/standard_message.html', context)


    exchange_rate = ProjectSettings.objects.last().exchange_rate
    markup_coefficient = order.markup_coefficient
    bided_order = BidedOrder.objects.all().filter(order=order).filter(user_driver=request.user)
    if old_order_total > order.total_initial:
        # Из отображения хтмл было передано значение большее чем начальное значение, а такое может быть только при
        # подделки запроса
        pass
    else:
        if order.status == "New":
            if order.product.schedule == True and len(bided_order) == 0:
                return redirect(reverse('requested-order', args=[order.id]))
            else:
                newBO = BidedOrder()
                newBO.user_driver = request.user
                new_total = old_order_total * Decimal(0.95)
                newBO.total = old_order_total * Decimal(0.95)
                newBO.total_rub = newBO.total * exchange_rate * markup_coefficient
                #Проверка на минимальную цену ордера
                if newBO.total < minimal_order_price:
                    newBO.total = minimal_order_price
                    newBO.total_rub = newBO.total * exchange_rate * markup_coefficient
                    new_total = minimal_order_price
                newBO.order = order
                # Если юзер уже указал расписание для ордера, то ему дасть сразу сделать бид по ордеру,
                # и чтобы  в новый инстанс BidedOrder перенеслось расписание мы его пересохраняеем ниже
                if order.product.schedule == True:
                    for i in bided_order:
                        newBO.schedule_value1 = i.schedule_value1
                        newBO.schedule_value2 = i.schedule_value2
                        newBO.schedule_value3 = i.schedule_value3
                        newBO.schedule_value4 = i.schedule_value4
                newBO.save()
                # Если в никто другой паралельно не бидал по продукту, то бит обработанный в текущей функции будет
                # самым низким и его значение будет установленно в модели заказа, также будет заменен драйвер
                if order.total > new_total:
                    order.total = new_total
                    order.total_rub = newBO.total_rub
                    order.user_driver = request.user
                    order.save()

    # возвращаемся на урл папки Requested order
    return redirect(reverse_lazy(requested_orders_for_drivers))


# В обзоре ордеров драйвера отрисовываем ордеры с определенным статусом указанном в названии функции
@login_required()
@permission_required('catalog.change_order', raise_exception=True)
def requested_order_status_pending(request):
    orders = Order.objects.all().filter(status='Pending').filter(user_driver=request.user)
    page = Custom_paginator(request, orders)
    context = {'orders': page.object_list, 'page': page}
    return render(request, 'catalog/requested_order_for_drivers_by_status.html', context)


# В обзоре ордеров драйвера отрисовываем ордеры с определенным статусом указанном в названии функции
@login_required()
@permission_required('catalog.change_order', raise_exception=True)
def requested_order_status_paid(request):
    orders = Order.objects.all().filter(status='Paid').filter(user_driver=request.user)
    page = Custom_paginator(request, orders)
    context = {'orders': page.object_list, 'page': page}
    return render(request, 'catalog/requested_order_for_drivers_by_status.html', context)


# В обзоре ордеров драйвера отрисовываем ордеры с определенным статусом указанном в названии функции
@login_required()
@permission_required('catalog.change_order', raise_exception=True)
def requested_order_status_processing(request):
    orders = Order.objects.all().filter(status='Processing').filter(user_driver=request.user)
    page = Custom_paginator(request, orders)
    context = {'orders': page.object_list, 'page': page}
    return render(request, 'catalog/requested_order_for_drivers_by_status.html', context)


# В обзоре ордеров драйвера отрисовываем ордеры с определенным статусом указанном в названии функции
@login_required()
@permission_required('catalog.change_order', raise_exception=True)
def requested_order_status_complete(request):
    orders = Order.objects.all().filter(status='Complete').filter(user_driver=request.user)
    page = Custom_paginator(request, orders)
    context = {'orders': page.object_list, 'page': page}
    return render(request, 'catalog/requested_order_for_drivers_by_status.html', context)


# Отображает список ордеров по которомы можно делать ставки для дриверов
@login_required()
# @permission_required('catalog.change_order', raise_exception=True)
def requested_orders_for_drivers(request):
    minimal_order_price = 9  # Миниамльная цена заказа.
    orders1 = Order.objects.filter(status='New')
    # Загружаем из бд  коэфициент моржи и текущий курс. Из бд выгружается последняя сущьность.
    exchange_rate = ProjectSettings.objects.last().exchange_rate

    orders = []
    for order in orders1:
        if order.user_driver is None:
            driver = None
        else:
            driver = order.user_driver.username
        order = {'pk': order.pk,
                 'name': order.product.name,
                 'total_rub': (order.total * exchange_rate * order.markup_coefficient).quantize(Decimal("1.00")),
                 'driver': driver,
                 'total': order.total,
                 'label_value': order.label_value,
                 'fraction': order.fraction,
                 'required_piloted': order.required_piloted,
                 'driver_rank': order.driver_rank,
                 'minimal_order_price': (minimal_order_price * exchange_rate * order.markup_coefficient).quantize(Decimal("1.00"))
                 }
        orders.append(order)

    page = Custom_paginator(request, orders=orders)
    context = {'orders': page.object_list, 'page': page}
    return render(request, 'catalog/requested_orders_for_drivers.html', context)


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/index.html', context)

# показывает продукты согласно категории
def show_all_products_category(request, category_slug):
    print(category_slug)
    category = Category.objects.get(slug=category_slug)
    products = Product.objects.all().filter(category=category).filter(status=True)
    context = {'products': products}
    return render(request, 'catalog/show_all_products.html', context)


@login_required()
def account_settings(request):
    template = loader.get_template('catalog/account_settings.html')
    var1 = 'Account settings'
    if request.user.groups.filter(name='Driver').count():
        var2 = 1
        driver = Driver.objects.get(user_driver=request.user)
    else:
        var2 = 0
        driver = None
    context = {'var1': var1, 'var2': var2, 'driver': driver}
    return HttpResponse(template.render(context, request))


def category_dungeon(request):
    category = get_object_or_404(Category, slug='dungeon')
    products = category.category_slug.all()
    context = {'products': products}
    return render(request, 'catalog/category.html', context)

# Функция отмены одной из ставок для драйвера
@login_required()
@permission_required('catalog.change_order', raise_exception=True)
def DeletBidedOrder(request, order_id):
    bided_orders = BidedOrder.objects.all().filter(user_driver=request.user).filter(order=order_id)
    if request.method == 'POST':
        try:
            a = request.POST['answer']
        except:
            a = None
        if a != None:
            order = Order.objects.get(pk=order_id)
            try:
                bided_order = BidedOrder.objects.get(pk=a)
            except:
                bided_order = None
            if bided_order!=None:
                all_bided_orders = BidedOrder.objects.all().filter(order=order_id)
                if order.status == 'New':
                    bided_order.delete()
                    if len(all_bided_orders) != 0:
                        for i in all_bided_orders.order_by('-total'):
                            new_bided_order = i
                            break
                        order.total = new_bided_order.total
                        order.total_rub = new_bided_order.total_rub
                        order.user_driver = new_bided_order.user_driver
                        order.save()
                    else:
                        order.total = order.total_initial
                        order.total_rub = 0
                        order.user_driver = None
                        order.save()
                    var1 = _('You have successfully deleted your bid')
                    context = {'var1': var1, 'bided_order': bided_orders}
                    return render(request, 'catalog/delet-bided-order.html', context)
                else:
                    var1 = _('Unfortunately, it is no longer possible to cancel the bid, because the buyer went to the ordering procedure or canceled the order.')
                    context = {'var1': var1, 'bided_order': bided_orders}
                    return render(request, 'catalog/delet-bided-order.html', context)
    var1 = None
    context = {'var1': var1, 'bided_order': bided_orders}
    return render(request, 'catalog/delet-bided-order.html', context)

# Если покуатель решит купить ставку которую уже отменили ем выпадет сообщение об ошибке.
def deleted_bid_message(request):
    notification_class = "notification is-info"
    var1 = _("Sorry, the driver canceled the current offer, please try another offer from the list.")
    context = {'var1': var1, 'notification_class': notification_class}
    return render(request, 'catalog/standard_message.html', context)
