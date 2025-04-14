from django import forms
from django.core.validators import FileExtensionValidator

class UploadFileForm(forms.Form):
	file = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),validators=[ FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp', 'gif','txt','pcap','pcapng']) ])
