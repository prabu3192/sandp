from __future__ import unicode_literals
from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404,redirect,render, render_to_response
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import   HttpResponseRedirect,Http404,HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Max, F
from django.utils import timezone
from .forms import ContactForm, ArticleForm, FormSouscriptionNews, CommentForm
from filer.models import File
from .models import articl, SouscripteursNews, SouscripteursNewsManager, Article, Categorie, Comment, Section
from django.template import RequestContext
from django.conf import global_settings
from django.template import Context
from django.contrib import messages
from datetime import date
from django.template.defaultfilters import slugify
from allauth.account.views import *

import os

#create by Khadija--------------------------

def myhome(request):
    beautyArticles = Article.objects.filter(section__section_name='Beauté',status=1).select_related()[:5]
    fashionArticles = Article.objects.filter(section__section_name='Fashion',status=1).select_related()[:5]
    horoscopeArticles = Article.objects.filter(section__section_name='Horoscope',status=1).select_related()[:5]
    shopingArticles = Article.objects.filter(section__section_name='Shopping',status=1).select_related()[:1]
    popularArticles=Article.objects.order_by('-views')[:5]
    #lastArticles=Article.objects.filter(section__section_name='People news', status=1).order_by('-publication_date')[:5]
    PubArticles=Article.objects.filter(section__section_name='Publicité', status=1).order_by('-publication_date')[:2]
    comments=Comment.objects.order_by('-date_comment')[:5]
    
    context = {
            'queryset': request.user,
            'popularArticles': popularArticles,
            #'lastArticles': lastArticles,
            'horoscopeArticles': horoscopeArticles,
            'shopingArticles': shopingArticles,
            'beautyArticles': beautyArticles,
            'fashionArticles': fashionArticles,
            'PubArticles': PubArticles,
            'comments': comments,       
        }

    return render(request,"home.html", context)

def sendMail(request):
    title = 'Contactez Nous'
    title_align_center = True
    form = ContactForm(request.POST or None)

    if form.is_valid():
        from_email = form.cleaned_data.get("email")
        message = form.cleaned_data.get("message") 
        subject =form.cleaned_data.get("obj")
        to_email = settings.EMAIL_HOST_USER
        if subject and message and from_email:
            try:
                send_mail(subject, message+"envoyé par "+from_email, from_email,[to_email])
                messages.success(request, "Votre message a été envoyé avec success ! Il sera traité dans les meilleurs délais")
            except BadHeaderError:
                messages.success(request, "Invalid header found")
        else:
            messages.success(request, "Vérifier que tous les champs sont saisis et valides")    
        form=ContactForm()
    context = {
        "queryset": request.user,
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "contact.html", context)


# @login_required
# @permission_required('home.add_articl', raise_exception=True)
# def ajout(request):
#     title = 'Ajout'

#     context = {
#         'queryset': request.user,
#         'title'  : title,

#     }

#     return render(request, "ajout.html", context, context_instance=RequestContext(request))

@login_required
@permission_required('home.add_article', raise_exception=True)
def addArticle(request):

    form=ArticleForm()
    title = 'Ajouter article'
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.auteur = request.user
        instance.slug=slugify(instance.titre)
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return redirect('/')
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

def articles(request,id):

    try:
        articleCategories = Article.objects.filter(categorie=id)

    except articl.DoesNotExist:
        raise Http404("Article does not exist")

    context = {
        'queryset': request.user,
        'articleCategories': articleCategories,
        }

    return render(request, "categorieArticle.html", context, context_instance=RequestContext(request))

#Create by Khadija ------------------------------------

def myview(request,id):
    # pub = Article.objects.filter( categorie=Categorie.objects.filter(categorie_nom="Publicité")).order_by('publication_date')[:6]
    # nouvo = Article.objects.filter( categorie=Categorie.objects.filter(categorie_nom="Nouvelle")).order_by('publication_date')[:6]
    # allArticls = Article.objects.filter( categorie=Categorie.objects.filter(categorie_nom="Article")).order_by('publication_date')[:6]
    # myslide = Article.objects.filter( categorie=Categorie.objects.filter(categorie_nom="Slide")).order_by('publication_date')[:6]
    try:       
            articls = Article.objects.get( id=id)
            Article.objects.filter(id=id).update(views=F('views')+1)
            articleComments=Comment.objects.filter(article_id=id)  
            if  request.method == 'POST':  
                commentForm = CommentForm(request.POST)  
                if commentForm.is_valid(): 
                    comment = commentForm.cleaned_data["comment"]
                    comments = Comment.objects.create_comment(comment,articls,request.user,date.today())
                    comments.save()
                    Article.objects.filter(id=id).update(nbComment=F('nbComment')+1)
                    commentForm = CommentForm()
            else:
                commentForm = CommentForm()
    except Article.DoesNotExist:
            raise Http404("Article does not exist")
 
    context = {
        # 'categorie':categories,
        'articles': articls,
        #'allArticls':allArticls,
        'articleComments':articleComments,
        'commentForm':commentForm,
        # 'nouvo': nouvo,
        # 'slide': slide,
        # 'pub': pub,
        'nbComment':articleComments.count(),
        }

    return render(request, "view.html", context, context_instance=RequestContext(request))

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
            messages.info(request,'Aucun article correspondant à votre récherche')
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
    

    return render(request, "home.html",locals(), context_instance=RequestContext(request))

class JointLoginSignupView(LoginView):
    form_class = LoginForm
    signup_form  = SignupForm
    def __init__(self, **kwargs):
        super(JointLoginSignupView, self).__init__(*kwargs)        

    def get_context_data(self, **kwargs):
        ret = super(JointLoginSignupView, self).get_context_data(**kwargs)
        ret['signupform'] = get_form_class(app_settings.FORMS, 'signup', self.signup_form)
        return ret

login = JointLoginSignupView.as_view()