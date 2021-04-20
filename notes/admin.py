from django.contrib import admin
from .models import Note, BotUser, Tag

# Register your models here.
admin.site.register(Note)
admin.site.register(BotUser)
admin.site.register(Tag)