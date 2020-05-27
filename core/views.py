from django.contrib import messages
from os.path import exists
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from core.models import Item

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
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView,View, FormView, View
from requests.api import request

from django.core.files.storage import FileSystemStorage

from . import forms
from .forms import CheckOutForm
from .models import Item, Order, OrderItem, BillingAddress, Category

# from scipy.constants.constants import slug

def index_view(request):
    return render(request, 'index.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


def cookie_policy(request):
    return render(request, 'cookie_policy.html')


def disclaimer(request):
    return render(request, 'disclaimer.html')


def return_policy(request):
    return render(request, 'returns.html')


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
    
    context = {}

    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)
    
    context_var = {

        "items": queryset,
    }

    return render(request, 'store/order_item_list.html', context_var)


class OrderCheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context_var = {
            'form': form
        }
        return render(self.request, 'store/checkout.html', context_var)
    
    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        
            if form.is_valid():
                # Create new instance of the form
                shipping_address_line_1 = form.cleaned_data.get(shipping_address_line_1)
                shipping_address_line_2 = form.cleaned_data.get(shipping_address_line_2)
                state = form.cleaned_data.get(state)
                phone_number = form.cleaned_data.get(phone_number)
                zip_code = form.cleaned_data.get(zip_code)
                same_as_shipping_address = form.cleaned_data.get(same_as_shipping_address)
                save_info = form.cleaned_data.get(save_info)

                billing_address = BillingAddress(
                    user = self.request.user,
                    shipping_address_line_1 = shipping_address_line_1,
                    shipping_address_line_2 = shipping_address_line_2,
                    state = state,
                    phone_number = phone_number,
                    zip_code = zip_code,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                return redirect('proceed_to_pay')
            return redirect('proceed_to_pay')    
            #return render(self.request, 'store/order_summary.html')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You don\'t seem to have any active order')
            return redirect('order_summary') 


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
            return redirect('order_summary')
            
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


def get_item_queryset(query=None):
    queryset = []
    queries = query.split(" ") 
    
    for q in queries:
        search_items = Item.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(category__icontains=q)
        ).distinct()  # Disallow duplicate items

        for item in search_items:
            queryset.append(item)

    return list(set(queryset))


def item_category_view(request, category_slug):
    categories = Category.objects.all()
    item = Item.objects.filter(title='title')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        item = item.filter(category=category)
    template_name = 'cats/item_category.html'
    context = {
            'categories': categories, 'item': item, 'category': category
        }
    return render(request, template_name, context)


def cat_detail_view(request, category_slug):
    template_name = 'cats/cat_detail.html'
    category = get_object_or_404(Category, category_slug=category_slug)
    item = Item.objects.filter(category=category)
    context = {
            'category': category, 'item': item,
        }
    return render(request, template_name, context)