from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from .models import Budynek, QRCode


class QRCodeAdmin(admin.ModelAdmin):
    list_display = ("budynek", "qr_code_image")
    actions = ["generate_qr_code"]

    def generate_qr_code(self, request, queryset):
        for qr in queryset:
            qr.generate_qr_code()
            qr.save()
        self.message_user(request, "Kody QR zostały wygenerowane.")

    generate_qr_code.short_description = "Wygeneruj kod QR"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("generate-qr/<int:budynek_id>/", self.admin_site.admin_view(self.generate_qr_view), name="generate_qr"),
        ]
        return custom_urls + urls

    def generate_qr_view(self, request, budynek_id):
        budynek = Budynek.objects.get(id=budynek_id)
        qr, created = QRCode.objects.get_or_create(budynek=budynek)
        qr.generate_qr_code()
        qr.save()
        self.message_user(request, f"Wygenerowano kod QR dla budynku {budynek.ulica}")
        return redirect("admin:app_budynek_changelist")


admin.site.register(QRCode, QRCodeAdmin)