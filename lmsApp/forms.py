
from django import forms
from . models import *

from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
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
    model = Profile
    
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

class SaveUser(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)

    class Meta:
        model = Profile
        fields = ('email', 'username','first_name', 'last_name','password1', 'password2',)

class UpdateProfile(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    # we don't use blank=True or null=True in forms rather we use required
    #current_password = forms.CharField(max_length=250, required=False)

    class Meta:
        model = Profile
        fields = ('avatar','email', 'username','first_name', 'last_name','profile_summary')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = Profile.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Profile.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdateUser(UserChangeForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")

    class Meta:
        model = Profile
        fields = ('email', 'username','first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = Profile.objects.exclude(id=self.cleaned_data['id']).get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = Profile.objects.exclude(id=self.cleaned_data['id']).get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = Profile
        fields = ('old_password','new_password1', 'new_password2')

class SaveCategory(forms.ModelForm):
    name = forms.CharField(max_length=250)
    description = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model =Category
        fields = ('name', 'description', 'status', )

    def clean_name(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            if id > 0:
                category = models.Category.objects.exclude(id = id).get(name = name, delete_flag = 0)
            else:
                category = models.Category.objects.get(name = name, delete_flag = 0)
        except:
            return name
        raise forms.ValidationError("Category Name already exists.")

class SaveSubCategory(forms.ModelForm):
    category = forms.CharField(max_length=250)
    name = forms.CharField(max_length=250)
    description = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model = SubCategory
        fields = ('category', 'name', 'description', 'status', )

    def clean_category(self):
        cid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        try:
            category =Category.objects.get(id = cid)
            return category
        except:
            raise forms.ValidationError("Invalid Category.")

    def clean_name(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        cid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        name = self.cleaned_data['name']
        try:
            category =Category.objects.get(id = cid)
            if id > 0:
                sub_category = models.SubCategory.objects.exclude(id = id).get(name = name, delete_flag = 0, category = category)
            else:
                sub_category = models.SubCategory.objects.get(name = name, delete_flag = 0, category = category)
        except:
            return name
        raise forms.ValidationError("Sub-Category Name already exists on the selected Category.")
     
class SaveBook(forms.ModelForm):
    sub_category = forms.CharField(max_length=250)
    isbn = forms.CharField(max_length=250)
    title = forms.CharField(max_length=250)
    description = forms.Textarea()
    author = forms.Textarea()
    publisher = forms.Textarea()
    date_published = forms.DateField()
    status = forms.CharField(max_length=2)

    class Meta:
        model = Books
        fields = ('isbn', 'sub_category', 'title', 'description', 'author', 'publisher', 'date_published', 'status', )

    def clean_sub_category(self):
        scid = int(self.data['sub_category']) if (self.data['sub_category']).isnumeric() else 0
        try:
            sub_category =SubCategory.objects.get(id = scid)
            return sub_category
        except:
            raise forms.ValidationError("Invalid Sub Category.")

    def clean_isbn(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        isbn = self.cleaned_data['isbn']
        try:
            if id > 0:
                book =Books.objects.exclude(id = id).get(isbn = isbn, delete_flag = 0)
            else:
                book = Books.objects.get(isbn = isbn, delete_flag = 0)
        except:
            return isbn
        raise forms.ValidationError("ISBN already exists on the Database.")
  
class SaveStudent(forms.ModelForm):
    first_name = forms.CharField(max_length=250)
    middle_name = forms.CharField(max_length=250, required= False)
    last_name = forms.CharField(max_length=250)
    gender = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250)
    department = forms.CharField(max_length=250)
    course = forms.CharField(max_length=250)
    address = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'gender', 'telephone', 'email', 'address', 'course', 'status', )

    def clean_code(self):
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        code = self.cleaned_data['code']
        try:
            if id > 0:
                book = models.Books.objects.exclude(id = id).get(code = code, delete_flag = 0)
            else:
                book = models.Books.objects.get(code = code, delete_flag = 0)
        except:
            return code
        raise forms.ValidationError("Student School Id already exists on the Database.")
    
class SaveBorrow(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ('student', 'book', 'borrowing_date', 'return_date', 'status', 'request_status')

    # def clean_student(self):
    #     student = int(self.data['student']) if (self.data['student']).isnumeric() else 0
    #     try:
    #         student =Profile.objects.get(id = student)
    #         return student
    #     except:
    #         raise forms.ValidationError("Invalid student.")
            
    # def clean_book(self):
    #     book = int(self.data['book']) if (self.data['book']).isnumeric() else 0
    #     try:
    #         book =Books.objects.get(id=book)
    #         return book
    #     except:
    #         raise forms.ValidationError("Invalid Book.")

class IssuedBookForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    
    isbn2=forms.ModelChoiceField(queryset=Borrow.objects.filter(status='Returned'),empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn')
    enrollment2=forms.ModelChoiceField(queryset=StudentExtra.objects.all(),empty_label="Name and enrollment",to_field_name='enrollment',label='Name and enrollment')
    
    
class BookRequestForm(forms.Form):
    class Meta:
        model=Borrow
    
