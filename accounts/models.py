from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # 사용 x
    first_name = None
    last_name = None

    # 사용 o
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20,unique=True)
    phone = models.CharField(max_length=15,unique=True)
    created = models.DateTimeField(auto_now_add=True)

    # 로그인 id로 사용할 필드
    USERNAME_FIELD = 'phone'
    # 필수 작성 필드
    REQUIRED_FIELDS = ['username','email']

    def __str__(self):
        return self.username
    
