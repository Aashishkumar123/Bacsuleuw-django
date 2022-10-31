import base64
from docusign_esign import (
    Document,
    Signer,
    EnvelopeDefinition,
    SignHere,
    Tabs,
    Recipients,
    ApiClient
    )
from django.conf import settings
import requests


def get_docusign_access_token(code):
    hostenv = f'https://{settings.DOCUSIGN_HOST_ENV}/oauth/token'
    headers = {'Authorization':f'Basic {settings.DOCUSIGN_ENCODE_KEYS}'}
    data = {'code':code,'grant_type':'authorization_code'}

    response = requests.post(url=hostenv,data=data,headers=headers)
    return response


def make_envelope(args):
    """
    Creates envelope
    args -- parameters for the envelope:
    signer_email, signer_name, signer_client_id
    returns an envelope definition
    """
    path = f'static/documents/Blank-Bascule-Agency-Agreement-Equine-{args["signer_email"]}.pdf'
    with open(path, "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')
    
    # Create the document model
    document = Document( # create the DocuSign document object
        document_base64 = base64_file_content,
        name = 'Example document', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    # Create the signer recipient model
    signer = Signer( # The signer
        email = args['signer_email'], name = args['signer_name'],
        recipient_id = "1", routing_order = "1",
        # Setting the client_user_id marks the signer as embedded
        client_user_id = args['signer_client_id']
    )

    # Create a sign_here tab (field on the document)
    sign_here = SignHere( # DocuSign SignHere field/tab
        anchor_string = '/sn1/', anchor_units = 'pixels',
        anchor_y_offset = '10', anchor_x_offset = '20'
    )

    # Add the tabs model (including the sign_here tab) to the signer
    # The Tabs object wants arrays of the different field/tab types
    signer.tabs = Tabs(sign_here_tabs = [sign_here])

    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject = "Please sign this document sent from the Python SDK",
        documents = [document],
        # The Recipients object wants arrays for each recipient type
        recipients = Recipients(signers = [signer]),
        status = "sent" # requests that the envelope be created and sent.
    )
    return envelope_definition


def create_api_client(base_path, access_token):
    """Create api client and construct API headers"""
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {access_token}")

    return api_client
