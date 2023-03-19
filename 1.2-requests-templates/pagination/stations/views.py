from csv import DictReader

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


DATA = []

with open(settings.BUS_STATION_CSV, newline='', encoding='UTF-8') as csvfile:
    reader = DictReader(csvfile)
    for row in reader:
        DATA.append(row)


def bus_stations(request):

    paginator = Paginator(DATA, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }

    return render(request, 'stations/index.html', context)
