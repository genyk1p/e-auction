from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from tinymce.models import HTMLField


# Карточка драйвера
# Важно группа дриверов в админке должна называться Driver с большой буквы
class Driver(models.Model):
    CHOICE = [('New', 'New'), ('Verified', 'Verified')]
    user_driver = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='Driver', default=None)
    number_done_orders = models.SmallIntegerField(default=0, verbose_name='Итого заказов выполненое Драйвером')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, verbose_name='Рейтинг драйвера',
                                 null=True, blank=True)
    can_do_piloted = models.BooleanField(verbose_name='Может ли драйвер делать заказы в режиме Piloted',
                                         default=False)
    skype = models.CharField(max_length=40, default='', null=True, blank=True)
    telegram = models.CharField(max_length=40, default='', null=True, blank=True)
    driver_rank = models.CharField(max_length=40, default='New', choices=CHOICE)

    # def __str__(self):
    #     return str(self.user_driver.username)

class Customer(models.Model):
    CHOICE = [('New', 'New'), ('Base', 'Base')]
    user_buyer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='buyer', default=None)
    rank = models.CharField(max_length=40, default='New', choices=CHOICE)


# Настройки платежных систем
class Payment_system_settings(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название платежной системы')
    email = models.EmailField(verbose_name='Емейл в платежной системе, для пейпала это логин в пейпал акаунте',
                              null=True, blank=True)
    domain = models.CharField(max_length=30, help_text='Your current domain: unitpay.money or unitpay.ru', null=True,
                              blank=True)
    projectId = models.IntegerField(null=True, blank=True)
    secretKey = models.CharField(max_length=100, null=True, blank=True)
    publicId = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(verbose_name='On/Off', default=True)

    def __str__(self):
        return str(self.name)


# Предполагается хранить тут всякие настройки связанные с пользователем, причем не обязательные для его редактирования.
class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    # current_order_filter - Это текущее значение фильтрации по которому фильтруются заказы клиента в папке My orders
    current_order_filter = models.CharField(max_length=20, default='New')


# Предполагается хранить тут всякие настройки связанные с проектом, доступные для редактирования в админке
class ProjectSettings(models.Model):
    exchange_rate = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Расчетный курс из пейпала')
    markup_coefficient = models.DecimalField(max_digits=8, decimal_places=2,
                                             verbose_name='Коэффициент наценки платформы')
    time_prefix = models.CharField(max_length=10, blank=True, default='CET',
                                   verbose_name='Какой префикс использовать CET/CEST')

    def __str__(self):
        return 'Настройки проекта, можно изменить их значения, но нельзя удалять и делать новый объект'


# Время торгов по заказу
class MaxTime(models.Model):
    max_time = models.SmallIntegerField(default=0, verbose_name='Максимальное время торгов по заказу')

    class Meta:
        ordering = ['max_time']

    def __str__(self):
        return str(self.max_time)


# Элементы виджита селект
class OptionSelectElement(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Виджет селект
class OptionSelectFirst(models.Model):
    name = models.CharField(max_length=50)
    admin_name = models.CharField(max_length=50, default='',
                                  verbose_name='Имя виджета админке формата Product.admin_name_OptionSelectFirst.name')
    elements = models.ManyToManyField(OptionSelectElement, related_name='option_check_box_element_first', blank=True,
                                      through='OptionSelectFirstSummary',
                                      through_fields=('option_select', 'option_select_element'))

    def __str__(self):
        return self.admin_name


# Связующая модель виджета селект1
class OptionSelectFirstSummary(models.Model):
    option_select = models.ForeignKey(OptionSelectFirst, on_delete=models.CASCADE)
    option_select_element = models.ForeignKey(OptionSelectElement, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        a = self.option_select.admin_name + ' ' + self.option_select_element.name + ' ' + str(self.price)
        return a


# Виджет селект(Второстепенный)
class OptionSelectSecond(models.Model):
    name = models.CharField(max_length=50)
    admin_name = models.CharField(max_length=50, default='',
                                  verbose_name='Имя виджета админке формата Product.admin_name_OptionSelectSecond.name')
    elements = models.ManyToManyField(OptionSelectElement, related_name='option_check_box_element_second', blank=True,
                                      through='OptionSelectSecondSummary',
                                      through_fields=('option_select', 'option_select_element'))

    def __str__(self):
        return self.admin_name


# Виджет селект(3)
class OptionSelect3(models.Model):
    name = models.CharField(max_length=50)
    admin_name = models.CharField(max_length=50, default='',
                                  verbose_name='Имя виджета админке формата Product.admin_name_OptionSelect3.name')
    elements = models.ManyToManyField(OptionSelectElement, related_name='option_check_box_element_3', blank=True,
                                      through='OptionSelect3Summary',
                                      through_fields=('option_select', 'option_select_element'))

    def __str__(self):
        return self.admin_name


# Связующая модель виджета селект3
class OptionSelect3Summary(models.Model):
    option_select = models.ForeignKey(OptionSelect3, on_delete=models.CASCADE)
    option_select_element = models.ForeignKey(OptionSelectElement, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        a = self.option_select.admin_name + ' ' + self.option_select_element.name + ' ' + str(self.price)
        return a


# Связующая модель виджета селект2
class OptionSelectSecondSummary(models.Model):
    option_select = models.ForeignKey(OptionSelectSecond, on_delete=models.CASCADE)
    option_select_element = models.ForeignKey(OptionSelectElement, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        a = self.option_select.admin_name + ' ' + self.option_select_element.name + ' ' + str(self.price)
        return a


# Виджет селект(проценты)
class OptionSelectPercent(models.Model):
    name = models.CharField(max_length=50)
    admin_name = models.CharField(max_length=50, default='',
                                  verbose_name='Имя виджета админке формата Product.admin_name_OptionSelectPercent.name')
    elements = models.ManyToManyField(OptionSelectElement, related_name='option_check_box_element_percent', blank=True,
                                      through='OptionSelectPercentSummary',
                                      through_fields=('option_select', 'option_select_element'))
    # is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.admin_name


# Связующая модель виджета селект Percent
class OptionSelectPercentSummary(models.Model):
    option_select = models.ForeignKey(OptionSelectPercent, on_delete=models.CASCADE)
    option_select_element = models.ForeignKey(OptionSelectElement, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

    def __str__(self):
        a = self.option_select.admin_name + ' ' + self.option_select_element.name + ' ' + str(self.price)
        return a


# Элементы виджета чекбокс
class OptionCheckBoxElement(models.Model):
    name = models.CharField(max_length=50, )

    def __str__(self):
        return self.name


# Виджет чекбокс1
class OptionCheckBoxFirst(models.Model):
    name = models.CharField(max_length=50)
    admin_name = models.CharField(max_length=50, default='',
                                  verbose_name='Имя виджета админке формата Product.admin_name_OptionCheckBoxFirst.name')
    elements = models.ManyToManyField(OptionCheckBoxElement, related_name='option_check_box_elements_first', blank=True,
                                      through='OptionCheckBoxFirstSummary',
                                      through_fields=('option_check_box', 'option_check_box_element'))

    def __str__(self):
        return self.admin_name


# Связующая можель виджета чекбокс1
class OptionCheckBoxFirstSummary(models.Model):
    option_check_box = models.ForeignKey(OptionCheckBoxFirst, on_delete=models.CASCADE)
    option_check_box_element = models.ForeignKey(OptionCheckBoxElement, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        a = self.option_check_box.admin_name + ' ' + self.option_check_box_element.name + ' ' + str(self.price)
        return a


# Виджет чекбокс(Второстепенный)
class OptionCheckBoxSecond(models.Model):
    name = models.CharField(max_length=50)
    admin_name = models.CharField(max_length=50, default='',
                                  verbose_name='Имя виджета админке формата Product.admin_name_OptionCheckBoxSecond.name')
    elements = models.ManyToManyField(OptionCheckBoxElement, related_name='option_check_box_elements_second',
                                      blank=True,
                                      through='OptionCheckBoxSecondSummary',
                                      through_fields=('option_check_box', 'option_check_box_element'))

    def __str__(self):
        return self.admin_name


# Связующая можель виджета чекбокс2
class OptionCheckBoxSecondSummary(models.Model):
    option_check_box = models.ForeignKey(OptionCheckBoxSecond, on_delete=models.CASCADE)
    option_check_box_element = models.ForeignKey(OptionCheckBoxElement, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        a = self.option_check_box.admin_name + ' ' + self.option_check_box_element.name + ' ' + str(self.price)
        return a


class Game(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название игры')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# Тут хранятся названия полей типа лейбел для продукта
class LabelText(models.Model):
    # admin_name = models.CharField(max_length=50, verbose_name='Имя которое не переводится и отображается только в '
    #                                                           'админке', default='')
    name = models.CharField(max_length=50)
    # Так как из базы данных ничего нельзя удалять, то в случае указания этого атрибута в положение True продукт
    # перестанет отображаться в админке, и для администратора сайта, будет равносильно удалению продукта
    is_hidden = models.BooleanField(default=False, verbose_name='Не отображать в админке On/Of')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# Продукт
class Product(models.Model):
    defpult_select_3 = OptionSelect3.objects.get(name='None').id

    game = models.ForeignKey(Game, verbose_name='Название игры', on_delete=models.CASCADE,
                             related_name='game_slug', default=None)
    category = models.ForeignKey(Category, verbose_name='Имя категории', on_delete=models.CASCADE,
                                 related_name='category_slug', default=None)
    name = models.CharField(max_length=101, verbose_name='Product Name')
    admin_name = models.CharField(max_length=50,
                                  verbose_name='Имя продуктак которое будет использовано для отображения в админке ')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    content = HTMLField(null=True, blank=True, verbose_name='Description')
    title = models.CharField(max_length=80, blank=True, verbose_name='Meta Tag Title')
    description = models.TextField(max_length=160, null=False, blank=True, verbose_name='Meta Tag Description',
                                   default=None)
    option_select_first = models.ForeignKey(OptionSelectFirst, on_delete=models.PROTECT)
    required_select_first = models.BooleanField(default=False, verbose_name='Обязательная или нет поле Select')
    option_select_second = models.ForeignKey(OptionSelectSecond, on_delete=models.PROTECT)
    required_select_second = models.BooleanField(default=False, verbose_name='Обязательная или нет поле Select second')
    option_select_3 = models.ForeignKey(OptionSelect3, on_delete=models.PROTECT, default=defpult_select_3)
    required_select_3 = models.BooleanField(default=False, verbose_name='Обязательная или нет поле Select 3')
    option_select_percent = models.ForeignKey(OptionSelectPercent, on_delete=models.PROTECT, blank=True, null=True,
                                              default=None)
    required_select_percent = models.BooleanField(default=False,
                                                  verbose_name='Обязательная или нет поле select percent')
    option_check_box_first = models.ForeignKey(OptionCheckBoxFirst, related_name='product_checkbox',
                                               on_delete=models.PROTECT)
    required_check_box_first = models.BooleanField(default=False, verbose_name='Обязательная или нет поле Check box')
    option_check_box_second = models.ForeignKey(OptionCheckBoxSecond, related_name='product_checkbox_second',
                                                on_delete=models.PROTECT)
    required_check_box_second = models.BooleanField(default=False,
                                                    verbose_name='Обязательная или нет поле Check box second')
    slug = models.SlugField(unique=True)
    status = models.BooleanField(verbose_name='On/Off', default=True)
    sort_order = models.SmallIntegerField(verbose_name='Sort Order', default=0)
    max_time = models.ManyToManyField(MaxTime, verbose_name='Максимальное время торгов по заказу', blank=True)

    first_label_required = models.BooleanField(default=False, verbose_name='First label required')
    first_label_is_private = models.BooleanField(default=False,
                                                 verbose_name='Является ли значение приватной информацией')
    first_label_name = models.ForeignKey(LabelText, blank=True, null=True, on_delete=models.PROTECT,
                                         related_name='Label_Text1')

    second_label_required = models.BooleanField(default=False, verbose_name='Second label required')
    second_label_is_private = models.BooleanField(default=False,
                                                 verbose_name='Является ли значение приватной информацией')
    second_label_name = models.ForeignKey(LabelText, on_delete=models.PROTECT, blank=True, null=True,
                                          related_name='Label_Text2')

    third_label_required = models.BooleanField(default=False, verbose_name='Third label required')
    third_label_is_private = models.BooleanField(default=False,
                                                 verbose_name='Является ли значение приватной информацией')
    third_label_name = models.ForeignKey(LabelText, on_delete=models.PROTECT, blank=True, null=True,
                                         related_name='Label_Text3')

    fourth_label_required = models.BooleanField(default=False, verbose_name='Fourth label required')
    fourth_label_is_private = models.BooleanField(default=False,
                                                 verbose_name='Является ли значение приватной информацией')
    fourth_label_name = models.ForeignKey(LabelText, on_delete=models.PROTECT, blank=True, null=True,
                                          related_name='Label_Text4')

    fifth_label_required = models.BooleanField(default=False, verbose_name='Fifth label required')
    fifth_label_is_private = models.BooleanField(default=False,
                                                 verbose_name='Является ли значение приватной информацией')
    fifth_label_name = models.ForeignKey(LabelText, on_delete=models.PROTECT, blank=True, null=True,
                                         related_name='Label_Text5')

    # Так как из базы данных ничего нельзя удалять, то в случае указания этого атрибута в положение True продукт
    # перестанет отображаться в админке, и для администратора сайта, будет равносильно удалению продукта
    is_hidden = models.BooleanField(default=False, verbose_name='Не отображать в админке On/Of')
    schedule = models.BooleanField(verbose_name='С расписанием On/Off', default=False)
    need_specific_markup_coefficient = models.BooleanField(default=False,
                        verbose_name='Нужно ли использовать специфические коэффициенты прибыли для данного продукта')
    markup_coefficient_before_15_eur = models.DecimalField(max_digits=8, decimal_places=2,
                        verbose_name='Коэффициент наценки платформы если цена меньше 15 евро', blank=True, null=True, default=0.65)
    markup_coefficient_before_200_eur = models.DecimalField(max_digits=8, decimal_places=2,
                        verbose_name='Коэффициент наценки платформы если цена меньше 200 евро,но больше 15',
                                                            blank=True, null=True, default=0.65)
    markup_coefficient_after_200_eur = models.DecimalField(max_digits=8, decimal_places=2,
                        verbose_name='Коэффициент наценки платформы если цена больше 200 евро', blank=True, null=True, default=0.65)


    class Meta:
        ordering = ['-sort_order']

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING = [(1, 'Bad'), (2, 'Poor'), (3, 'Average'), (4, 'Great'), (5, 'Excellent')]
    review_text = models.TextField(null=True, blank=True)
    rating = models.SmallIntegerField(choices=RATING)
    user_buyer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='user_buyer_review')
    user_driver = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='user_driver_review')
    review_status = models.BooleanField(verbose_name='On/Off', default=True)

    def __str__(self):
        return str(self.pk)


class Invoice(models.Model):
    paid_at = models.DateTimeField(auto_now_add=True, db_index=True)
    amount = models.DecimalField(max_digits=64, decimal_places=2, default=0, blank=True, null=True,
                                 help_text="Amount in Euro")
    status = models.CharField(max_length=30, null=False, default='new')
    payment_system = models.CharField(max_length=50, blank=True, null=True)
    payment_system_email = models.EmailField(
        verbose_name='Имейл пейпал аккаунта который был использован при формировании заказа',
        null=True,
        blank=True
    )


# Заказ
class Order(models.Model):
    STATUS = [('Processing', 'Processing'), ('Pending', 'Pending'), ('Complete', 'Complete'),
              ('Denied', 'Denied'), ('New', 'New'), ('Expired', 'Expired'), ('Paid', 'Paid')]

    # Сколько денег заплатит клиен в евро за заказ
    product_name = models.CharField(max_length=101, verbose_name='Product Name', null=True, blank=True, default=None)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    driver_name = models.CharField(max_length=40, default='', null=True, blank=True)
    driver_skype = models.CharField(max_length=40, default='', null=True, blank=True)
    driver_telegram = models.CharField(max_length=40, default='', null=True, blank=True)
    # Сколько денег получит драйвер за заказ в рублях
    total_rub = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_initial = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    user_buyer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='user_buyer', verbose_name='Buyer')
    user_driver = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                    related_name='user_driver', verbose_name='Driver', default=None)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    max_time = models.SmallIntegerField(default=0, verbose_name='Максимальное время торгов по заказу')
    option_select_first = models.CharField(null=True, blank=True, max_length=200)
    option_select_first_price = models.DecimalField(max_digits=8, decimal_places=2,
                                                    default=0, verbose_name='Стоимость опции select')
    option_select_second = models.CharField(null=True, blank=True, max_length=200)
    option_select_second_price = models.DecimalField(max_digits=8, decimal_places=2,
                                                     default=0, verbose_name='Стоимость опции select_second')
    option_select_percent = models.CharField(null=True, blank=True, max_length=200, default=None)
    option_select_percent_price = models.IntegerField(default=0, verbose_name='На сколько процентов увеличиваем итого')
    option_check_box_first = models.CharField(null=True, blank=True, max_length=200)
    option_check_box_first_price = models.DecimalField(max_digits=8, decimal_places=2,
                                                       default=0, verbose_name='Стоимость опции check_box')
    option_check_box_second = models.CharField(null=True, blank=True, max_length=200)
    option_check_box_second_price = models.DecimalField(max_digits=8, decimal_places=2,
                                                        default=0, verbose_name='Стоимость опции check_box_second')
    review = models.ForeignKey(Review, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Review',
                               default=None)
    invoice = models.OneToOneField(Invoice, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name='order_invoice')

    fraction = models.CharField(blank=True, null=True, default=None, max_length=20)
    # schedule_value1-schedule_value4 Это варианты распеисания от драйвера который закреплен за заказом.
    schedule_value1 = models.DateTimeField(blank=True, null=True)
    schedule_value2 = models.DateTimeField(blank=True, null=True)
    schedule_value3 = models.DateTimeField(blank=True, null=True)
    schedule_value4 = models.DateTimeField(blank=True, null=True)
    # Вариант расписания утрвержденный покупателем
    schedule_value_final = models.DateTimeField(blank=True, null=True)
    # Атрибут отвечающий за то, требуется ли данный ордер делать в режиме piloted
    required_piloted = models.BooleanField(default=False)
    markup_coefficient = models.DecimalField(max_digits=8, decimal_places=2,
                        verbose_name='Коэффициент наценки платформы для текущего ордера, заполняется автоматически',
                        default=0.65)
    label_value = HTMLField(default='', verbose_name='Значение элементов label продукта')
    label_value1 = HTMLField(null=True, blank=True, verbose_name='промежуточное значение')
    label_value_private = HTMLField(default='', verbose_name='Значение приватных элементов label продукта')
    driver_rank = models.CharField(max_length=40, default='Verified')

    def formed_data(self):
        data_format = "%Y-%m-%d %H.%M " + str(ProjectSettings.objects.get(pk=1).time_prefix)
        formed_data = self.published.strftime(data_format)
        return formed_data

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "1. Orders"


class BidedOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='bid_order')
    # Сколько денег заплатит клиен в евро за заказ
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # Сколько денег получит драйвер за заказ в рублях
    total_rub = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    user_driver = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='Driver', default=None)
    schedule_value1 = models.DateTimeField(blank=True, null=True)
    schedule_value2 = models.DateTimeField(blank=True, null=True)
    schedule_value3 = models.DateTimeField(blank=True, null=True)
    schedule_value4 = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.order)


# Отправляем письмо пользователю когда заказ выполнен с предложением оставить отзыв, по это ссылке
# Проверяет количество заказов со статусом Complete и сумму по этим заказам, и если условие тру меняет ранк баера
# https://p.mmo-lvl.com/catalog/customer-orders/{{order_id}}/
@receiver(post_save, sender=Order)
def send_email_for_review(sender, **kwargs):
    if kwargs['instance'].status == 'Complete':
        print("Зашел в проверку ранга покупателя")
        order_for_review = Order.objects.get(pk=kwargs['instance'].pk)
        order_id = order_for_review.pk
        user = order_for_review.user_buyer.first_name
        user_buyer = order_for_review.user_buyer

        #Выполняет проверку создан ли инстанс модели Customer для текущего юзера баера
        try:
            user_buyer_from_Customer = Customer.objects.get(user_buyer=user_buyer)
        except:
            customer = Customer()
            customer.user_buyer = user_buyer
            customer.save()

        customer_orders = Order.objects.all().filter(user_buyer=user_buyer).filter(status='Complete')
        order_total_money = 0
        order_total_quantity = len(customer_orders)
        print(order_total_quantity)
        for i in customer_orders:
            order_total_money = order_total_money + i.total
        print(order_total_money)
        if order_total_quantity > 5 and order_total_money > 100:
            customer = Customer.objects.get(user_buyer=user_buyer)
            customer.rank = 'Base'
            customer.save()
        print(Customer.objects.get(user_buyer=user_buyer).rank)

        s1 = 'Hi ' + str(user) + ' your order ' + str(order_id) + ' has been successfully completed! '
        s2 = 'Please leave a review about the executor of the order at '
        s3 = 'https://nstopboost.com/catalog/customer-orders/' + str(order_id) + "/"
        s4 = 'Best regards, administration https://nstopboost.com/'
        s = s1 + "\n" + s2 + s3 + "\n" + s4
        em = EmailMessage(
            subject=('Your order ' + str(order_id) + ' has been successfully completed'),
            body=s,
            from_email='support@mmo-lvl.com',
            to=[order_for_review.user_buyer.email]
        )
        em.send()
