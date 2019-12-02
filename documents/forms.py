from django import forms
from .models import Document
from .utils import validate_file_size

# MAX_UPLOAD_SIZE = "5242880"
class FileUploadForm(forms.ModelForm):
    title = forms.CharField()
    document = forms.FileField(validators=[validate_file_size])
    
    class Meta:
        model = Document
        fields = ['title', 'document']