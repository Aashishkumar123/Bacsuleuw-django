from django.urls import path
from . import views

app_name='myadmin'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/settings/', views.settings_profile, name='settings_profile'),
    path('ajax-profile/settings/', views.ajax_settings_profile, name='ajax_settings_profile'),
    path('customers/policies/', views.policies, name='policies'),
    path('customers/request-policies/', views.request_policies, name='request_policies'),
    path('customer/policy-details/', views.policy_details, name='policy_details'),
    path('login/', views.login, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('customers/', views.customers, name='customers'),
    path('employees/', views.employees, name="employees"),
    path('agency/', views.agency, name="agency"),
    path('pagination/', views.pagination, name="pagination"),
    path('user/register/', views.user_add, name='user_add'),
    path('customer/edit/', views.customer_edit, name='customer_edit'),
    path('agency/edit/', views.agency_edit, name='agency_edit'),
    path('employee/edit/', views.employee_edit, name='employee_edit'),
    path('active_user/', views.active_user, name="active_user"),
    path('delete_user/', views.delete_user, name="delete_user"),
    path('all_groups/', views.all_groups, name="all_groups"),
    path('create_groups/', views.create_groups, name="create_groups"),
    path('employee_dashboard/<int:id>/', views.employee_dashboard, name='employee_dashboard'),
    path('search/user/', views.searcheduser, name="searcheduser"),
    path('agency/info/', views.agency_info, name='agency_info'),
]
