# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from smart_selects.db_fields import ChainedForeignKey 

class articl(models.Model):
    Article  ='Article'
    Slide    ='Slide'
    Publicite='Publicite'
    Nouvelle ='Nouvelle'
    
    section_choice=((Article  ,'Article'),
      (Slide    ,'Slide'),
      (Publicite,'Publicite'),
      (Nouvelle ,'Nouvelle'))

    section = models.CharField(max_length=11,
                               choices=section_choice)
    titre = models.CharField(max_length = 200, null = True)
    contenu =RichTextField()
    description = RichTextField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    image100 = models.ImageField(null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=700)
    width_field = models.IntegerField(default=1024)
    timestamp = models.DateTimeField(auto_now_add= datetime.now().replace(microsecond=0), null=True)
    

    def __str__(self):
        return  self.titre

    def __unicode__(self):
        return  self.titre


#create by @ Khadija----------------------------
class SouscripteursNewsManager(models.Manager):   
    def create_souscripteurs(self, usermail):
        souscripteur = self.create(usermail=usermail)
        return souscripteur

class SouscripteursNews(models.Model):
    usermail = models.CharField(max_length = 200, null = False)
    objects = SouscripteursNewsManager()
    def __str__(self):
        return self.usermail


class CommonFields(models.Model):
  slug=models.SlugField(max_length=100)
  description=models.CharField(max_length=500)
  class Meta:
        abstract=True

class Article(CommonFields):
  status_choices=((1,'Publier'),(0,'Dépublier'))
  titre = models.CharField(max_length=100)
  contenu = RichTextUploadingField() #RichTextField()
  #categorie=models.ForeignKey('Categorie')
  auteur = models.ForeignKey(User)
  section=models.ForeignKey('Section')
  categorie = models.ForeignKey('Categorie')
  image = models.ImageField(null=False,
                              blank=False,
                              width_field="width_field",
                              height_field="height_field")
  height_field = models.IntegerField(default=700, verbose_name="Hoteur de l'image")
  width_field = models.IntegerField(default=1024, verbose_name="Largeur de l'image")
  status=models.IntegerField(choices=status_choices)
  publication_date = models.DateTimeField(default=timezone.now, verbose_name="Date de publication")
  update_date = models.DateTimeField(default=timezone.now,verbose_name="Date de modification")
  ratings = GenericRelation(Rating, related_query_name='foos')
  views=models.IntegerField(default=0)
  nbComment=models.IntegerField(default=0)
  
  def __str__(self):  
     
      return self.titre


class Section(CommonFields):
  section_name=models.CharField(max_length=100)
  is_SectionMenu = models.BooleanField(default=False)

  def __str__(self):
    return self.section_name

class Categorie(CommonFields):
  categorie_nom=models.CharField(max_length=100,verbose_name='Nom du categorie')
  section=models.ForeignKey('Section')
  is_CategorieMenu=models.BooleanField(default=False)
  
  def __str__(self):
        return self.categorie_nom

# class Slide(CommonFields):
#   image = models.ImageField(null=True,
#                               blank=True,
#                               width_field="width_field",
#                               height_field="height_field")
#   height_field = models.IntegerField(default=0)
#   width_field = models.IntegerField(default=0)
  
#   def __str__(self):
#         return self.titre

class CommentManager(models.Manager):
      
    def create_comment(self, comment, article, user, date_comment):
        comment = self.create(comment=comment, article=article, user=user, date_comment=date_comment)
        return comment

class Comment(models.Model):
  comment=models.CharField(max_length=500)
  article=models.ForeignKey('Article')
  date_comment=models.DateField(default=date.today)
  user=models.ForeignKey(User)
  objects = CommentManager()
  
  def __str__(self):
    return self.comment
    
class UploadMagasine(models.Model):
    titre=models.CharField(max_length=100)
    fileMagazine = models.FileField(upload_to="magazines", verbose_name='Document')
    image = models.ImageField(null=False,
                              blank=False,verbose_name='Couverture')
    def __str__(self):
      return self.titre
      
    