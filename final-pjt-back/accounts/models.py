from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=40)
    nickname = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=240)
    age = models.IntegerField(blank=True, null=True)
    maninbank = models.TextField(blank=True, null=True)
    savestyle = models.TextField(blank=True, null=True)
    # 리스트 데이터 저장을 위해 Text 형태로 저장
    financial_products = models.TextField(blank=True, null=True, default="")

    # 관리자 관련
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # 무슨 필드인지는 모르겠지만
    USERNAME_FIELD = 'username'