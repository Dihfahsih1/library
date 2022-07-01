from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, models,  inlineformset_factory


from Profile.models import User
class StudentSignupForm(UserCreationForm):

  def __init__(self, *args, **kwargs):
    super(StudentSignupForm, self).__init__(*args, **kwargs)
    self.fields["first_name"].label = "First Name"
    self.fields["last_name"].label = "Last Name"
    self.fields["password1"].label = "Password"
    self.fields["password2"].label = "Confirm Password"

    # self.fields['gender'].widget = forms.CheckboxInput()

    self.fields["first_name"].widget.attrs.update(
        {
            "placeholder": "Enter First Name",
        }
    )
    self.fields["last_name"].widget.attrs.update(
        {
            "placeholder": "Enter Last Name",
        }
    )
    self.fields["email"].widget.attrs.update(
        {
            "placeholder": "Enter Email",
        }
    )
    self.fields["password1"].widget.attrs.update(
        {
            "placeholder": "Enter Password",
        }
    )
    self.fields["password2"].widget.attrs.update(
        {
            "placeholder": "Confirm Password",
        }
    )

  class Meta:
    model = User
    
    exclude = ()
    fields = [
        "first_name", "last_name", 'avatar', 'gender',
        'birth_date', 'telephone','profile_summary','course',"email", "password1",  "password2",
        
    ]
    error_messages = {
        "first_name": {
            "required": "First name is required",
            "max_length": "Name is too long",
        },
        "last_name": {
            "required": "Last name is required",
            "max_length": "Last Name is too long",
        },
        "gender": {"required": "Gender is required"},
    }

  def clean_gender(self):
    gender = self.cleaned_data.get("gender")
    if not gender:
        raise forms.ValidationError("Gender is required")
    return gender

  def save(self, commit=True):
    user = super(UserCreationForm, self).save(commit=False)
    if commit:
      user.save()
    return user
