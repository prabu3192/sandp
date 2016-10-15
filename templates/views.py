# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404,redirect,render, render_to_response
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import   HttpResponseRedirect,Http404,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Max
from django.utils import timezone
from .forms import ContactForm, ArticleForm, FormSouscriptionNews
from filer.models import File
from .models import articl, SouscripteursNews, SouscripteursNewsManager, Article, Categorie
from django.template import RequestContext
from django.conf import global_settings
from django.template import Context
from django.contrib import messages

import os


def home(request):
    title = 'Article'
    articls = articl.objects.filter( section='Article').order_by('-timestamp')[:6]
    pub = articl.objects.filter( section='Publicite').order_by('-timestamp')[:6]
    nouvo = articl.objects.filter( section='Nouvelle').order_by('-timestamp')[:6]
    slide = articl.objects.filter( section='Slide').order_by('-timestamp')[:5]
    sections = ''
    beauty = Article.objects.filter( categorie__categorie_nom='Beauty').order_by('-publication_date')[:3]
    fashion = Article.objects.filter( categorie__categorie_nom='Fashion').order_by('-publication_date')[:3]

    for article in articls :
        sections = article.section
     
    try:
        f=File.objects.get(id=File.objects.aggregate(Max('id'))['id__max'])
        fileName=f.file
    except Exception as e:
        fileName =''
    
    
    
    context = {
            'queryset': request.user,
            'title'  : title,
            'articls': articls,
            'nouvo': nouvo,
            'slide': slide,
            'pub': pub,
            'section': sections,
		    'beauty': beauty,
		    'fashion': fashion,            
        }

    return render_to_response("home.html", context,context_instance=RequestContext(request))

#create by Khadija--------------------------
def myhome(request):
    title = 'Article'
    #slideId=Categorie.objects.filter(nom="Slide")
    
    articls = Article.objects.filter( categorie=Categorie.objects.filter(categorie_nom="Article")).order_by('date')[:6]
    pub = Article.objects.filter( categorie=Categorie.objects.filter(categorie_nom="Publicite")).order_by('date')[:6]
    nouvo = Article.objects.filter( categorie=Categorie.objects.filter(categorie_nom="Nouvelle")).order_by('date')[:6]
    #slide = Slide.objects.all().order_by('date')[:5]

    paginator=Paginator(nouvo,2)
    page=request.GET.get("page")
    try:
        newArticls=paginator.page(page)

    except PageNotAnInteger:
        newArticls=paginator.page(1)
    except EmptyPage:
        newArticls=paginator.page(paginator.num_pages)

    context = {
            'queryset': request.user,
            'title'  : title,
            'articls': articls,
            'nouvo': newArticls,
            #'slide': slide,
            'pub': pub,
            #'section': sections,
            
        }

    return render_to_response("myhome.html", context,context_instance=RequestContext(request))






def contact(request):

    title = 'Contactez Nous'
    title_align_center = True
    form = ContactForm(request.POST or None)

    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        # 	print key, value
        # 	#print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = form.cleaned_data.get("subject")
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'tallkhadija@yahoo.fr']
        contact_message = "%s: %s via %s" % (
            form_full_name,
            form_message,
            form_email)
        some_html_message = """
        <h2>Thank you</h2>
        """
        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  fail_silently=True)
        
    context = {
        "queryset": request.user,
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }

    return render(request, "contact.html", context, context_instance=RequestContext(request))


@login_required
@permission_required('home.add_articl', raise_exception=True)
def ajout(request):
    title = 'Ajout'

    context = {
        'queryset': request.user,
        'title'  : title,

    }

    return render(request, "ajout.html", context, context_instance=RequestContext(request))

@login_required
@permission_required('home.add_articl', raise_exception=True)
def article(request):
    title = 'article'
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        #instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return redirect('home.views.home')

    context = {
    'queryset': request.user,
    'title'  : title,
    'form'   : form,

    }

    return render(request, "article.html", context, context_instance=RequestContext(request))

def slide(request):
    title = 'Slide'


    context = {
        'queryset': request.user,
        'title'  : title,


    }

    return render(request, "slide.html", context)
def nouvo(request):
    title = 'Nouvo'
    context = {
        'queryset': request.user,
        'title'  : title,


    }

    return render(request, "nouvo.html", context, context_instance=RequestContext(request))

def view(request,id):
    title = 'Article'
    pub = articl.objects.filter( section='Publicite').order_by('-timestamp')[:6]
    nouvo = articl.objects.filter( section='Nouvelle').order_by('-timestamp')[:6]
    slide = articl.objects.filter( section='Slide').order_by('-timestamp')[:5]


    try:
        articls = articl.objects.get( id=id)

    except articl.DoesNotExist:
        raise Http404("Article does not exist")

    context = {
        'queryset': request.user,
        'title'  : title,
        'articles': articls,
        'nouvo': nouvo,
        'slide': slide,
        'pub': pub,

        }

    return render(request, "view.html", context, context_instance=RequestContext(request))

#Create by Khadija ------------------------------------

def myview(request,id,categories):
    pub = Article.objects.filter( categorie=Categorie.objects.filter(nom="Publicité")).order_by('date')[:6]
    nouvo = Article.objects.filter( categorie=Categorie.objects.filter(nom="Nouvelle")).order_by('date')[:6]
    allArticls = Article.objects.filter( categorie=Categorie.objects.filter(nom="Article")).order_by('date')[:6]
    myslide = Article.objects.filter( categorie=Categorie.objects.filter(nom="Slide")).order_by('date')[:6]

    try:
        articls = Article.objects.get( id=id)

    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    context = {

        'categorie':categories,
        'articles': articls,
        'allArticls':allArticls,
        'nouvo': nouvo,
        'slide': slide,
        'pub': pub,
        }

    return render(request, "myview.html", context, context_instance=RequestContext(request))

def slideView(request, id):
    try:
        slide=Slide.objects.get(id=id)
    except Slide.DoesNotExist:
        raise Http404("Slide does not exist")
    return render(request,"myview.html",{'slide':slide }, context_instance=RequestContext(request))    

#-------------------- A completer"""

def search_sap(request):
    if request.GET.get("q")!="":
        queryset_list=Article.objects.all()
        query=request.GET.get("q")
        if query:
            queryset_list=queryset_list.filter(
                        Q (titre__icontains=query)|
                        Q (contenu__icontains=query)
                    ).distinct()
        if not queryset_list:
            messages.info(request,'Aucun article correspondant à votre récherche' )

        paginator=Paginator(queryset_list,2)
        page_request_var="page"
        page=request.GET.get(page_request_var)
        try:
            queryset=paginator.page(page)
        
        except PageNotAnInteger:
            queryset=paginator.page(1)

        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)

        context={
                 "obj_list": queryset,
                 "page_request_var": page_request_var
                 }
        return render(request,"search_form.html",context, context_instance=RequestContext(request))
    else:
        return redirect("home")
def addSouscripteurNews(request):

    if request.method == 'POST':  # S'il s'agit d'une requête POST
        formNews = FormSouscriptionNews(request.POST)  # Nous reprenons les données

        if formNews.is_valid(): # Nous vérifions que les données envoyées sont valides
            # Ici nous pouvons traiter les données du formulaire
            email = formNews.cleaned_data["usermail"]
            if SouscripteursNews.objects.filter(usermail=email).exists():
                userExist=True
                message="vous vous êtes déjà inscrit"
                
            else:
                userExist=False
                souscripteur = SouscripteursNews.objects.create_souscripteurs(email)
                souscripteur.save()
                message="l'inscription est passée avec succès !"
        formNews = FormSouscriptionNews()

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        formNews = FormSouscriptionNews()  # Nous créons un formulaire vide
    

    return render(request, "myhome.html",locals(), context_instance=RequestContext(request))

"""@login_required
def getFileName(request):
   
    f=File.objects.get(id=File.objects.aggregate(Max('id'))['id__max'])
    fileName=f.file
    
    context = {
               'fileName': fileName,
        }


    return render(request, "home.html",context, context_instance=RequestContext(request))"""




