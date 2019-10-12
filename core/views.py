from django.contrib import messages
from os.path import exists
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Context, Template, loader
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView,View
from requests.api import request

from purchase.views import OrderPaymentView

from . import forms
from .models import Item, Order, OrderItem

# from scipy.constants.constants import slug



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

        subject = 'Contact Email Received from a Visitor'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = ['from_email']
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


def order_item_list(request):
    queryset = Item.objects.all()
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        ).distinct()  # Disallow duplicate items

    context = {

        "items": queryset,
    }

    return render(request, 'store/order_item_list.html', context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'item': order
            }
             
            return render(self.request, 'store/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You don\'t seem to have any active order')
            return redirect('/')


def product(request, slug):
    item = get_object_or_404(Item, slug=slug)

    return render(request, 'products_list/product_detail.html', {'item': item })


# Add_to-cart view
@login_required(login_url='/accounts/login/')
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
         user=request.user, ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Find out if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity was updated!")
            return redirect('marketplace')
            
        else:
            messages.info(request, "Item was added to your cart")
            order.items.add(order_item)   
            return redirect('marketplace')
    else: 
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your cart")
        return redirect('order_summary')


# Remove from cart View 
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # Find out if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item) 
            messages.info(request, "This item was removed from your cart") 
            return redirect('order_summary')          
        else:
            messages.info(request, "This item was not in your cart") 
            return redirect('product_detail', slug=slug)         
    else: 
        messages.info(request, "You do not have any active order") 
        return redirect('product_detail', slug=slug)


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # Find out if the order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated") 
            return redirect('order_summary')          
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('order_summary', slug=slug)         
    else: 
        messages.info(request, "You do not have any active order") 
        return redirect('order_summary', slug=slug)