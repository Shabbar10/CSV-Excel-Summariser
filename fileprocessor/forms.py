from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(label="Upload Excel/CSV File")
    name = forms.CharField(label="Your Name", max_length=100)
