from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect

from django.shortcuts import redirect, render, get_object_or_404 
from django.template import Context, Template, loader
from django.template.loader import get_template

from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from requests.api import request

from . import forms
from .models import Item, Order, OrderItem


def index(request):
    return render(request, 'homepage.html')

def about_us(request):
    return render(request, 'about_us.html')

# @login_required(login_url='/accounts/login/')
def email_subscribe(request):
    post_data = request.POST.copy()
    email = post_data.get('email', None)
    error_msg = validation_util.validate_email(email)
    
    if error_msg:
        messages.error(request, error_msg)
        return HttpResponseRedirect(reverse('appname:baseapp'))

    return redirect('/index/', 'subscribe.html')

def our_services(request):
    return render(request, 'our_services.html')

def how_we_do_it(request):
    return render(request, 'how_we_do_it.html')

def drugs(request):
    return render(request, 'dispensary/drugs.html')

def store(request):
    queryset = Item.objects.all()  # .order_by('-timestamp')
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        ).distinct()  # Disallow duplicate items

    context = {

        "products": queryset,
    }

    return render(request, 'products_list/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Item, slug=slug)

    return render(request, 'products_list/product_detail.html', {'product': product})


 # View for Prostaright Tea   
def product_prostaright(request):
    return render(request, 'products_list/prostaright_tea.html')




# Create your views here.
@login_required(login_url='/accounts/login/')
def add_product(request):
    if request.method == 'POST':
        form = forms.AddProduct(request.POST, request.FILES,)
        if form.is_valid():

            # Save data to Products
            form_instance_create = form.save(commit=False)
            form_instance_create.user = request.user
            form_instance_create.save()
            return redirect('store') 
    else:
        form = forms.AddProduct()
    return render(request, 'products_list/add_product.html', {'form': form})


#Contact us view
def contact_us(request):
    form = forms.ContactUsForm(request.POST or None)
    if form.is_valid():
        form_first_name = form.cleaned_data.get('first_name')
        form_last_name = form.cleaned_data.get('last_name')
        form_contact_email = form.cleaned_data.get('contact_email')
        form_message = form.cleaned_data.get('message')
        form_full_name = form_first_name + ' ' + form_last_name

        subject = 'Site contact mail'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = ''' 
        %s: %s via %s 
        '''%(form_full_name,
            form_message,
            form_contact_email     
        )

        send_mail(
            subject, contact_message, from_email,
            to_email, fail_silently=False
        )

        return redirect('index')
    
    return render(request, 'contact_us.html', {'form': form})
