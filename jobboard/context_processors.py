from django.conf import settings
from django.db.models import Q, Max
from filer.models import File
from django.contrib.auth.decorators import login_required, permission_required
from home.forms import ContactForm, Article, FormSouscriptionNews
from home.models import articl, SouscripteursNews, SouscripteursNewsManager, Categorie, Section, UploadMagasine
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

def getFileName(request):
   
    #f=UploadMagasine.objects.get(id=UploadMagasine.objects.aggregate(Max('id'))['id__max'])
    f=UploadMagasine.objects.order_by('-id')[:3]
    
    lastArticles=Article.objects.filter(section__section_name='People news', status=1).order_by('-publication_date')[:5]
    sectionArticles=Section.objects.filter(is_SectionMenu=1)
    for sectionArticle in sectionArticles:
        sectionArticle.categorieArticles=Categorie.objects.filter(is_CategorieMenu=1,section=sectionArticle)
    categorieArticles=Categorie.objects.filter(is_CategorieMenu=1)

    #fileName=f.file
    return {'fileName': f,'queryset': request.user,'sectionArticles': sectionArticles,'categorieArticles': categorieArticles,'lastArticles': lastArticles,}

def addSouscripteurNews(request): 
    if request.method == 'POST':  
        formNews = FormSouscriptionNews(request.POST)
        if formNews.is_valid(): 
            email = formNews.cleaned_data["usermail"]
            if SouscripteursNews.objects.filter(usermail=email).exists():
                userExist=True
                message="vous vous êtes déjà inscrit"
                formNews = FormSouscriptionNews()
            else:
                userExist=False
                souscripteur = SouscripteursNews.objects.create_souscripteurs(email)
                souscripteur.save()
                message="l'inscription est passée avec succès !"
                formNews = FormSouscriptionNews()

    else: 
        formNews = FormSouscriptionNews() 
    return locals()

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
        return locals()
 else:
        return redirect("home")