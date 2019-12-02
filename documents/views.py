from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView, 
    DeleteView
)

from .forms import FileUploadForm
from .models import Document

from .utils import validate_file_size
# Create your views here.
@login_required(login_url='/accounts/login/')
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/documents/whitepapers/')

    else:
        form = FileUploadForm()
    
    return render (request, 'documents/file_upload.html', {
        'form': form
    })


class DocumentListView(ListView):
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    ordering = ['-timestamp']
    paginate_by = 10