import PIL
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.views.decorators.http import require_POST
from django.contrib.staticfiles import finders
from PIL import Image
from django.conf import settings
import datetime
import calendar

from .form import CardForm
from .models import User, Card, Task


def index(request):
    cards = Card.objects.all()
    card = CardForm()

    if request.method == "POST":
        date = request.POST['month']
    else:
        date = datetime.datetime.now().strftime("%Y-%m")

    calendar_arr, tasks, year, month = get_calendar_with_tasks(date)

    ava = thumbnail_img('images/user.jpg')

    return render(request, 'clientTodo/index.html', {'card': card, 'cards': cards, 'ava': ava, 'calendar_arr': calendar_arr, 'tasks': tasks, 'year': year, 'month': month})


def get_calendar_with_tasks(date):
    c = calendar.Calendar()

    year, month = map(int, date.split('-'))
    calendar_arr = c.monthdayscalendar(year, month)

    tasks = {}

    for i in calendar_arr:
        for j in i:
            if j:
                tasks[str(j)] = []
                t = Card.objects.filter(date=f"{year}-{month:02d}-{j:02d}")
                list_t = list(t)
                if list_t:
                    tasks[j] = list_t

    return calendar_arr, tasks, year, month


def thumbnail_img(image):
    img = finders.find(image)
    img = Image.open(img)
    thumbnail_size = (55, 55)
    img.thumbnail(thumbnail_size, resample=PIL.Image.LANCZOS)
    img.convert('RGB').save(f'{settings.MEDIA_ROOT}/thumbnails/user.png', 'PNG', quality=95)

    return f'{settings.MEDIA_URL}thumbnails/user.png'


@require_POST
def add_card(request):
    year = request.POST.get('year')
    month = request.POST.get('month')
    day = request.POST.get('day')

    date = datetime.date(int(year), int(month), int(day))

    new_card = Card(date=date, user=User.objects.get(id=1))
    new_card.save()

    return redirect('clientTodo:index')


def create_task(request, id):
    if request.method == 'POST':
        card_instance = Card.objects.get(id=id)
        new_task = Task(name=request.POST.get('name'), card=card_instance)
        new_task.save()

        return JsonResponse({'id': new_task.id, 'message': 'Задача успешно добавлена.'})

    return JsonResponse({'error': 'Метод не разрешен.'}, status=405)


def delete_card(request, id=None):
    card = Card.objects.filter(id=id)
    card.delete()

    return redirect('clientTodo:index')


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

