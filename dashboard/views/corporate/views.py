from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from authentication.utils import User


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'employee')
def index(request):
    return render(request, 'dashboard/corporate/index.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'employee')
def policy_details(request):
    return render(request, 'dashboard/corporate/policy-details.html')

@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'employee')
def agency_approve(request):
    users = User.objects.filter(account_type='agency',is_active=True)
    context = {'users':users}
    return render(request, 'dashboard/corporate/agency/agency.html',context)

@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'employee')
def agency_disapprove(request):
    users = User.objects.filter(account_type='agency',is_active=False)
    context = {'users':users}
    return render(request, 'dashboard/corporate/agency/agency.html',context)

@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'employee')
def agency_edit(request):
    id = request.GET.get('id')
    users = User.objects.get(id=id)
    context = {'users':users}
    return render(request, 'dashboard/corporate/agency/edit_user.html',context)

@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'employee')
def profile(request):
    return render(request,'dashboard/corporate/profile/profile.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'employee')
def account_settings(request):
    return render(request,'dashboard/corporate/profile/settings.html')
