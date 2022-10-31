from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from authentication.models import UserPassword
from .helpers import (
    send_email, 
    blank_fields_validation, 
    reset_password_mail, 
    password_validation,
    send_crenditials
    )
from .utils import User
from django.core.cache import cache
import uuid
from django.contrib.auth.hashers import make_password
from authentication.decorators import login_redirect_dashboard


@login_redirect_dashboard
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms = request.POST.get('terms')
        accounttype = request.POST.get('account_type')
        fields_validation = blank_fields_validation(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
                confirm_password = confirm_password,
                terms = terms
                )
        if fields_validation:
            return JsonResponse(fields_validation)
        user = User.objects.create_user(
                email = email,
                first_name = first_name,
                last_name = last_name,
                password = password,
                is_active = False,
                account_type = accounttype
                )
        userpass = UserPassword(user=user,password=password)
        userpass.save()
        if accounttype == 'customer':
            send_email.delay(user.pk,user.email,request.META['HTTP_HOST'])
        user.save()
        request.session['email'] = email
        cache.set(email,password)
        return JsonResponse({'status':200,'accounttype':accounttype})
    account_type = request.GET.get('account_type')
    return render(request, 'authentication/sign-up.html',{'account_type':account_type})


def social_auth(request,name):
    if name is not None:
        user = User.objects.get(id=request.user.id)
        user.account_type = name
        user.save()
        auth.login(request,user)
        if name == 'customer':
            return redirect('/dashboard/customer/equine/')
        elif name == 'employee':
            return redirect('/dashboard/employee/')
        elif name == 'agency':
            return redirect('/dashboard/agency/')
        else:
            return redirect('/')
    else:
        return redirect('/')


@login_redirect_dashboard
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user=authenticate(email=email,password=password)
        data = {}
        if email == '':
            data['email'] = "Email address is required"
        if password == '':
            data['password'] = "Password is required"

        if data:
            return JsonResponse(data)
        if user is not None:
            if user.account_type == 'customer':
                auth.login(request,user)
                return JsonResponse({'status':200,'account_type':'customer'})
            elif user.account_type == 'agency':
                auth.login(request,user)
                return JsonResponse({'status':200,'account_type':'agency'})
            elif user.account_type == 'employee':
                auth.login(request,user)
                return JsonResponse({'status':200,'account_type':'employee'})
        else:
            return JsonResponse({'error':'username or password is wrong.'})
    return render(request, 'authentication/sign-in.html')


@login_redirect_dashboard
def reset_password(request):
    type = request.GET.get('type',None)
    if request.method == "POST":
        type = request.POST.get('type',None)
        email = request.POST.get('email')
        if email == '':
            return JsonResponse({'email':'Email address is required'})
        if '.com' not in email or '@' not in email:
            return JsonResponse({'email':'The value is not a valid email address'})
        try:
            user = User.objects.get(email=email)
            if (User.objects.filter(email=email).exists() 
                    and user.is_customer and user.is_active and user.password):
                token = user.uuid
                reset_password_mail(request,email,token,type)
                return JsonResponse({'status':200})
        except:
            return JsonResponse({'email':'Email address is not exist'})
    return render(request, 'authentication/password-reset.html',{'type':type})


class Verification(View):
    def get(self,request,uidb64,token,email):
        u = User.objects.get(email=email)
        u.is_active = True
        u.save()
        user_auth = authenticate(email=u.email,password=cache.get(email))
        cache.delete(email)
        if user_auth is not None:
            auth.login(request,user_auth)
        #return redirect('authentication:welcome')
        return redirect('authentication:login')


@login_redirect_dashboard
def new_password(request,token,type):
    try:
        validate_token = User.objects.get(uuid=token)
        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            terms = request.POST.get('terms')
            data = {}
            if password == '':
                data['password'] = "The password is required"
            if confirm_password == '':
                data['confirm_password'] = "The confirm password is required"
            elif password != confirm_password:
                data['confirm_password'] = 'The password and its confirm are not the same'
            if terms == 'false':
                data['terms'] = "You must accept the terms and conditions"
            if password_validation(password) is False:
                data['password'] = 'Please enter valid password'
            if data:
                return JsonResponse(data)
            validate_token.password = make_password(password)
            validate_token.uuid = uuid.uuid4()
            validate_token.save()
            return JsonResponse({'status':200,'type':type})
    except:
        return render(request,'base/404.html')
    return render(request,'authentication/new-password.html',{'token':token,'type':type})


def google_login(request):
    user = User.objects.get(email=request.user)
    user.account_type = 'customer'
    user.save()
    return redirect('/dashboard/customer/equine/')


def changemode(request):
    mode = request.POST.get('mode')
    request.session['mode'] = mode
    return JsonResponse({'status':200})


def send_mail_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = UserPassword.objects.get(user=User.objects.get(email=email)).password
        send_crenditials.delay(email, password)
        return JsonResponse({'status':200})
