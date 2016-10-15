# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User, Permission, Group
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect


def about(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        title = "RAJOUT D'UNE OFFRE"

        return HttpResponseRedirect(reverse('home.views.home'))

        context = {
            "title": title,
        }
    return render(request, "about.html", context)

def permission_denied_view(request):
	return render(request, '403.html', )