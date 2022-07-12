from django.contrib import admin
from lmsApp.models import Category,SubCategory,Books, Profile, Borrow

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Profile)
admin.site.register(Borrow)
admin.site.register(Books)
