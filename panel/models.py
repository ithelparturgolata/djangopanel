from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
import re
from django.core.exceptions import ValidationError
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import User


class Spoldzielnia(models.Model):
	nazwa = models.CharField(max_length=100, unique=True)
	miasto = models.CharField(max_length=100)
	ulica = models.CharField(max_length=100)
	kod = models.CharField(max_length=10)
	rok_zalozenia = models.PositiveIntegerField()
	email = models.EmailField(null=True, blank=True)
	strona_www = models.URLField(max_length=200, null=True, blank=True)
	facebook = models.URLField(max_length=200, null=True, blank=True)
	instagram = models.URLField(max_length=200, null=True, blank=True)
	linkedin = models.URLField(max_length=200, null=True, blank=True)
	history = HistoricalRecords()
	
	def clean(self):
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.nazwa):
			raise ValidationError({'nazwa': "Pole 'Nazwa' może zawierać tylko litery z polskiego alfabetu."})
		
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.miasto):
			raise ValidationError({'miasto': "Pole 'Miasto' może zawierać tylko litery z polskiego alfabetu."})
		
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż0-9\s]+$', self.ulica):
			raise ValidationError(
				{'ulica': "Pole 'Ulica' może zawierać tylko litery polskiego alfabetu, cyfry oraz spacje."})
		
		if not re.match(r'^\d{2}-\d{3}$', self.kod):
			raise ValidationError({'kod': "Pole 'Kod' musi być w formacie xx-xxx, gdzie x to cyfry."})
	
	def save(self, *args, **kwargs):
		if re.match(r'^\d{6}$', self.kod):
			self.kod = f'{self.kod[:3]}-{self.kod[2:]}'
		super().save(*args, **kwargs)
	
	def __str__(self):
		return f'{self.nazwa} | {self.miasto}'
	
	class Meta:
		verbose_name = _('Spółdzielnia')
		verbose_name_plural = _('Spółdzielnia')


class AdministracjaOsiedla(models.Model):
	nazwa = models.CharField(max_length=100, null=True, blank=True)
	ulica = models.CharField(max_length=100, null=True, blank=True)
	telefon = models.CharField(max_length=15, null=True, blank=True)
	email_administracja = models.EmailField(null=True, blank=True)
	spoldzielnia = models.ForeignKey('Spoldzielnia', on_delete=models.CASCADE, related_name='administracje')
	history = HistoricalRecords()
	
	def clean(self):
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.nazwa):
			raise ValidationError({'nazwa': "Pole 'Nazwa' może zawierać tylko litery polskiego alfabetu i spacje."})
		
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż0-9\s]+$', self.ulica):
			raise ValidationError(
				{'ulica': "Pole 'Ulica' może zawierać tylko litery polskiego alfabetu, cyfry oraz spacje."})
		
		if not re.match(r'^\d+$', self.telefon):
			raise ValidationError({'telefon': "Pole 'Telefon' może zawierać tylko cyfry."})
	
	def __str__(self):
		return f'{self.nazwa}'
	
	class Meta:
		verbose_name = _('Administracja Osiedla')
		verbose_name_plural = _('Administracje Osiedli')


class Kierownik(models.Model):
	imie_kierownik = models.CharField(max_length=100, null=True, blank=True)
	nazwisko_kierownik = models.CharField(max_length=100, null=True, blank=True)
	imie_zastepca = models.CharField(max_length=100, null=True, blank=True)
	nazwisko_zastepca = models.CharField(max_length=100, null=True, blank=True)
	email_kierownik = models.EmailField(null=True, blank=True)
	telefon_kierownik = models.CharField(max_length=15, null=True, blank=True)
	osiedle = models.ForeignKey('AdministracjaOsiedla', on_delete=models.CASCADE, related_name='kierownicy')
	foto_kierownik = models.ImageField(blank=True, null=True, upload_to='fotos/')
	history = HistoricalRecords()
	
	def clean(self):
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.imie_kierownik):
			raise ValidationError(
				{'imie_kierownik': "Pole 'Imię' może zawierać tylko litery polskiego alfabetu i spacje."})
		
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.nazwisko_kierownik):
			raise ValidationError(
				{'nazwisko_kierownik': "Pole 'Nazwisko' może zawierać tylko litery polskiego alfabetu i spacje."})
		
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.imie_zastepca):
			raise ValidationError(
				{'imie_zastepca': "Pole 'Imię' może zawierać tylko litery polskiego alfabetu i spacje."})
		
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.nazwisko_zastepca):
			raise ValidationError(
				{'nazwisko_zastepca': "Pole 'Nazwisko' może zawierać tylko litery polskiego alfabetu i spacje."})
		
		if not re.match(r'^\d+$', self.telefon_kierownik):
			raise ValidationError({'telefon_kierownik': "Pole 'Telefon komórkowy' może zawierać tylko cyfry."})
	
	def __str__(self):
		return f'{self.imie_kierownik} {self.nazwisko_kierownik} | {self.osiedle}'
	
	class Meta:
		verbose_name = _('Kierownik')
		verbose_name_plural = _('Kierownik')


class Administrator(models.Model):
	imie_administrator = models.CharField(max_length=100, null=True, blank=True)
	nazwisko_administrator = models.CharField(max_length=100, null=True, blank=True)
	email_administrator = models.EmailField(null=True, blank=True)
	komorka_administrator = models.CharField(max_length=15, null=True, blank=True)
	telefon_stacjonarny_administrator = models.CharField(max_length=15, null=True, blank=True)
	foto_administrator = models.ImageField(blank=True, null=True, upload_to='fotos/')
	osiedle = models.ForeignKey('AdministracjaOsiedla', on_delete=models.CASCADE, related_name='administratorzy')
	history = HistoricalRecords()
	
	def clean(self):
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.imie_administrator):
			raise ValidationError(
				{'imie_administrator': "Pole 'Imię' może zawierać tylko litery polskiego alfabetu i spacje."})
		
		if not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+$', self.nazwisko_administrator):
			raise ValidationError(
				{'nazwisko_administrator': "Pole 'Nazwisko' może zawierać tylko litery polskiego alfabetu i spacje."})
		
		if not re.match(r'^\d+$', self.komorka_administrator):
			raise ValidationError({'komorka_administrator': "Pole 'Telefon komórkowy' może zawierać tylko cyfry."})
		
		if not re.match(r'^\d+$', self.telefon_stacjonarny_administrator):
			raise ValidationError(
				{'telefon_stacjonarny_administrator': "Pole 'Telefon stacjonarny' może zawierać tylko cyfry."})
	
	def __str__(self):
		return f'{self.imie_administrator} {self.nazwisko_administrator} | {self.osiedle}'
	
	class Meta:
		verbose_name = _('Administrator')
		verbose_name_plural = _('Administrator')


class Budynek(models.Model):
	indeks = models.CharField(max_length=10, unique=True, null=True, blank=True)
	ulica = models.CharField(max_length=100)
	kod = models.CharField(max_length=10, null=True, blank=True)
	kierownik = models.ForeignKey('Kierownik', on_delete=models.SET_NULL, null=True, blank=True, related_name='budynki')
	osiedle = models.ForeignKey('AdministracjaOsiedla', on_delete=models.CASCADE, null=True, blank=True,
								related_name='budynki')
	spoldzielnia = models.ForeignKey('Spoldzielnia', on_delete=models.CASCADE, null=True, blank=True,
									 related_name='budynki')
	administrator = models.ForeignKey('Administrator', on_delete=models.SET_NULL, null=True, blank=True,
									  related_name='budynki')
	foto = models.ImageField(upload_to='budynki_foto/', null=True, blank=True)
	rok_budowy = models.CharField(max_length=20, null=True, blank=True)
	telefon_osiedla = models.CharField(max_length=20, null=True, blank=True)
	obreb = models.CharField(max_length=100, null=True, blank=True)
	dzialka = models.CharField(max_length=50, null=True, blank=True)
	laczna_powierzchnia_dzialki = models.CharField(max_length=50, null=True, blank=True)
	powierzchnia_wspolna_budynku = models.CharField(max_length=50, null=True, blank=True)
	history = HistoricalRecords()
	
	def __str__(self):
		return f'{self.ulica} | {self.administrator}'
	
	class Meta:
		verbose_name = _('Budynek')
		verbose_name_plural = _('Budynki')


class Finanse(models.Model):
	budynek = models.ForeignKey('Budynek', on_delete=models.CASCADE, related_name='finanse')
	fundusz_remontowy = models.CharField(max_length=50, null=True, blank=True)
	zadluzenie_budynku = models.CharField(max_length=50, null=True, blank=True)
	history = HistoricalRecords()
	
	def clean(self):
		if not re.match(r'^[0-9,;.]*$', self.fundusz_remontowy):
			raise ValidationError(
				{'fundusz_remontowy': "Pole 'Fundusz remontowy' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.zadluzenie_budynku):
			raise ValidationError(
				{'zadluzenie_budynku': "Pole 'Zadłużenie budynku' może zawierać tylko cyfry oraz znaki: , ; ."})
	
	def __str__(self):
		return f'{self.budynek.ulica}'
	
	class Meta:
		verbose_name = _('Finanse')
		verbose_name_plural = _('Finanse')


class Remonty(models.Model):
	budynek = models.ForeignKey('Budynek', on_delete=models.CASCADE, related_name='remonty')
	wykonawca = models.CharField('Wykonawca', max_length=100, null=True, blank=True)
	opis_remontu = models.TextField(null=True, blank=True)
	poczatek_prac = models.DateField(null=True, blank=True)
	koniec_prac = models.DateField(null=True, blank=True)
	uchwala = models.FileField(upload_to='uchwaly/', null=True, blank=True)
	ankieta = models.FileField(upload_to='ankiety/', null=True, blank=True)
	history = HistoricalRecords()
	
	def __str__(self):
		return f'{self.wykonawca} | {self.budynek.ulica} | {self.koniec_prac}'
	
	class Meta:
		verbose_name = _('Remonty')
		verbose_name_plural = _('Remonty')


class Przeglady(models.Model):
	budynek = models.ForeignKey('Budynek', on_delete=models.CASCADE, related_name='przeglady')
	planowany_przeglad_kominiarski = models.CharField(_('Planowany przegląd kominiarski'), max_length=255, blank=True,
													  null=True)
	planowany_przeglad_gazowy = models.CharField(_('Planowany przegląd gazowy'), max_length=255, blank=True, null=True)
	planowany_przeglad_roczny_budynku = models.CharField(_('Planowany roczny przegląd budynku'), max_length=255,
														 blank=True, null=True)
	planowany_przeglad_piecioletni_budynku = models.CharField(_('Planowany pięcioletni przegląd budynku'),
															  max_length=255, blank=True, null=True)
	planowany_przeglad_piecioletni_gazowy = models.CharField(_('Planowany pięcioletni przegląd gazowy'), max_length=255,
															 blank=True, null=True)
	
	aktualny_przeglad_kominiarski = models.CharField(_('Aktualny przegląd kominiarski'), max_length=255, blank=True,
													 null=True)
	aktualny_przeglad_gazowy = models.CharField(_('Aktualny przegląd gazowy'), max_length=255, blank=True, null=True)
	aktualny_przeglad_roczny_budynku = models.CharField(_('Aktualny roczny przegląd budynku'), max_length=255,
														blank=True, null=True)
	aktualny_przeglad_piecioletni_budynku = models.CharField(_('Aktualny pięcioletni przegląd budynku'), max_length=255,
															 blank=True, null=True)
	aktualny_przeglad_piecioletni_gazowy = models.CharField(_('Aktualny pięcioletni przegląd gazowy'), max_length=255,
															blank=True, null=True)
	history = HistoricalRecords()
	
	def __str__(self):
		return f'{self.budynek.ulica}'
	
	class Meta:
		verbose_name = _('Przeglądy')
		verbose_name_plural = _('Przeglądy')


class Energetyka(models.Model):
	budynek = models.ForeignKey('Budynek', on_delete=models.CASCADE, related_name='energetyka')
	termin_podzielniki = models.CharField(_('Okres rozliczeniowy'), max_length=255)
	termin_legalizacji_wodomierzy = models.CharField(_('Termin legalizacji wodomierzy'), max_length=255, null=True,
													 blank=True)
	uwagi_legalizacja_wodomierzy = models.TextField(_('Uwagi legalizacja wodomierzy'), null=True, blank=True)
	wymiana_baterii = models.CharField(_('Wymiana baterii'), max_length=255, null=True, blank=True)
	uwagi_wymiana_baterii = models.TextField(_('Uwagi wymiana baterii'), null=True, blank=True)
	history = HistoricalRecords()
	
	def __str__(self):
		return f'{self.budynek.ulica}'
	
	class Meta:
		verbose_name = _('Energetyka')
		verbose_name_plural = _('Energetyka')


class Smieci(models.Model):
	budynek = models.ForeignKey('Budynek', on_delete=models.CASCADE, related_name='smieci', null=True, blank=True)
	styczen = models.CharField(max_length=255, default='', blank=True, null=True)
	luty = models.CharField(max_length=255, default='', blank=True, null=True)
	marzec = models.CharField(max_length=255, default='', blank=True, null=True)
	kwiecien = models.CharField(max_length=255, default='', blank=True, null=True)
	maj = models.CharField(max_length=255, default='', blank=True, null=True)
	czerwiec = models.CharField(max_length=255, default='', blank=True, null=True)
	lipiec = models.CharField(max_length=255, default='', blank=True, null=True)
	sierpien = models.CharField(max_length=255, default='', blank=True, null=True)
	wrzesien = models.CharField(max_length=255, default='', blank=True, null=True)
	pazdziernik = models.CharField(max_length=255, default='', blank=True, null=True)
	listopad = models.CharField(max_length=255, default='', blank=True, null=True)
	grudzien = models.CharField(max_length=255, default='', blank=True, null=True)
	history = HistoricalRecords()
	
	def clean(self):
		if not re.match(r'^[0-9,;.]*$', self.styczen):
			raise ValidationError({'styczen': "Pole 'Styczeń' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.luty):
			raise ValidationError({'luty': "Pole 'luty' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.marzec):
			raise ValidationError(
				{'marzec': "Pole 'Marzec' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.kwiecien):
			raise ValidationError(
				{'kwiecien': "Pole 'Kwiecień' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.maj):
			raise ValidationError(
				{'maj': "Pole 'Maj' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.czerwiec):
			raise ValidationError(
				{'czerwiec': "Pole 'Czerwiec' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.lipiec):
			raise ValidationError(
				{'lipiec': "Pole 'Lipiec' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.sierpien):
			raise ValidationError(
				{'sierpien': "Pole 'Sierpień' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.wrzesien):
			raise ValidationError(
				{'wrzesien': "Pole 'Wrzesień' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.pazdziernik):
			raise ValidationError(
				{'pazdziernik': "Pole 'Październik' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.listopad):
			raise ValidationError(
				{'listopad': "Pole 'Listopad' może zawierać tylko cyfry oraz znaki: , ; ."})
		
		if not re.match(r'^[0-9,;.]*$', self.grudzien):
			raise ValidationError(
				{'grudzien': "Pole 'Grudzień' może zawierać tylko cyfry oraz znaki: , ; ."})
	
	def __str__(self):
		return f'{self.budynek}'
	
	class Meta:
		verbose_name = _('Śmieci')
		verbose_name_plural = _('Śmieci')


class QRCode(models.Model):
	budynek = models.OneToOneField(Budynek, on_delete=models.CASCADE, related_name="qrcode")
	qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
	
	def generate_qr_code(self):
		url = f"https://smbudowlani.panelmieszkanca.com/blok/details2.php?details=1#administracja{self.budynek.id}"
		qr = qrcode.make(url)
		qr_io = BytesIO()
		qr.save(qr_io, format="PNG")
		self.qr_code_image.save(f"{self.budynek.ulica}_qr.png", ContentFile(qr_io.getvalue()), save=False)
	
	def save(self, *args, **kwargs):
		if not self.qr_code_image:
			self.generate_qr_code()
		super().save(*args, **kwargs)
	
	def __str__(self):
		return f"Kod QR dla {self.budynek.ulica}"
	
	class Meta:
		verbose_name = _('Kody QR')
		verbose_name_plural = _('Kody QR')
