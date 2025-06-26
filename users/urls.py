# jwt_auth_project/users/urls.py

from django.urls import path
# Aşağıdaki importlar, eğer dj_rest_auth kullanılıyorsa artık gerekli değildir:
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from users.serializers import MyTokenObtainPairSerializer

# Sadece gerçekten kullandığınız view'leri import edin.
# Eğer sadece ProfileView'ınız özel ve dj_rest_auth tarafından karşılanmıyorsa,
# sadece onu import edin.
from .views import ProfileView # Veya ihtiyacınız olan diğer özel view'ler

urlpatterns = [
    # Bu URL'ler dj_rest_auth ve django-allauth tarafından zaten sağlanıyor.
    # Bu yüzden buradaki tanımlar kaldırılmalıdır!
    # path('login/', TokenObtainPairView.as_view(serializer_class=MyTokenObtainPairSerializer), name='token_obtain_pair'), # KALDIRILDI
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # KALDIRILDI
    # path('register/', views.RegisterView.as_view(), name='auth_register'), # ANA SORUN BUYDU, KALDIRILDI!
    # path('change-password/', views.PasswordChangeView.as_view(), name='change_password'), # KALDIRILDI

    # Sadece dj_rest_auth'un doğrudan sağlamadığı özel endpoint'ler burada kalır.
    # Kullanıcı profilini görüntüleme/güncelleme gibi.
    path('profile/', ProfileView.as_view(), name='auth_profile'),
]