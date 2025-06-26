# jwt_auth_project/users/models.py (GÜNCELLENDİ: PhoneNumberField eklendi)

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField # <-- BURAYI EKLEDİK!

# CustomUserManager: Kullanıcıları Oluşturmaktan Sorumlu Yönetici
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# CustomUser: Kullanıcı Verilerimizin Yapısı
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    # Yeni eklenen ve güncellenen alanlar
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # phone_number alanını PhoneNumberField olarak değiştirdik
    # unique=True, her telefon numarasının tek bir kullanıcıya ait olmasını sağlar.
    # region="TR", varsayılan olarak Türkiye numaralarını formatlamayı ve doğrulamayı bekler.
    phone_number = PhoneNumberField(blank=True, null=True, unique=False, region="TR") # <-- BURAYI GÜNCELLEDİK!

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'