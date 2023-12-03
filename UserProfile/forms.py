
from django import forms

class LikeForm(forms.Form):
    post_id = forms.IntegerField()


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
