from django.urls import path
from dashboard.views.customer import views as customer_view
from dashboard.views.corporate import views as employee_view
from dashboard.views.agency import views as agency_view
from django.contrib.auth import views as auth_view


app_name = "dashboard"


urlpatterns = [
    #customer urls goes here
    path('customer/equine/', customer_view.equine_dashboard, name='equne-customer-dashboard'),
    path('customer/equine/policies/', customer_view.equine_policies, name='equine-customer-policies'),
    path('customer/equine/add-policy-request/', customer_view.add_policy_request, name='add_policy_request'),
    path('customer/equine/policies/policy-detail/', customer_view.equine_policy_details, name='equine-customer-policy-details'),
    path('customer/equine/create/policy/', customer_view.equine_new_policy, name='equine-new-policy'),
    path('customer/equine/horses/', customer_view.equine_horses, name='equine-horses'),
    path('customer/equine/financial/', customer_view.equine_financial, name='equine-financial'),
    path('customer/equine/claims/', customer_view.equine_claims, name='equine-claims'),
    path('customer/equine/documents/', customer_view.equine_documents, name='equine-documents'),
    path('customer/profile/', customer_view.profile, name='customer-profile'),
    path('customer/profile/settings/', customer_view.account_settings, name='customer-account-settings'),
    path('customer/logout/',auth_view.LogoutView.as_view(),name='logout'),


    #agency urls goes here
    path('agency/',agency_view.index,name='agency-dashboard-index'),
    path('agency/policy-details/', agency_view.policy_details, name='policy-delails'),
    path('agency/info/', agency_view.agency_info, name='agency-info'),
    path('agency/get-document/', agency_view.get_document, name='agency-get-document'),
    path('agency/profile/', agency_view.agency_profile, name="agency_profile"),
    path('agency/profile/settings/', agency_view.agency_profile_settings, name="agency_profile_settings"),
    path('agency/document-verified/', agency_view.document_verified, name="document-verified"),
    path('agency/upload-document/', agency_view.upload_agent_document, name="upload-document-agent"),


    # employee urls goes here
    path('employee/',employee_view.index,name='corporate-dashboard-index'),
    path('employee/policy-details/', employee_view.policy_details, name='policy-delails'),
    path('employee/agency-edit/',employee_view.agency_edit, name='agency_edit'),
    path('employee/agency-approve/', employee_view.agency_approve, name="agency-approve"),
    path('employee/agency-disapprove/', employee_view.agency_disapprove, name="agency_disapprove"),
    path('employee/profile/', employee_view.profile, name='customer-profile'),
    path('employee/profile/settings/', employee_view.account_settings, name='customer-account-settings'),
]
