from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

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
    return render(request, 'pages/index.html')

def massSchedule(request):
    return render(request, 'pages/mass-schedule.html')

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