from django.contrib import admin
from lmsApp.models import Category,SubCategory,Books, Students, Borrow

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Students)
admin.site.register(Borrow)
admin.site.register(Books)
