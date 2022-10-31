from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect


class MyAccountAdapter(DefaultAccountAdapter):
    def respond_user_inactive(self, request, user):
        return redirect('/account-inactive/')
