from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

from Profile.managers import UserManager
from django.utils.timezone import now


GENDER_CHOICES = (("male", "Male"), ("female", "Female"))

class User(AbstractUser):
  username = None
  registration_date = models.DateTimeField(default=now, editable=False)
  
  avatar = models.FileField(upload_to='media/avatars/', null=True, blank=True, default="media/default/avatar.png")
  gender = models.CharField(max_length=8,choices=GENDER_CHOICES, default='male',null=True, blank=True)
  
  telephone = models.CharField(max_length=200, null=True, blank=True)
  address = models.CharField(max_length=200, null=True, blank=True)
  birth_date = models.DateField(blank=True, null=True)
  course = models.IntegerField(default=0,null=True, blank=True)
  
  profile_summary = models.TextField(max_length=2000,blank=True, null=True)
  is_active = models.BooleanField(default=True)
  email = models.EmailField(unique=True,blank=False,error_messages={
          "unique": "A user with that email already exists.",
      },
  )
  

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []

  def __unicode__(self):
      return self.email

  objects = UserManager()