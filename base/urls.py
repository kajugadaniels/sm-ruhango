from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('change-language/<str:lang_code>/', change_language, name='change_language'),

    path('', home, name='home'),
    path('mass-schedule/', massSchedule, name='massSchedule'),
    path('homilies/', homilies, name='homilies'),
    path('healing-prayers/', healingPrayers, name='healingPrayers'),
    path('events/', events, name='events'),
    path('events/<int:id>/', eventDetails, name='eventDetails'),
    path('rooms/', rooms, name='rooms'),
    path('room/<int:id>/', roomDetails, name='roomDetails'),
    path('testimonies/', testimonies, name='testimonies'),
    path('members/', members, name='members'),
    path('gallery/', gallery, name='gallery'),
    path('donate/', donate, name='donate'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)