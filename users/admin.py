# jwt_auth_project/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # Django'nun varsayılan UserAdmin'ini import ediyoruz
from .models import CustomUser

# CustomUser modelini admin panelinde göstermek ve özelleştirmek için
# Django'nun UserAdmin sınıfını genişletiyoruz.
class CustomUserAdmin(UserAdmin):
    # Admin listeleme sayfasında gösterilecek alanlar
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active')

    # Kullanıcı düzenleme formundaki alanların düzeni
    # Django'nun UserAdmin'indeki varsayılan alanları korurken
    # phone_number ve profile_picture'ı "Personal info" kısmına ekliyoruz.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Yeni kullanıcı ekleme formundaki alanların düzeni
    add_fieldsets = (
        (None, {
            'classes': ('wide',), # Bu stil sınıfı formun genişliğini ayarlar
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'phone_number'),
        }),
    )
    # Admin arama çubuğunda arama yapılabilecek alanlar
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    # Admin listesinde varsayılan sıralama
    ordering = ('email',)
    # Many-to-Many ilişkiler için özel widget (isteğe bağlı, ama daha kullanışlı)
    filter_horizontal = ('groups', 'user_permissions',) 

# CustomUser modelini CustomUserAdmin sınıfını kullanarak admin paneline kaydet
admin.site.register(CustomUser, CustomUserAdmin)