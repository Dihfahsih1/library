from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, FormView, RedirectView

from Profile.forms import *
from Profile.models import User
from django.urls import reverse_lazy
from .forms import *
from django.db import transaction

class student_signup(CreateView):
  model = User
  success_message = 'Your Account has been created sucessfully!'
  success_url = reverse_lazy('Profile:login')
  template_name = "Student/student_signup.html"
  form_class=StudentSignupForm

  def form_valid(self, form):
    context = self.get_context_data()

    with transaction.atomic():
      user = form.save(commit=False)
      password = form.cleaned_data.get("password1")
      user.set_password(password)
      user.save()
      self.object = form.save()
    return super(student_signup, self).form_valid(form)
