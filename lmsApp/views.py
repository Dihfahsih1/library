from datetime import datetime,timedelta,date
from django.shortcuts import redirect, render,get_object_or_404
import json
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from requests import request
from . models import *
from . forms import *
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db import transaction

def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Nita Library Management',
        'topbar' : True,
        'footer' : True,
    }

    return context
    
def userregister(request):
    context = context_data(request)
    context['topbar'] = False
    context['footer'] = False
    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

def save_register(request):
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form =SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def update_profile(request):
    context = context_data(request)
    context['page_title'] = 'Update Profile'
    user = Profile.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
    else:
        form =UpdateProfile(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)

@login_required
def update_password(request):
    context =context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form =UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form =UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

def login_page(request):
    context = context_data(request)    
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    redirect_to = request.GET.get('next', '')
    current_url = request.path
    if request.POST:
        username = request.POST.get('username')
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
                if current_url == '/login':
                    if user.is_staff:
                        return redirect('home/')
                    else:
                        return redirect('profile-page')
                    
                else:
                    return redirect(redirect_to) 
                    
                # else:
               
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return render(request, 'login.html', context)


def welcome(request):
    return render(request, 'main-page/index.html')

login_required
def home(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['categories'] = Category.objects.filter(delete_flag = 0, status = 1).all().count()
    context['sub_categories'] = SubCategory.objects.filter(delete_flag = 0, status = 1).all().count()
    context['students'] =Profile.objects.filter(delete_flag = 0, status = 1, is_superuser=False).all().count()
    context['books'] =Books.objects.filter(delete_flag = 0, status = 1).all().count()
    context['unapproved'] = Borrow.objects.filter(request_status = 1).all().count()
    context['approved'] = Borrow.objects.filter(request_status = 2).all().count()
    context['transactions'] =Borrow.objects.all().count()

    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect(request.GET.get('next','/'))
    
@login_required
def profile(request):
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)

@login_required
def users(request):
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"
    context['users'] = Profile.objects.exclude(pk=request.user.pk).filter(is_superuser = False).all()
    return render(request, 'users.html', context)

@login_required
def save_user(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            user = Profile.objects.get(id = post['id'])
            form =UpdateUser(request.POST, instance=user)
        else:
            form =SaveUser(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def manage_user(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_user'
    context['page_title'] = 'Manage User'
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = Profile.objects.get(id=pk)
    return render(request, 'manage_user.html', context)

@login_required
def delete_user(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            Profile.objects.filter(pk = pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting User Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def category(request):
    context = context_data(request)
    context['page'] = 'category'
    context['page_title'] = "Category List"
    context['category'] =Category.objects.filter(delete_flag = 0).all()
    return render(request, 'category.html', context)

@login_required
def save_category(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            category = Category.objects.get(id = post['id'])
            form =SaveCategory(request.POST, instance=category)
        else:
            form =SaveCategory(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Category has been saved successfully.")
            else:
                messages.success(request, "Category has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_category'
    context['page_title'] = 'View Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = Category.objects.get(id=pk)
    
    return render(request, 'view_category.html', context)

@login_required
def manage_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_category'
    context['page_title'] = 'Manage Category'
    if pk is None:
        context['category'] = {}
    else:
        context['category'] = Category.objects.get(id=pk)
    
    return render(request, 'manage_category.html', context)

@login_required
def delete_category(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Category ID is invalid'
    else:
        try:
            Category.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Category has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Category Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def sub_category(request):
    context = context_data(request)
    context['page'] = 'sub_category'
    context['page_title'] = "Sub Category List"
    context['sub_category'] = SubCategory.objects.filter(delete_flag = 0).all()
    return render(request, 'sub_category.html', context)

@login_required
def save_sub_category(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            sub_category = SubCategory.objects.get(id = post['id'])
            form = SaveSubCategory(request.POST, instance=sub_category)
        else:
            form = SaveSubCategory(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Sub Category has been saved successfully.")
            else:
                messages.success(request, "Sub Category has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_sub_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_sub_category'
    context['page_title'] = 'View Sub Category'
    if pk is None:
        context['sub_category'] = {}
    else:
        context['sub_category'] = SubCategory.objects.get(id=pk)
    
    return render(request, 'view_sub_category.html', context)

@login_required
def manage_sub_category(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_sub_category'
    context['page_title'] = 'Manage Sub Category'
    if pk is None:
        context['sub_category'] = {}
    else:
        context['sub_category'] = SubCategory.objects.get(id=pk)
    context['categories'] = Category.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_sub_category.html', context)

@login_required
def delete_sub_category(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Sub Category ID is invalid'
    else:
        try:
            SubCategory.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Sub Category has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Sub Category Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def books(request):
    context = context_data(request)
    context['page'] = 'book'
    context['page_title'] = "Book List"
    context['books'] = Books.objects.filter(delete_flag = 0).all()
    return render(request, 'books.html', context)

@login_required
def save_book(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            book = Books.objects.get(id = post['id'])
            form = SaveBook(request.POST, instance=book)
        else:
            form = SaveBook(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Book has been saved successfully.")
            else:
                messages.success(request, "Book has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_book'
    context['page_title'] = 'View Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = Books.objects.get(id=pk)
    
    return render(request, 'view_book.html', context)

@login_required
def manage_book(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_book'
    context['page_title'] = 'Manage Book'
    if pk is None:
        context['book'] = {}
    else:
        context['book'] = Books.objects.get(id=pk)
    context['sub_categories'] = SubCategory.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_book.html', context)

@login_required
def delete_book(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Book ID is invalid'
    else:
        try:
            Books.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Book has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Book Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def students(request):
    context = context_data(request)
    context['page'] = 'student'
    context['page_title'] = "Student List"
    context['students'] = Profile.objects.filter(delete_flag = 0).all()
    return render(request, 'students.html', context)

@login_required
def save_student(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            student = Profile.objects.get(id = post['id'])
            form = SaveStudent(request.POST, instance=student)
        else:
            form = SaveStudent(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Student has been saved successfully.")
            else:
                messages.success(request, "Student has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_student(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_student'
    context['page_title'] = 'View Student'
    if pk is None:
        context['student'] = {}
    else:
        context['student'] = Profile.objects.get(id=pk)
    
    return render(request, 'view_student.html', context)

@login_required
def manage_student(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_student'
    context['page_title'] = 'Manage Student'
    if pk is None:
        context['student'] = {}
    else:
        context['student'] = Profile.objects.get(id=pk)
    context['sub_categories'] = SubCategory.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_student.html', context)

@login_required
def delete_student(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Student ID is invalid'
    else:
        try:
            Profile.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Student has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Student Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def borrows(request):
    context = context_data(request)
    context['page'] = 'borrow'
    context['page_title'] = "Borrowing Transaction List"
    context['borrows'] = Borrow.objects.order_by('status').all()
    return render(request, 'borrows.html', context)

@login_required
def save_borrow(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            borrow = Borrow.objects.get(id = post['id'])
            form =SaveBorrow(request.POST, instance=borrow)
        else:
            form =SaveBorrow(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Borrowing Transaction has been saved successfully.")
            else:
                messages.success(request, "Borrowing Transaction has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_borrow(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_borrow'
    context['page_title'] = 'View Transaction Details'
    if pk is None:
        context['borrow'] = {}
    else:
        context['borrow'] = Borrow.objects.get(id=pk)
    
    return render(request, 'view_borrow.html', context)

@login_required
def manage_borrow(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_borrow'
    context['page_title'] = 'Manage Transaction Details'
    if pk is None:
        context['borrow'] = {}
    else:
        context['borrow'] = Borrow.objects.get(id=pk)
    context['students'] = Profile.objects.filter(delete_flag = 0, status = 1).all()
    context['books'] = Books.objects.filter(delete_flag = 0, status = 1).all()
    return render(request, 'manage_borrow.html', context)

@login_required
def delete_borrow(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            Borrow.objects.filter(pk = pk).delete()
            messages.success(request, "Transaction has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

####View issued book######
def viewissuedbook_view(request):
    issuedbooks=IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(Books.objects.filter(isbn=ib.isbn))
        students=list(StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request,'library/viewissuedbook.html',{'li':li})

######ISSUE BOOK MODULE#######
def issuebook_view(request):
    form=IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=IssuedBookForm(request.POST)
        if form.is_valid():
            obj=IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',{'form':form})

#####Searching Catalogue#############
def search(request):        
    if request.method == 'POST': # this will be GET now      
        book_name =  request.POST.get('search') # do some research what it does       
        try:
            status = Books.objects.filter(title__icontains=book_name) # filter returns a list so you might consider skip except part
        except:
            pass
        context={"books":status, 'item':book_name}
        return render(request,"main-page/search_catalogue.html",context)
    else:
        return render(request,"main-page/search_catalogue.html",{})
    
def book_catalogue(request):
    all_books = Books.objects.all()
    context={'book_list':all_books}
    return render(request,'main-page/book_catalogue.html', context)

@login_required
def book_request(request,pk):
    book=Books.objects.get(id=pk)    
    s = get_object_or_404(Profile, id=str(request.user.id))
    form = SaveBorrow()
    if request.method=="POST":        
        form = SaveBorrow(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"successfully requested for the book")
            return redirect('/')
    
    context={"form":form, 'book':book, 'student':s}
    return render(request, "main-page/book_request_form.html", context)

@login_required
def student_request_issue(request, pk):
    obj = Books.objects.get(id=pk)
    stu=Profile.objects.get(id=request.user.id)
    s = get_object_or_404(Profile, id=str(request.user.id))
    if s.total_books_due < 10:
        messages.success(request,"book has been isuued, You can collect book from library")
        a = Borrow()
        a.student = s
        a.book = obj
        a.issue_date = datetime.datetime.now()
        obj.available_copies = obj.available_copies - 1
        obj.save()
        stu.total_books_due=stu.total_books_due+1
        stu.save()
        a.save()
    else:
        messages.success(request,"you have exceeded limit.")
    return render(request, 'main-page/search_catalogue.html', locals())

def unapproved_book_request(request):
    context = context_data(request)
    context['page_title'] = 'Book Requests'
    qs=Borrow.objects.all()
    context['qs']=qs
    return render(request,'unapproved_book_request.html',context)

def approve_request(request, pk):
    if request.method == "GET":
        Borrow.objects.update(id=pk,request_status=2)
        Books.objects.update(id=pk,status=2)
        messages.success(request, f'Request Approved')
        return redirect('unapproved_book_request')
    
def return_book(equest, pk):
    
##########Student Sign Up############
class student_signup(CreateView):
  model = Profile
  success_message = 'Your Account has been created sucessfully!'
  success_url = reverse_lazy('profile-page')
  template_name = "Student/student_signup.html"
  form_class=StudentSignupForm

  def form_valid(self, form):
    context = self.get_context_data()
    user = form.save(commit=False)
    password = form.cleaned_data.get("password1")
    user.set_password(password)
    user.save()
    self.object = form.save()
    new_user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password1'])
    login(self.request,new_user)
    return super(student_signup, self).form_valid(form)

def view_borrowed_books(request):
    borrowed_books = Borrow.objects.all()
    details = []
    for i in borrowed_books:
        days = (date.today()-i.borrowing_date)
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*1000
        books = list(models.Books.objects.filter(isbn=i.isbn))
        students = list(models.Profile.objects.filter(id=i.student))
        i=0
        for l in books:
            t=(students[i].user,students[i].user_id,books[i].name,books[i].isbn,borrowed_books[0].issued_date,borrowed_books[0].expiry_date,fine)
            i=i+1
            details.append(t)
    return render(request, "view_borrowed_book.html", {'borrowed_books':borrowed_books, 'details':details})