from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from authentication.utils import User
from dashboard.filters import PolicyFilter
from myadmin.models import Policy


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def equine_dashboard(request):
    return render(request, 'dashboard/customer/equine/dashboard.html')

@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def equine_policies(request):
    policy = Policy.objects.filter(user=request.user.id)
    myFilter = PolicyFilter(request.GET, queryset=policy)
    policy = myFilter.qs
    context = {'myFilter': myFilter, 'policy': policy}
    return render(request, 'dashboard/customer/equine/policy.html',context)


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def equine_policy_details(request):
    return render(request, 'dashboard/customer/equine/policy-details.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def equine_new_policy(request):
    return render(request, 'dashboard/customer/equine/new-policy.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def equine_horses(request):
    return render(request, 'dashboard/customer/equine/horses.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def equine_financial(request):
    return render(request, 'dashboard/customer/equine/financial.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def equine_claims(request):
    return render(request, 'dashboard/customer/equine/claims.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def equine_documents(request):
    return render(request, 'dashboard/customer/equine/documents.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def profile(request):
    return render(request,'dashboard/customer/profile.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def account_settings(request):
    return render(request,'dashboard/customer/settings.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'customer')
def add_policy_request(request):
    if request.method == 'POST':
        policynumber = request.POST.get('policynumber')
        userid = request.POST.get('userid')
        user = User.objects.get(id=userid)
        policies = Policy(user=user,policy_number=policynumber)
        policies.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
