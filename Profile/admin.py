from django.contrib import admin

from .models import User

admin.site.site_header ="Online JLibrary System"

admin.site.register(User)

# Register your models here.
