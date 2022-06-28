from django.contrib import admin
from lmsApp.models import Category,SubCategory,Books, Students, Borrow

# Register your models here.
# admin.site.register(models.Groups)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Students)
admin.site.register(Borrow)
admin.site.register(Books)
