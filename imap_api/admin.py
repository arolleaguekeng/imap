from django.contrib import admin

# Register your models here.
from imap_api.models import *

admin.site.register(Batiment)
admin.site.register(Salle)
admin.site.register(CheckPoint)
admin.site.register(Cable)
admin.site.register(Etage)

