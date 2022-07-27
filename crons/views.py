from datetime import timedelta
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django_cron import CronJobBase, Schedule
from catalog.models import Order, Driver, BidedOrder
# Для запуска python manage.py runcrons

def work_with_order_status():
    orders = Order.objects.all().filter(status='New')
    for order in orders:
        if timezone.now() > (order.published + timedelta(minutes=order.max_time)):
            bided_order = BidedOrder.objects.all().filter(order=order)
            # Если по ордеру были выполнены ставки то статус будет Pending если ставок не было выполнено сразу
            # будет Expired
            if len(bided_order) != 0:
                order.status = 'Pending'
            else:
                order.status = 'Expired'
                order.save()
    orders = Order.objects.all().filter(status='Pending')
    for order in orders:
        if timezone.now() > (order.published + timedelta(minutes=30)):
            order.status = 'Expired'
            order.save()


# Страничка которую я дергаю извне
def change_orders_status(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    if ip == '159.224.73.228' or ip == '159.224.73.23':
        work_with_order_status()
        return HttpResponse(status=200)  # ok
    return HttpResponse(status=400)  # Bad Request


# Крон задача котора меняет статусы у заказов
class MyCronJob_change_order_status(CronJobBase):
    RUN_EVERY_MINS = 0.1  # every 0.1 mins
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'crons.my_cron_job'

    def do(self):
        print('Выполнил MyCronJob_change_order_status')
        pass
        work_with_order_status()


# Считаем рейтинги для драйверов
class MyCronJob_change_drivers_rank(CronJobBase):
    RUN_EVERY_MINS = 60  # every 60 mins
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'crons.my_cron_job1'

    def do(self):
        print('Выполнил MyCronJob_change_drivers_rank')
        orders = Order.objects.all().filter(status='Complete')
        drivers = User.objects.all().filter(groups__name='Driver')
        for driver in drivers:
            driver_orders = orders.filter(user_driver=driver)
            number_of_review = 0
            rating_sum = 0
            for driver_order in driver_orders:
                if driver_order.review is not None:
                    number_of_review = number_of_review + 1
                    rating_sum = rating_sum + driver_order.review.rating
            if rating_sum != 0:
                average_rating = rating_sum / number_of_review
                try:
                    driver_card = Driver.objects.get(user_driver=driver)
                except:
                    driver_card = Driver()
                    driver_card.user_driver = driver
                driver_card.rating = average_rating
                driver_card.number_done_orders = number_of_review
                driver_card.save()
