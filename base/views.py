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
    homilies = Homily.objects.all().order_by('-id')[:4]

    context = {
        'schedules': schedules,
        'homilies': homilies,
    }

    return render(request, 'pages/index.html', context)


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
    Titles and content are pulled from the session’s lang code
    into `localized_title` and `localized_content` on each Homily.
    """
    homily_list = Homily.objects.all().order_by('-published_at', '-created_at')
    paginator   = Paginator(homily_list, 8)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Pick the right fields for title & content
    lang           = request.session.get('lang', 'en')
    title_field    = f"title_{lang}"
    content_field  = f"content_{lang}"

    # Annotate each homily with localized_title & localized_content
    for homily in page_obj:
        homily.localized_title   = getattr(homily, title_field) or homily.title_en
        homily.localized_content = getattr(homily, content_field) or homily.content_en

    # Build sliding window of page links ±3
    current   = page_obj.number
    total     = paginator.num_pages
    start     = max(current - 3, 1)
    end       = min(current + 3, total)
    page_range = range(start, end + 1)

    context = {
        'page_obj':   page_obj,
        'page_range': page_range,
    }

    return render(request, 'pages/homilies.html', context)

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