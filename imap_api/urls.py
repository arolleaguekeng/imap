
from django.urls import path
from imap_api.views import *

urlpatterns = [
    path('save-batiment', batiment_save, name="save-batiment"),
]

