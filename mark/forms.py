from django import forms
from .models import Text


# class TextForm(forms.ModelForm):
#     class Meta:
#         model = Text
#         fields = ('id', 'regexText', 'inputText')
#         #actuall styling 
#         widgets = {
#             'regexText':
#         } 

class TextModelForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('inputText', 'regexText')