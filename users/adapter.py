# users/adapter.py

from allauth.account.adapter import DefaultAccountAdapter
from django.db import transaction

class CustomAccountAdapter(DefaultAccountAdapter):
    # Bu metot, allauth bir kullanıcı kaydettiğinde çağrılır.
    # Biz burada allauth'un varsayılan davranışını biraz değiştiriyoruz.
    def save_user(self, request, user, form, commit=True):
        # Önce allauth'un kendi kullanıcı kaydetme mantığını çalıştırıyoruz.
        # super().save_user(...) demek, DefaultAccountAdapter'ın save_user metodunu çağır demek.
        # commit=False: Henüz veritabanına kaydetme, çünkü biz ek alanları da ekleyeceğiz.
        user = super().save_user(request, user, form, commit=False)

        # Şimdi kendi özel alanlarımızı (first_name, last_name, phone_number) ekliyoruz.
        # Bu bilgiler, kayıt formundan (form.cleaned_data) geliyor.
        user.first_name = form.cleaned_data.get('first_name', '')
        user.last_name = form.cleaned_data.get('last_name', '')
        user.phone_number = form.cleaned_data.get('phone_number', None)
        
        # Eğer commit True ise, şimdi kullanıcıyı veritabanına kaydediyoruz.
        if commit:
            user.save() 
        return user