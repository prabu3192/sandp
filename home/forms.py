# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import Article,Categorie

class ContactForm(forms.Form):
    email = forms.EmailField(required=True, label= 'Email')
    obj = forms.CharField(required=True, label='Objet')
    message = forms.CharField(widget = forms.Textarea)

class SearchForm(forms.Form):
    Quoi = forms.CharField(required=False)

class ArticleForm(forms.ModelForm):

    # def __init__(self,  *args, **kwargs):
    #     super(ArticleForm, self).__init__(*args, **kwargs)
    #     section=self.fields['section']
    #     self.fields['categorie']=forms.ModelChoiceField(queryset=Categorie.objects.filter(section__section_name=section)
    #     )
    class Meta:
        model = Article
        fields = ['titre', 'section', 'categorie', 'image', 'contenu']      

class FormSouscriptionNews(forms.Form):
   usermail=forms.EmailField(label ='Inscription Newsletter', widget=forms.TextInput(attrs={'class': 'form-control','id':'input-email','placeholder':'Type your e-mail adress'}))

class CommentForm(forms.Form):
   comment=forms.CharField(label ='', widget=forms.Textarea(attrs={'class': 'form-control','id':'message','placeholder':'votre commentaire','rows':'8'}))
   
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Prénom',widget=forms.TextInput(attrs={'placeholder': 'Prénomsss'}))
    last_name = forms.CharField(max_length=30, label='Nom',widget=forms.TextInput(attrs={'placeholder': 'Nom'}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

