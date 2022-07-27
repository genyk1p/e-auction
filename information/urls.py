from django.urls import path
from information.views import show_info

urlpatterns = [
    path('<slug:information_slug>/', show_info, name='information'),
]