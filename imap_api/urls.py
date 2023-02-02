
from django.urls import path
from imap_api.views import *

urlpatterns = [
    path('save-batiment/', batiment_save, name="save-batiment"),
    path('save-etage/', etage_save, name="save-etage"),
    path('save-salle/', salle_save, name="save-salle"),
    path('save-cp/', check_point_save, name="save-cp"),
    path('save-cable/', cable_save, name="save-cable"),

    path('etages', etage_list, name="etages"),
    path('get-path/<str:source>/<str:destination>/', get_routes, name="get-path"),
]

