# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""jobboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static
from django.contrib import admin
#from home.views import  IndexView

urlpatterns = patterns('',
    #url(r'^', include('jobboard.home.urls', namespace="home")),
    #url(r'^grappelli/', include('grappelli.urls')), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home.views.myhome', name='home'),
    url(r'^contact/$', 'home.views.sendMail', name='sendMail'),
	url(r'^legal/$', 'home.views.legal', name='legal'),
	url(r'^tos/$', 'home.views.tos', name='tos'),
	url(r'^publicity/$', 'home.views.publicity', name='publicity'),
	url(r'^mobileapp/$', 'home.views.mobileapp', name='mobileapp'),
	url(r'^subscription/$', 'home.views.subscription', name='subscription'),
	url(r'^sitemap/$', 'home.views.sitemap', name='sitemap'),
	url(r'^magazine/$', 'home.views.magazine', name='magazine'),
    #url(r'^ajout/$', 'home.views.ajout', name='ajout'),
    url(r'^article/$', 'home.views.addArticle', name='addarticle'),
    url(r'^nouvo/$', 'home.views.nouvo', name='nouvo'),
    url(r'^slide/$', 'home.views.slide', name='slide'),
    url(r'^search/$', 'home.views.search_sap', name='search'),
    #url(r'^souscriptionnews/', 'home.views.addSouscripteurNews', name='news'),
    url(r'^myview/(?P<id>[0-9]+)/$', 'home.views.myview', name='myview'),
    url(r'^categories/(?P<id>[0-9]+)/$', 'home.views.articles', name='categories'),
    #url(r'^myview/(?P<id>[0-9]+)/categorie=(?P<categories>[a-z]+)', 'home.views.myview', name='myview'),
    url(r'^slideview/(?P<id>[0-9]+)/$', 'home.views.slideView', name='slide'),
    url(r'^about/$', 'jobboard.views.about', name='about'),
    #url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^filer/', include('filer.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^chaining/', include('smart_selects.urls')),



    

)
handler403 = 'jobboard.views.permission_denied_view'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
