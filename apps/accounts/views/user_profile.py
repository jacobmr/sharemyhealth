from django.http import JsonResponse
from django.views.decorators.http import require_GET
# from apps.fhir.bluebutton.models import Crosswalk
from oauth2_provider.decorators import protected_resource
from django.contrib.auth.decorators import login_required
from collections import OrderedDict
from django.conf import settings


# TODO: include IAL from upstream IDP.
# TO DO: Include the contents of document and address from upstream IDP

# TODO: Must sort the crosswalk and document IDs.

def get_userprofile(user):
    """
    OIDC-style userinfo
    """
    data = OrderedDict()
    data['sub'] = user.username
    data['name'] = "%s %s" % (user.first_name, user.last_name)
    data['given_name'] = user.first_name
    data['family_name'] = user.last_name
    data['email'] = user.email
    data['iat'] = user.date_joined
    data['call_member'] = settings.CALL_MEMBER
    data['call_member_plural'] = settings.CALL_MEMBER
    data['call_organization'] = settings.CALL_ORGANIZATION
    data['call_organization_plural'] = settings.CALL_ORGANIZATION_PLURAL

    # Get the FHIR ID if its there
    # fhir_id = get_fhir_id(user)
    # if fhir_id:
    #    data['patient'] = fhir_id
    return data


@require_GET
@login_required
def oidc_userprofile_test(request):
    """
    OIDC-style userinfo
    """
    user = request.user
    data = OrderedDict()
    data['sub'] = user.username
    data['name'] = "%s %s" % (user.first_name, user.last_name)
    data['given_name'] = user.first_name
    data['family_name'] = user.last_name
    data['email'] = user.email
    data['iat'] = user.date_joined
    data['call_member'] = settings.CALL_MEMBER
    data['call_member_plural'] = settings.CALL_MEMBER
    data['call_organization'] = settings.CALL_ORGANIZATION
    data['call_organization_plural'] = settings.CALL_ORGANIZATION_PLURAL

    # Get the FHIR ID if its there
    # fhir_id = get_fhir_id(user)
    # if fhir_id:
    #     data['patient'] = fhir_id
    return JsonResponse(data)


@require_GET
@protected_resource()
def oidc_userprofile(request):
    user = request.resource_owner
    data = get_userprofile(user)
    return JsonResponse(data)


# TODO Work out crosswalk.
# def get_fhir_id(user):
#
#     r = None
#     if Crosswalk.objects.filter(user=user).exists():
#         c = Crosswalk.objects.get(user=user)
#         r = c.fhir_id
#     return r
