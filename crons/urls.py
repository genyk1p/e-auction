from django.urls import path
from crons.views import change_orders_status

urlpatterns = [
    path('check-cron/', change_orders_status, name='check-cron'),
]