from django import forms
from django.conf import settings
from .models import Kierownik, Administrator, AdministracjaOsiedla, Budynek
from django.core.mail import send_mail
from smsapi.client import SmsApiPlClient


class BulkUpdateForm(forms.Form):
    kierownik = forms.ModelChoiceField(queryset=Kierownik.objects.all(), required=False)
    osiedle = forms.ModelChoiceField(queryset=AdministracjaOsiedla.objects.all(), required=False)
    administrator = forms.ModelChoiceField(queryset=Administrator.objects.all(), required=False)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
    

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label="Wybierz plik Excel")


class FormularzZgloszeniowyForm(forms.Form):
    osiedle = forms.ModelChoiceField(
        queryset=AdministracjaOsiedla.objects.all(),
        label="Wybierz osiedle",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    budynek = forms.ModelChoiceField(
        queryset=Budynek.objects.none(),
        label="Wybierz budynek",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    temat = forms.CharField(
        max_length=100,
        label="Temat zgłoszenia",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="Treść zgłoszenia"
    )
    phone = forms.CharField(
        max_length=15,
        label="Numer telefonu",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np. +48123456789'})
    )

    def __init__(self, *args, **kwargs):
        osiedle_id = kwargs.pop('osiedle_id', None)
        super().__init__(*args, **kwargs)

        if osiedle_id:
            self.fields['budynek'].queryset = Budynek.objects.filter(osiedle_id=osiedle_id)
        elif 'osiedle' in self.data:
            try:
                osiedle_id = int(self.data.get('osiedle'))
                self.fields['budynek'].queryset = Budynek.objects.filter(osiedle_id=osiedle_id)
            except (ValueError, TypeError):
                self.fields['budynek'].queryset = Budynek.objects.none()
        else:
            self.fields['budynek'].queryset = Budynek.objects.none()

    def send_email(self):
        osiedle = self.cleaned_data['osiedle']
        temat = self.cleaned_data['temat']
        content = self.cleaned_data['content']
        phone = self.cleaned_data['phone']
        email_administracja = osiedle.email_administracja

        message = f"Temat: {temat}\n\nTreść: {content}\n\nNumer telefonu: {phone}"
        send_mail(
            subject=temat,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_administracja],
        )

    def send_sms(self):
        phone = self.cleaned_data['phone']
        content = "Twoje zgłoszenie zostało pomyślnie wysłane do administracji. Skontaktujemy się z Tobą wkrótce."

        to_replace = {
            "ą": "a", "Ą": "A", "ś": "s", "Ś": "S", "ę": "e", "Ę": "E",
            "ł": "l", "Ł": "L", "ó": "o", "Ó": "O", "ń": "n", "Ń": "N",
            "ć": "c", "Ć": "C", "ż": "z", "Ż": "Z", "ź": "z", "Ź": "Z",
            '„': "", '”': ""
        }
        for char, replacement in to_replace.items():
            content = content.replace(char, replacement)

        token = "SGfuxxeDr8GYAWMOXp1kzx18ZT5hTuKp60Cw69en"
        client = SmsApiPlClient(access_token=token)
        client.sms.send(to=phone, message=content, from_="SMBUDOWLANI")
