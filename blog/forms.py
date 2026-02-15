from django import forms

from . import models as blog_models

class PostForm(forms.ModelForm):

    def clean(self):
        title = self.cleaned_data.get("title", "")
        if not title: raise forms.ValidationError("Too Empty title, Please write titles")
        return self.cleaned_data

    class Meta:
        model = blog_models.Post
        fields = ['title', 'content', 'publish', 'files', 'images']