from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from .utils import token_generator
from django.template.loader import get_template
import re
from .utils import User
from celery import shared_task


@shared_task(name="email_send")
def send_email(pk,user_email,host):
    uidb64 = urlsafe_base64_encode(force_bytes(pk))
    link = reverse(
        'authentication:activate',
        kwargs={'uidb64':uidb64,'email':user_email,'token':token_generator.make_token(pk)}
        )
    active_link ='http://'+host+link
    email_subject ='Activate your account'
    context = {'link':active_link}
    message = get_template('authentication/verification-email.html').render(context)
    email = EmailMessage(
            email_subject,
            message,
            'noreplay@gmail.com',
            [user_email],
        )
    email.content_subtype="html"
    email.send(fail_silently=False)


@shared_task(name="email_send_activation")
def send_active_email(user_email,status):
    if status == '1':
        userstatus = 'Active'
    else:
        userstatus = 'In-active'
    email_subject = f'{userstatus} your account'
    context = {'userstatus':userstatus}
    message = get_template('authentication/userstatus-email.html').render(context)
    email = EmailMessage(
            email_subject,
            message,
            'noreplay@gmail.com',
            [user_email],
        )
    email.content_subtype="html"
    email.send(fail_silently=False)


@shared_task(name="send_crenditials")
def send_crenditials(email,password):
    email_subject = 'Your Crenditials'
    context = {'email':email,'password':password}
    message = get_template('authentication/send-password-email.html').render(context)
    email = EmailMessage(
            email_subject,
            message,
            'noreplay@gmail.com',
            [email],
        )
    email.content_subtype="html"
    email.send(fail_silently=False)

def password_validation(password):
    pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
    result = re.findall(pattern, password)
    if(result):
        return True
    return False


def blank_fields_validation(**kwargs):
    blank_fields = {}
    if kwargs.get('first_name') == '':
        blank_fields['first_name'] = 'First Name is required'
    if kwargs.get('last_name') == '':
        blank_fields['last_name'] = 'Last Name is required'
    if kwargs.get('email') == '':
        blank_fields['email'] = 'Email is required'
    elif '.com' not in kwargs.get('email') or '@' not in kwargs.get('email'):
        blank_fields['email'] = 'The value is not a valid email address.'
    elif User.objects.filter(email=kwargs.get('email')).exists():
        blank_fields['email'] = 'This email is already taken'
    if kwargs.get('password') == '':
        blank_fields['password'] = 'The password is required'
    elif password_validation(kwargs.get('password')) is False:
        blank_fields['password'] = 'Please enter valid password'
    if kwargs.get('confirm_password') == '':
        blank_fields['confirm_password'] = 'The password confirmation is required'
    elif kwargs.get('password') != kwargs.get('confirm_password'):
        blank_fields['confirm_password'] = 'The password and its confirm are not the same'
    if kwargs.get('terms') == 'false':
        blank_fields['terms'] = 'You must accept the terms and conditions'
    return blank_fields


def reset_password_mail(request,email,token,type):
    link = reverse(
        'authentication:new-password',
        kwargs={'token':token,'type':type}
        )
    active_link = f'http://{request.META["HTTP_HOST"]}{link}'
    email_subject ='Reset Your Bascule Password'
    context = {'link':active_link}
    message = get_template('authentication/reset-password-verification.html').render(context)
    email = EmailMessage(
            email_subject,
            message,
            'noreplay@gmail.com',
            [email],
        )
    email.content_subtype="html"
    email.send(fail_silently=False)
