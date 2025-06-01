from base.models import *
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    """
    Home page: latest 4 MassSchedules, Homilies, Events, Advertisements,
    4 random Rooms, 4 latest Testimonies, and Gallery.
    """
    schedules = MassSchedule.objects.all().order_by("-id")[:4]
    homilies  = Homily.objects.all().order_by("-id")[:4]
    events    = Event.objects.all().order_by("-event_date", "-created_at")[:4]
    adverts   = Advertisement.objects.all().order_by("-published_at", "-created_at")[:4]
    rooms     = Room.objects.order_by("?")[:4]
    testimonies = Testimony.objects.filter(status='published').order_by("-created_at")[:4]
    gallery   = Gallery.objects.all().order_by("-created_at")[:6]

    context = {
        "schedules":   schedules,
        "homilies":    homilies,
        "events":      events,
        "adverts":     adverts,
        "rooms":       rooms,
        "testimonies": testimonies,
        "gallery":     gallery,
    }

    return render(request, "pages/index.html", context)


def massSchedule(request):
    """
    Fetch MassSchedule entries in reverse insertion order,
    paginate at 12 per page, and render the schedule page
    with a sliding window of ±3 page links.
    """
    schedule_list = MassSchedule.objects.all().order_by('-id')
    paginator     = Paginator(schedule_list, 12)
    page_number   = request.GET.get('page', 1)

    try:
        schedules = paginator.page(page_number)
    except PageNotAnInteger:
        schedules = paginator.page(1)
    except EmptyPage:
        schedules = paginator.page(paginator.num_pages)

    current   = schedules.number
    total     = paginator.num_pages
    start     = max(current - 3, 1)
    end       = min(current + 3, total)
    page_range = range(start, end + 1)
    
    context = {
        'schedules':  schedules,
        'page_range': page_range,
    }

    return render(request, 'pages/mass-schedule.html', context)

def homilies(request):
    """
    List homilies, newest first, paginated at 8 per page.
    Only show page links within ±3 of the current page.
    """
    homily_list = Homily.objects.all().order_by('-published_at', '-created_at')
    paginator = Paginator(homily_list, 6)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    current = page_obj.number
    total   = paginator.num_pages
    start   = max(current - 3, 1)
    end     = min(current + 3, total)
    page_range = range(start, end + 1)

    context = {
        'page_obj':    page_obj,
        'page_range':  page_range,
    }

    return render(request, 'pages/homilies.html', context)

def healingPrayers(request):
    return render(request, 'pages/healing-prayers.html')

def events(request):
    """
    Paginated Events listing.
    """
    event_list = Event.objects.all().order_by('-event_date', '-created_at')
    paginator  = Paginator(event_list, 12)
    page       = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    current    = page_obj.number
    total      = paginator.num_pages
    start      = max(current - 3, 1)
    end        = min(current + 3, total)
    page_range = range(start, end + 1)

    context = {
        'page_obj':   page_obj,
        'page_range': page_range,
    }

    return render(request, 'pages/events/index.html', context)

def eventDetails(request, id):
    """
    Show a single Event’s full details.
    """
    event = get_object_or_404(Event, pk=id)

    context = {
        'event': event,
    }

    return render(request, 'pages/events/show.html', context)

def rooms(request):
    pass

def roomDetails(request, id):
    pass

def testimonies(request):
    return render(request, 'pages/testimonies.html')

def gallery(request):
    return render(request, 'pages/gallery.html')

def donate(request):
    return render(request, 'pages/donate.html')