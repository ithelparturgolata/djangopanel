from .models import (
    Spoldzielnia, Smieci, AdministracjaOsiedla, Administrator, Kierownik, Remonty, Przeglady, Finanse, Budynek,
)
from .admin_przeglady import *
from .admin_smieci import *
from .admin_budynek import *
from .admin_finanse import *
from .admin_remonty import *
from .admin_kierownik import *
from .admin_administrator import *
from .admin_energetyka import *
from .admin_smieci import *
from .admin_qr import *


class SpoldzielniaHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['nazwa', 'miasto']
    history_list_display = ['nazwa']
    search_fields = ('nazwa', 'miasto')


admin.site.register(Spoldzielnia, SpoldzielniaHistoryAdmin)


class AdministracjaOsiedlaHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['nazwa', 'ulica']
    history_list_display = ['nazwa']
    search_fields = ('nazwa', 'ulica')


admin.site.register(AdministracjaOsiedla, AdministracjaOsiedlaHistoryAdmin)
