from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from authentication.decorators import verification_required
from dashboard.helpers import generate_document
from authentication.models import AgentInfo, AgentLicense, AgentDocument
from django.conf import settings
from docusign_esign import EnvelopesApi, RecipientViewRequest
from dashboard.docusign import create_api_client, get_docusign_access_token, make_envelope
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'agency')
@verification_required
def index(request):
    return render(request, 'dashboard/agency/index.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'agency')
@verification_required
def policy_details(request):
    return render(request, 'dashboard/agency/policy-details.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'agency')
def agency_info(request):
    license = AgentLicense.objects.filter(user=request.user)
    other_document = AgentDocument.objects.filter(user=request.user)
    agent_info = AgentInfo.objects.filter(type='EQUINE',user=request.user).first()
    return render(request, 'dashboard/agency/agency-info.html',{'license':license,'other_document':other_document,'agent_info':agent_info})


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'agency')
def get_document(request):
    agency_name = request.POST.get('agency_name')
    agency_address = request.POST.get('agency_address')
    agency_commission = request.POST.get('commissions')
    state = request.POST.get('state')
    city = request.POST.get('city')
    zip = request.POST.get('zip')
    if not agency_name or not agency_address or not agency_commission:
        return JsonResponse({'msg':'ok'})
    documents = AgentInfo.objects.filter(user=request.user,type='EQUINE')
    if not documents.exists():
        AgentInfo.objects.create(
            user = request.user,
            agency_name = agency_name,
            agency_address = agency_address,
            commission = agency_commission,
            state = state,
            city = city,
            zip = zip,
            type = 'EQUINE'
        )
    else:
        document_id = documents.first()
        edit_document = AgentInfo.objects.get(id=document_id.id)
        edit_document.agency_name = agency_name
        edit_document.agency_address = agency_address
        edit_document.commission = agency_commission
        edit_document.state = state
        edit_document.city = city
        edit_document.zip = zip
        edit_document.save()
    document_data = documents.first()
    generate_document(
        agency_name = document_data.agency_name,
        agency_address = document_data.agency_address,
        agency_state = document_data.state,
        agency_city = document_data.city,
        agency_zip = document_data.zip,
        date = document_data.date,
        agent_name = f'{request.user.first_name} {request.user.last_name}',
        agency_commission = document_data.commission,
        email = request.user.email
    )
    return JsonResponse({'msg':'created'})


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'agency')
def sign_document(request):
    code = request.GET.get('code')
    access_token = get_docusign_access_token(code=code).json()

    args = {
        'signer_email':request.user.email,
        'signer_name':f'{request.user.first_name} {request.user.last_name}',
        'signer_client_id':settings.DOCUSIGN_USER_ID,
        'base_path':settings.DOCUSIGN_URI,
        'access_token':access_token['access_token'],
        'account_id':settings.DOCUSIGN_ACCOUNT_ID,
        'signer_client_id':settings.DOCUSIGN_USER_ID
    }
    envelope_definition = make_envelope(args)
        
    # Call Envelopes::create API method
    # Exceptions will be caught by the calling function
    api_client = create_api_client(base_path=args["base_path"], access_token=args["access_token"])
    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id=args["account_id"], envelope_definition=envelope_definition)
    envelope_id = results.envelope_id

    recipient_view_request = RecipientViewRequest(
        authentication_method = 'email',
        client_user_id = settings.DOCUSIGN_USER_ID,
        recipient_id = '1',
        return_url = 'http://127.0.0.1:8000/dashboard/agency/document-verified/',
        user_name = args['signer_name'],
        email = args['signer_email']
    )
    results = envelope_api.create_recipient_view(
            settings.DOCUSIGN_ACCOUNT_ID, envelope_id,
            recipient_view_request = recipient_view_request
            )

    data = {'envelope_id': envelope_id, 'redirect_url': results.url}
    return redirect(data['redirect_url'])


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'agency')
@verification_required
def agency_profile(request):
    return render(request,'dashboard/agency/profile/profile.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'agency')
@verification_required
def agency_profile_settings(request):
    return render(request,'dashboard/agency/profile/settings.html')


@login_required(login_url="/login/")
@user_passes_test(lambda u: u.account_type == 'agency')
def document_verified(request):
    if request.GET.get('event') == 'signing_complete':
        agent = AgentInfo.objects.filter(type='EQUINE',user=request.user).first()
        agent.uploaded = True
        agent.save()
        return render(request,'dashboard/agency/document-submit.html')
    else:
        return render(request,'base/404.html')


@csrf_exempt
def upload_agent_document(request):
    if request.method == "POST" and 'state_license' in request.POST:
        license = request.FILES.get('license')
        state_license = request.POST.get('state_license')
        upload_license = AgentLicense.objects.create(
            user = request.user,
            state = state_license,
            document = license
        )
        data = {
            'id':upload_license.id,
            'license':upload_license.document.url
            }
        return JsonResponse(data)

    if request.method == "POST" and 'name' in request.POST:
        document = request.FILES.get('document')
        name = request.POST.get('name')
        upload_document = AgentDocument.objects.create(
            user = request.user,
            name = name,
            document = document
        )
        data = {
            'id':upload_document.id,
            'name':upload_document.name,
            'license':upload_document.document.url
            }
    return JsonResponse(data)
