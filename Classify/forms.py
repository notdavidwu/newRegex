from django import forms
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.FileInput(attrs={'multiple': True, 'webkitdirectory':True,'directory':True}))
    username = forms.CharField(min_length=0,max_length=1000)
    path = forms.CharField(min_length=0, max_length=1000)