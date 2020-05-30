from django.contrib import admin
from django.contrib.sessions.models import Session

# Register your models here.
from .models import Category, Sharetext, Poll, Results

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'visible', )

@admin.register(Sharetext)
class SharetextAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', )

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'type', 'options', 'another', 'another_text', 'share_text', 'category', 'state', 'created_time', 'color', 'repeat', 'repeat_pause')

@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_time', 'poll', 'result', 'input_text', 'user', 'session_key', )

@admin.register(Session)
class ResultsAdmin(admin.ModelAdmin):
    #list_display = ('pk', 'session_key', 'session_data', 'expire_date', 'get_decoded')
    list_display = ('session_key', 'expire_date', 'get_decoded')

