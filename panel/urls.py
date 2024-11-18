from django.urls import path
from panel import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('budynki/<int:id>/', views.budynki_view, name='budynki_view'),
    path('formularz-zgloszeniowy/', views.formularz_zgloszeniowy, name='formularz_zgloszeniowy'),
    path('pobierz-budynki/', views.pobierz_budynki, name='pobierz_budynki'),
    path('potwierdzenie/', views.ConfirmForm.as_view(), name='potwierdzenie'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
