# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# dj_rest_auth'un varsayılan Login, Logout, Password Change/Reset görünümlerini dahil ediyoruz
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)

# Kendi RegisterView'inizi import edin!
from users.views import RegisterView as MyRegisterView # <-- Burası kritik! Kendi RegisterView'inizi import edin.
                                                       #    Eğer users/views.py'deki class adı RegisterView ise
                                                       #    burada "as MyRegisterView" diyerek isim çakışmasını önleyebiliriz.


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Kullanıcılar uygulamasının kendi URL'leri.
    path('api/', include('users.urls')), 

    # dj-rest-auth'un standart kimlik doğrulama API'leri (giriş, çıkış vb.)
    path('api/auth/', include('dj_rest_auth.urls')),
    
    # dj-rest-auth ile Django Allauth'un varsayılan kayıt API'leri yerine,
    # KENDİ CustomRegisterSerializer'ınızı kullanan view'inizi burada doğrudan belirtin.
    # ÖNCEKİ: path('api/auth/registration/', include('dj_rest_auth.registration.urls')), # <-- BU SATIR YORUM SATIRI OLMALI VEYA SİLİNMELİ!
    path('api/auth/registration/', MyRegisterView.as_view(), name='rest_register'), # <-- BU SATIR YERİNE GELMELİ!
                                                                                   #     (MyRegisterView'ı import ettiyseniz)
    
    # Django Allauth'un kendi URL'leri
    path('accounts/', include('allauth.urls')), 
]

# Geliştirme ortamında (DEBUG=True ise) medya dosyalarını sunmak için
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)