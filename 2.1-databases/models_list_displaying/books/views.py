import datetime

from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, template, context)


def sort_by_date(request, pub_date):
    year = int(pub_date.split('-')[0])
    month = int(pub_date.split('-')[1])
    day = int(pub_date.split('-')[2])
    current_date = datetime.date(year=year, month=month, day=day)

    ordered_pub_dates = Book.objects.values('pub_date').order_by('pub_date')

    date_before = ordered_pub_dates.filter(pub_date__lt=current_date)
    if date_before:
        date_before = str(date_before[len(date_before) - 1]['pub_date'])

    date_after = ordered_pub_dates.filter(pub_date__gt=current_date)
    if date_after:
        date_after = str(date_after[0]['pub_date'])

    books = Book.objects.filter(pub_date=current_date)
    template = 'books/sort_date_list.html'

    context = {
        'books': books,
        'date_after': date_after,
        'date_before': date_before,
    }
    return render(request, template, context)
