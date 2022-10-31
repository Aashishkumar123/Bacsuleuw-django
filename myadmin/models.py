from email.policy import default
from signal import signal
from django.db import models
from authentication.models import CustomUser
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.
class Policy(models.Model):
    TYPE_CHOICE=(('approved','APPROVED'),
                 ('in progress','IN PROGRESS'),
                 ('success','SUCCESS'),
                 ('rejected','REJECTED'),)
    STATUS_CHOICE=(('active','ACTIVE'),
                   ('inactive','INACTIVE'),)
    policy_number=models.CharField(max_length=20,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    insured=models.CharField(max_length=20,blank=True)
    agent_name=models.CharField(max_length=20,blank=True)
    date_created=models.DateField(auto_now_add=True)
    created_by=models.CharField(max_length=20,blank=True)
    inception_date=models.DateField(null=True, blank=True)
    type=models.CharField(max_length=20,choices=TYPE_CHOICE,default='in progress',blank=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICE,default='inactive',blank=True)
    def __str__(self):
        return self.policy_number

    def save(self, *args, **kwars):
        #channel_layer = get_channel_layer()
        notification_objs = Policy.objects.all().count()
        data= {'count':notification_objs, 'currunt_notification': self.policy_number}
        print(notification_objs)
        #async_to_sync = {}
        super(Policy, self).save(*args, **kwars)

# class Notification(models.Model):
#     policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
#     agent_name=models.CharField(max_length=20,blank=True)
#     status = models.BooleanField(default=False)
#     date_created=models.DateField(auto_now_add=True)