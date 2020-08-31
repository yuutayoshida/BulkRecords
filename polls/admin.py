from django.contrib import admin
from .models import Save

# Register your models here.

class SaveAdmin(admin.ModelAdmin):
  list_display = ('post_id','title')
  list_display_links = ('post_id','title')

admin.site.register(Save, SaveAdmin)
