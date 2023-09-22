from django import forms


class CommentProductForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea({'placeholder': 'message'}))
