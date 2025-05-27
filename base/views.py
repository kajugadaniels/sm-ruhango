from base.models import *
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

SUPPORTED_LANGS = {
    "en": "English",
    "fr": "Français",
    "rw": "Kinyarwanda",
    "sw": "Kiswahili",
}

def change_language(request: HttpRequest, lang_code: str) -> HttpResponse:
    """
    Store the chosen language in the session and bounce the user back
    to where they came from.  Defaults to English on funny business.
    """
    lang_code = lang_code.lower()
    if lang_code not in SUPPORTED_LANGS:
        lang_code = "en"

    request.session["lang"] = lang_code
    return redirect(request.META.get("HTTP_REFERER", "/"))

def home(request):
    schedules = MassSchedule.objects.all().order_by('-id')[:4]

    context = {
        'schedules': schedules
    }

    return render(request, 'pages/index.html', context)

def massSchedule(request):
    """
    Fetch MassSchedule entries in reverse insertion order,
    paginate at 12 per page, and render the schedule page.
    """
    schedule_list = MassSchedule.objects.all().order_by('-id')
    paginator = Paginator(schedule_list, 3)  # 12 items per page
    page = request.GET.get('page', 1)

    try:
        schedules = paginator.page(page)
    except PageNotAnInteger:
        schedules = paginator.page(1)
    except EmptyPage:
        schedules = paginator.page(paginator.num_pages)

    context = {
        'schedules': schedules
    }

    return render(request, 'pages/mass-schedule.html', context)

def homilies(request):
    return render(request, 'pages/homilies.html')

def healingPrayers(request):
    return render(request, 'pages/healing-prayers.html')

def events(request):
    return render(request, 'pages/events/index.html')

def eventDetails(request):
    return render(request, 'pages/events/show.html')

def testimonies(request):
    return render(request, 'pages/testimonies.html')

def gallery(request):
    return render(request, 'pages/gallery.html')

def donate(request):
    return render(request, 'pages/donate.html')