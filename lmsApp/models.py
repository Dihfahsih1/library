from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime,timedelta

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


GENDER_CHOICES = (("male", "Male"), ("female", "Female"))

class Profile(AbstractUser):
  registration_date = models.DateTimeField(default=now, editable=False)
  
  avatar=models.FileField(upload_to='avatars/', null=True, blank=True, default="default/avatar.png")
  gender=models.CharField(max_length=8,choices=GENDER_CHOICES, default='male',null=True, blank=True)
  username=models.CharField(max_length=200, null=True, blank=True)
  telephone=models.CharField(max_length=200, null=True, blank=True)
  address=models.CharField(max_length=200, null=True, blank=True)
  birth_date=models.DateField(blank=True, null=True)
  email=models.EmailField(unique=True)
  course=models.CharField(max_length=200,null=True, blank=True)
  total_books_due=models.IntegerField(default=0)
  delete_flag = models.IntegerField(default = 0)
  profile_summary = models.TextField(max_length=2000,blank=True, null=True)
  status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
  USERNAME_FIELD = "email"
  EMAIL_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  def __unicode__(self):
      return self.email


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Categories"

    def __str__(self):
        return str(f"{self.name}")


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of SubCategories"

    def __str__(self):
        return str(f"{self.name} / {self.name}")

class Books(models.Model):
    book_cover = models.ImageField(upload_to="media/book-covers", blank=True, null=False)
    sub_category = models.ForeignKey(SubCategory, on_delete= models.CASCADE)
    isbn = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    author = models.TextField(blank=True, null= True)
    publisher = models.CharField(max_length=250)
    date_published = models.DateTimeField()
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default=1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Books"

    def __str__(self):
        return self.title

def get_expiry():
    return datetime.today() + timedelta(days=14)
class Borrow(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="student_id_fk", blank=True, null=True)
    book = models.ForeignKey(Books, on_delete= models.CASCADE, related_name="book_id_fk")
    borrowing_date = models.DateField()
    return_date = models.DateField(default=get_expiry)
    status = models.CharField(max_length=2, choices=(('1','Pending'), ('2','Returned')), default = 1)
    request_status = models.CharField(max_length=2, choices=(('1','unapproved'), ('2','approved')), default = 1,blank=True, null=True)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Borrowing Transactions"
  
    def __str__(self):
        return str(f"{self.student}")
class StudentExtra(models.Model):
    user=models.OneToOneField(Profile,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id    
    
 
