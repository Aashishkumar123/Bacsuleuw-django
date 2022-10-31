from email import policy
from authentication.models import CustomPermission,GroupPermission
from django.contrib import admin
from .models import Policy
# Register your models here.
admin.site.register(Policy)
admin.site.register(CustomPermission)
admin.site.register(GroupPermission)
