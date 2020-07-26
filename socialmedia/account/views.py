from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages

from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
def home(request):
    return render(request, 'account/signup.html')

def signup(request):
    if request.method == 'POST':
        mail = request.POST.get('email','')
        name = request.POST.get('name','')
        username = request.POST.get('username','')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        duplicate_user = User.objects.filter(username=username)
        duplicate_mail = User.objects.filter(email=mail)

        if password1==password2:
            if duplicate_mail.exists():
                messages.error(request, 'Email already exists. Please use another email')
            else:
                if duplicate_user.exists():
                    messages.error(request, 'Username already taken')
                else:
                    user_obj = User.objects.create_user(first_name=name, email=mail, password = password1, username=username)
                    user_obj.save()
                    messages.success(request, "Successfully registered!")

    return redirect("/")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if user exist in database or not
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,'you are looged in')
            return redirect('/user')
        else:
            messages.error(request, 'incorrect username or password')
            return redirect('/')
def user_logout(request):
    logout(request)
    messages.success(request, "you are looged out")
    return redirect('/')

class Change_Password(TemplateView):
    template_name = "account/password_change.html"

    def post(self, request):
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user = request.user)
            messages.success(request, 'Password Changed Successfully')
            return redirect('/user')
        else:
            messages.error(request, "Wrong Credentials")
            return redirect('/change_password')

    def get(self, request):
        form = PasswordChangeForm(user = request.user)
        return render(request, self.template_name, {'form':form})