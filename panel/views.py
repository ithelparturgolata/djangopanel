from django.http import JsonResponse
from .models import Budynek, Przeglady, Remonty, Smieci, Energetyka, Finanse
from django.core.paginator import Paginator
from datetime import date
from .forms import FormularzZgloszeniowyForm
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q


def dashboard(request):
	query = request.GET.get('q', '')
	budynki_list = Budynek.objects.all()
	
	if query:
		budynki_list = budynki_list.filter(
			Q(ulica__icontains=query)
		)
	
	paginator = Paginator(budynki_list, 8)
	page_number = request.GET.get('page')
	budynki = paginator.get_page(page_number)
	
	return render(request, 'dashboard.html', {'budynki': budynki, 'query': query})


def get_administrator_info(budynek):
	administrator = budynek.osiedle.administratorzy.first()
	if administrator:
		return {
			'imie_administrator': administrator.imie_administrator,
			'nazwisko_administrator': administrator.nazwisko_administrator,
			'komorka_administrator': administrator.komorka_administrator,
			'telefon_stacjonarny': administrator.telefon_stacjonarny_administrator,
			'email_administrator': administrator.email_administrator,
		}
	return None


def get_kierownik_info(budynek):
	kierownik = budynek.osiedle.kierownicy.first() if budynek.osiedle else None
	if kierownik:
		return {
			'imie_kierownik': kierownik.imie_kierownik,
			'nazwisko_kierownik': kierownik.nazwisko_kierownik,
			'email_kierownik': kierownik.email_kierownik,
			'telefon_kierownik': kierownik.telefon_kierownik,
			'foto_kierownik': kierownik.foto_kierownik,
			'osiedle': kierownik.osiedle.nazwa if kierownik.osiedle else None,
		}
	return None


def get_budynek_info(budynek):
	return {
		'indeks': budynek.indeks,
		'ulica': budynek.ulica,
		'kod': budynek.kod,
		'osiedle': budynek.osiedle,
		'telefon_osiedla': budynek.telefon_osiedla,
		'rok_budowy': budynek.rok_budowy,
		'obreb': budynek.obreb,
		'dzialka': budynek.dzialka,
		'laczna_powierzchnia_dzialki': budynek.laczna_powierzchnia_dzialki,
		'powierzchnia_wspolna_budynku': budynek.powierzchnia_wspolna_budynku,
	}


def get_smieci_info(budynek):
	smieci = Smieci.objects.filter(budynek=budynek).first()
	if smieci:
		return {
			'styczen': smieci.styczen,
			'luty': smieci.luty,
			'marzec': smieci.marzec,
			'kwiecien': smieci.kwiecien,
			'maj': smieci.maj,
			'czerwiec': smieci.czerwiec,
			'lipiec': smieci.lipiec,
			'sierpien': smieci.sierpien,
			'wrzesien': smieci.wrzesien,
			'pazdziernik': smieci.pazdziernik,
			'listopad': smieci.listopad,
			'grudzien': smieci.grudzien,
		}
	return None


def get_energetyka_info(budynek):
	energetyka = Energetyka.objects.filter(budynek=budynek).first()
	if energetyka:
		return {
			'termin_podzielniki': energetyka.termin_podzielniki,
			'termin_legalizacji_wodomierzy': energetyka.termin_legalizacji_wodomierzy,
			'uwagi_legalizacja_wodomierzy': energetyka.uwagi_legalizacja_wodomierzy,
			'wymiana_baterii': energetyka.wymiana_baterii,
			'uwagi_wymiana_baterii': energetyka.uwagi_wymiana_baterii,
		}
	return None


def get_finanse_info(budynek):
	finanse = Finanse.objects.filter(budynek=budynek).first()
	if finanse:
		return {
			'fundusz_remontowy': finanse.fundusz_remontowy,
			'zadluzenie_budynku': finanse.zadluzenie_budynku,
		}
	return None


def get_przeglady_info(budynek):
	przeglady = Przeglady.objects.filter(budynek=budynek).first()
	if przeglady:
		return {
			'planowany_przeglad_kominiarski': przeglady.planowany_przeglad_kominiarski,
			'planowany_przeglad_gazowy': przeglady.planowany_przeglad_gazowy,
			'planowany_przeglad_roczny_budynku': przeglady.planowany_przeglad_roczny_budynku,
			'planowany_przeglad_piecioletni_budynku': przeglady.planowany_przeglad_piecioletni_budynku,
			'planowany_przeglad_piecioletni_gazowy': przeglady.planowany_przeglad_piecioletni_gazowy,
			'aktualny_przeglad_kominiarski': przeglady.aktualny_przeglad_kominiarski,
			'aktualny_przeglad_gazowy': przeglady.aktualny_przeglad_gazowy,
			'aktualny_przeglad_roczny_budynku': przeglady.aktualny_przeglad_roczny_budynku,
			'aktualny_przeglad_piecioletni_budynku': przeglady.aktualny_przeglad_piecioletni_budynku,
			'aktualny_przeglad_piecioletni_gazowy': przeglady.aktualny_przeglad_piecioletni_gazowy,
			
		}
	return None


def get_remonty_info(budynek):
	remonty = Remonty.objects.filter(budynek=budynek)
	return [{
		'wykonawca': remont.wykonawca,
		'opis': remont.opis_remontu,
		'poczatek_prac': remont.poczatek_prac,
		'koniec_prac': remont.koniec_prac,
		'uchwala': remont.uchwala.url if remont.uchwala else None,
		'ankieta': remont.ankieta.url if remont.ankieta else None,
		'remont_zakonczony': remont.koniec_prac < date.today() if remont.koniec_prac else False,
	} for remont in remonty]


def budynki_view(request, id=None):
	if id:
		budynek = get_object_or_404(Budynek, id=id)
		
		return render(request, 'details_budynek.html', {
			'budynek_info': get_budynek_info(budynek),
			'przeglady_info': get_przeglady_info(budynek),
			'kierownik_info': get_kierownik_info(budynek),
			'remonty_info': get_remonty_info(budynek),
			'smieci_info': get_smieci_info(budynek),
			'energetyka_info': get_energetyka_info(budynek),
			'finanse_info': get_finanse_info(budynek),
			'administrator_info': get_administrator_info(budynek),
		})
	else:
		budynki = Budynek.objects.all()
		return render(request, 'dashboard.html', {'budynki': budynki})


def pobierz_budynki(request):
	osiedle_id = request.GET.get('osiedle')
	budynki = Budynek.objects.filter(osiedle_id=osiedle_id).values('id', 'ulica')
	return JsonResponse(list(budynki), safe=False)


def formularz_zgloszeniowy(request):
	osiedle_id = request.POST.get('osiedle') if request.method == 'POST' else None
	form = FormularzZgloszeniowyForm(request.POST or None, osiedle_id=osiedle_id)
	
	if request.method == 'POST' and form.is_valid():
		form.send_email()
		form.send_sms()
		return redirect('potwierdzenie')
	
	return render(request, 'form.html', {'form': form})


class ConfirmForm(TemplateView):
	template_name = 'confirm.html'
