from django.conf import settings
from django.db import models
from documents.utils import validate_file_size


# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=160)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    document = models.FileField(upload_to='documents', validators=[validate_file_size])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title