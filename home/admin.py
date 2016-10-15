# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html

from home.models import articl, SouscripteursNews
from home.models import Article, Categorie, Section, UploadMagasine

#create by @Khadija
@admin.register(articl)
class AricleAdminBad(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('titre', ), }
    list_display   = ('titre','section',)
    list_filter    = ('section','titre')
    #date_hierarchy = 'date_aparution'
    #ordering       = ('date', )
    search_fields  = ('titre', 'contenu')
    

    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Général', {
            'classes': ['', ],
            'fields': ('titre', 'slug', 'section',)
        }),
        # Fieldset 2 : contenu de l'article

        ('Contenu de l\'article', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('contenu', 'description','image','image100')
        }),
    )
#admin.site.register(UploadFileForm)
admin.site.register(UploadMagasine)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
 prepopulated_fields = {'slug': ('section_name', ), }
 fieldsets = (
               ('Général', {
                    'fields': ('section_name', 'slug', 'description','is_SectionMenu',)
                }),
 )

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
 #form=CategorieAdminForm
 prepopulated_fields = {'slug': ('categorie_nom', ), }
 list_display   = ('categorie_nom','section')
 list_filter    = ('section',)
 fieldsets = (
               ('Général', {
                    'fields': ('categorie_nom', 'slug', 'section','description','is_CategorieMenu',)
                }),
 )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('titre', ), }
    list_display   = ('titre','section','categorie','publication_date','auteur','status_icon')
    list_filter    = ('section','categorie','titre')
    date_hierarchy = 'publication_date'
    ordering       = ('publication_date', )
    search_fields  = ('titre', 'contenu')
    actions=['publish_article','depublish_article']
    fieldsets = (
                # Fieldset 1 : meta-info (titre, auteur…)
               ('Général', {
                    'fields': ('titre', 'slug', 'auteur','section','categorie','status','image','height_field','width_field')
                }),
                # Fieldset 2 : contenu de l'article

                ('Contenu de l\'article', {
                   'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
                   'fields': ('contenu',)
                }),
        )
    def publish_article(self, request, queryset):
        published=queryset.update(status=1)
        if published==1:
            self.message_user(request,"l'article est publié avec succès !")
        else:
            self.message_user(request,"les articles ont été publiés avec succès !")
    publish_article.short_description="Publier les articles séléctionnés"

    def depublish_article(self, request, queryset):
        dep=queryset.update(status=0)
        if dep==1:
            self.message_user(request,"l'article a été dépublié avec succès !")
        else:
            self.message_user(request,"les articles ont été dépubliés avec succès !")
    depublish_article.short_description="Dépublier les articles séléctionnés"

    # def satus_article(self, obj):
    #     status=obj.status
    #     if status==1:
    #         queryset.update(status=1)
    #         message="l'article a été publié avec succès !"
    #         description="Publier les articles séléctionnés"
    #     else:
    #         queryset.update(status=0)
    #         message="l'article a été dépublié avec succès !"
    #         description="Dépublier les articles séléctionnés"
    #     return (message,description)

    def status_icon(self, obj):

        if obj.status==1:
            return True
        else: 
            return False
    status_icon.boolean=True
