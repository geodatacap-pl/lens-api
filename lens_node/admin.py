from django.contrib import admin
from .models import Endpoint, Detection

admin.site.register(Endpoint)
admin.site.register(Detection)

# Register your models here.
