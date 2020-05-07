from django import forms

from .models import Comment


class emailform(forms.Form):

    name=forms.CharField()
    sender=forms.EmailField()
    to=forms.EmailField()
    comment=forms.CharField(required=False,widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=['name','body']
