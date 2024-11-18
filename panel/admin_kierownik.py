from os import path
from .models import (Administrator, Finanse, Budynek, Kierownik)
from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from openpyxl import load_workbook
from django.shortcuts import render, redirect
from django.urls import path
from .forms import ExcelImportForm


class KierownikHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['imie_kierownik', 'nazwisko_kierownik', 'osiedle']
    history_list_display = ['osiedle']
    search_fields = ('nazwisko_kierownik', 'osiedle')


admin.site.register(Kierownik, KierownikHistoryAdmin)
