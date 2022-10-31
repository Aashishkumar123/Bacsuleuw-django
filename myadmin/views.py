from http.client import HTTPResponse
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate
#from importlib_metadata import PackageNotFoundError
from pytz import country_names
from authentication.decorators import login_redirect_dashboard
from authentication.models import AgentDocument, AgentInfo, AgentLicense, GroupPermission, Profile, UserPassword,CustomPermission
from authentication.utils import User
from authentication.forms import UserGroupForm, GroupAdminForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from authentication.helpers import send_active_email, blank_fields_validation
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, Permission
from myadmin.models import Policy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    return render(request, 'basculeadmin/index.html')

@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def profile(request):
    return render(request, 'basculeadmin/profile/profile.html')

@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def settings_profile(request):
    return render(request, 'basculeadmin/profile/settings.html')

def searcheduser(request):
    string = request.GET.get('string')
    usertype = request.GET.get('usertype')
    users = User.objects.filter(account_type=usertype,first_name__contains=string,last_name__contains=string).values()
    data = list(users)
    return JsonResponse({'data':data})
    
def ajax_settings_profile(request):
     if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        occupation = request.POST.get('occupation')
        user = User.objects.get(id=request.user.id)
        user.first_name = fname
        user.last_name = lname
        user.save()
        profile = Profile.objects.get(user=user)
        profile.company_site = request.POST.get('website')
        profile.phonenumber = request.POST.get('phone')
        profile.company_name = request.POST.get('company')
        profile.country_names = country
        profile.occupation = occupation
        profile.address = address
        if len(request.FILES) != 0:
            if profile.profile_img:
                os.remove(profile.profile_img.path)
            profile.profile_img = request.FILES.get('avatar')
        profile.save()
        return JsonResponse({'status':200})

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
        if user is not None and user.is_superuser:
            auth.login(request,user)
            return JsonResponse({'status':200})
        else:
            return JsonResponse({'error':'username or password is wrong.'})
    return render(request, 'basculeadmin/sign-in.html')


def logout(request):
    auth.logout(request)
    return redirect('/basculeadmin/login/')


@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def customers(request):
    users = User.objects.filter(account_type='customer')
    paginator = Paginator(users, 1) 
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    context = {'users':customers}
    return render(request,'basculeadmin/customer/customers.html',context=context)


@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def agency(request):
    users = User.objects.filter(account_type='agency')
    paginator = Paginator(users, 1)
    page_number = request.GET.get('page')
    agency = paginator.get_page(page_number)
    context = {'users':agency}
    return render(request,'basculeadmin/agency/agency.html',context=context)

def pagination(request):
    users = User.objects.filter(account_type='agency')
    paginator = Paginator(users, 1)
    pagenu = request.GET.get('pagenu')
    page_number = request.GET.get('page')
    agency = paginator.get_page(page_number)
    context = {'users':agency}
    return render(request,'basculeadmin/ajaxagency.html',context=context)

@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def employees(request):
    users = User.objects.filter(account_type='employee')
    paginator = Paginator(users, 1) 
    page_number = request.GET.get('page')
    employee = paginator.get_page(page_number)
    context = {'users':employee}
    return render(request,'basculeadmin/employee/employees.html',context=context)


def active_user(request):
    if request.method == "POST":
        id = request.POST.get('id')
        user = User.objects.get(id=id)
        if user.is_active == 1:
            status = '0'
        else:
            status = '1'
        user.is_active = status
        user.save()
        send_active_email.delay(user.email,status)
        return JsonResponse({'status':200})


def delete_user(request):
    if request.method == "POST":
        try:
            userid = request.POST.getlist('id[]')
            id = request.POST.get('id')
            if userid:
                for id in userid:
                    User.objects.get(id=id).delete()
                return JsonResponse({'status':200})
            User.objects.get(id=id).delete()
            return JsonResponse({'status':200})
        except:
            pass
            


def user_add(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        if user_id is not None:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user = User.objects.get(id=user_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return JsonResponse({'status':200,'msg':'User Update Successfully'})
        else:
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
            user.save()
            userpass = UserPassword(user=user,password=password)
            userpass.save()
            return JsonResponse({'status':200,'account_type':accounttype})
        

def customer_edit(request):
    id = request.GET.get('id')
    users = User.objects.get(id=id)
    return render(request,'basculeadmin/customer/edit_user.html',{'users':users})

def agency_edit(request):
    id = request.GET.get('id')
    users = User.objects.get(id=id)
    return render(request,'basculeadmin/agency/edit_user.html',{'users':users})

def employee_edit(request):
    id = request.GET.get('id')
    users = User.objects.get(id=id)
    return render(request,'basculeadmin/employee/edit_user.html',{'users':users})

@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def policies(request):
    if request.method == 'POST':
        id = request.POST.get('policyid')
        policies = Policy.objects.get(id=id)
        # user = User.objects.get(id=request.POST.get('user'))
        # policies.policy_number = request.POST.get('policy_number')
        # policies.user= user
        policies.insured= request.POST.get('insured')
        policies.agency_name= request.POST.get('agency_name')
        policies.created_by= request.POST.get('created_by')
        policies.inception_date= request.POST.get('inception_date')
        policies.type= request.POST.get('type')
        policies.status= request.POST.get('status')
        policies.save()
        return redirect('/basculeadmin/customers/policies/')
    else:
        inactivepolicy = Policy.objects.filter(status='inactive')
        policies = Policy.objects.filter(status='active')
        context = {'policies':policies,'inactivepolicy':inactivepolicy}
        return render(request, 'basculeadmin/policies.html',context)

@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def request_policies(request):
    policies = Policy.objects.filter(status='inactive')
    context = {'policies':policies}
    return render(request, 'basculeadmin/request-new-policy.html',context)


@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def policy_details(request):
    return render(request, 'basculeadmin/policy-details.html')

@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def all_groups(request):
    if request.method == "POST":
        about_group = request.POST.get('about_group')
        group_pera = request.POST.get('group_pera')
        cperm = CustomPermission(text=about_group,name=group_pera)
        cperm.save()
        return JsonResponse({'status':200})
    else:
        groups = GroupPermission.objects.all()
        roles = CustomPermission.objects.all()
        users = User.objects.all()
        return render(request, 'basculeadmin/all_groups.html',{'groups':groups,'roles':roles,'users':users})

@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def create_groups(request):
        if request.method == "POST":
            group_name = request.POST.get('name')
            pid = request.POST.getlist('rolesid')
            userid = request.POST.getlist('userid')
            user = User.objects.get(id=userid)
            perm = CustomPermission.objects.get(id__in=pid)
            grouppm = GroupPermission(name=group_name)
            grouppm.save()
            grouppm.user.add(user)
            grouppm.permision.add(perm)
            grouppm.save()
            return JsonResponse({'status':200})
        else:
            groups = GroupPermission.objects.all()
            return render(request, 'basculeadmin/create_groups.html',{'groups':groups})
        
@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def agency_info(request):
    id = request.GET.get('id')
    agency_info = AgentInfo.objects.filter(user__id=id)
    agency_doc = AgentDocument.objects.filter(user_id=id)
    agency_license = AgentLicense.objects.filter(user__id=id)
    context={'agency_info':agency_info,'agency_doc':agency_doc,'agency_license':agency_license}
    return render(request,'basculeadmin/agency_info.html',context)


@login_required(login_url='/basculeadmin/login/')
@user_passes_test(lambda u: u.is_superuser)
def employee_dashboard(request,id):
    employee=User.objects.get(id=id)
    context={'employee':employee}
    return render(request,'dashboard/corporate/index.html',context)

