
from django import forms

class LikeForm(forms.Form):
    post_id = forms.IntegerField()

