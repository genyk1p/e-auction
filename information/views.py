from django.shortcuts import render
from information.models import Information


def show_info(request, information_slug):
    information = Information.objects.get(slug=information_slug)
    context = {'information': information}
    return render(request, 'information/standard_message.html', context)
