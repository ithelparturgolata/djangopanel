from .models import Administrator
from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin


class AdministratorHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['imie_administrator', 'nazwisko_administrator', 'osiedle']
    search_fields = ['nazwisko_administrator']
    history_list_display = ['nazwisko_administrator']


admin.site.register(Administrator, AdministratorHistoryAdmin)
