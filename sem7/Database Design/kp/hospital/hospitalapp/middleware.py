from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.core.urlresolvers import resolve


class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated():
            current_url = resolve(request.path_info).url_name
            print('current_url:', current_url)
            if current_url not in ('index', 'doctor_login', 'patient_login', 'doctor', 'patient', 'check_user', 'patient_not_found'):
                return HttpResponseRedirect(reverse('hospitalapp:index')) # or http response
        response = self.get_response(request)
        return response