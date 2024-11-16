from django import forms

class JPGToPDFForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)

class JPEGToPNGForm(forms.Form):
    file = forms.FileField(required=True)

class MergePDFsForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)

class ResizeImageForm(forms.Form):
    file = forms.FileField(required=True)
    width = forms.IntegerField(required=True)
    height = forms.IntegerField(required=True)

class WordToPDFForm(forms.Form):
    file = forms.FileField(required=True)
