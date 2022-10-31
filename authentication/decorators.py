from django.shortcuts import redirect
from authentication.models import AgentInfo


def login_redirect_dashboard(func):
    def inner(request):
        if request.user.is_authenticated:
            if request.user.account_type == 'customer':
                return redirect('/dashboard/customer/equine/')
            elif request.user.account_type == 'employee':
                return redirect('/dashboard/employee/')
            elif request.user.account_type == 'agency':
                return redirect('/dashboard/agency/')
            else:
                return redirect('/basculeadmin/')
        return func(request)
    return inner


def verification_required(func):
    def inner(request):
        if not request.user.user_profile.verified_equine:
            return redirect('/dashboard/agency/info/')
        return func(request)
    return inner
