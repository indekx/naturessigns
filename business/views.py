import json
import urllib

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from urllib3 import request

from business.models import Advert

from . import forms
from .forms import DistributorApplication
from .models import Advert, BecomeAnAffiliate


# Create your views here.
class AdCreateView(LoginRequiredMixin, CreateView):
    model = Advert
    template_name = 'business/ad_create.html'
    fields = [
        'label', 'image', 'price', 
        'discount_price', 'description', 
        'category', 'detail', 'slug'
    ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AdvertListView(ListView):
    model = Advert
    template_name = 'business/all_products.html'
    context_object_name = 'adverts'
    ordering = ['-date_added']
    paginate_by = 5


def become_an_affiliate(request):
    if request.method == 'POST':
        form = forms.BecomeAnAffiliate(request.POST)
        if form.is_valid():

            ''' reCAPTCHA Validation Begins '''
            ClientKey = request.POST['g-recaptcha-response']
            SecretKey = 'settings.GOOGLE_RECAPTCHA_SECRET_KEY'
            
            CaptchaData = {
                'secret': SecretKey,
                'response': ClientKey,
            }

            result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=CaptchaData)
            response = json.loads(result.text)
            verify = response['success']
            print('Your success is', verify)

            ''' reCAPTCHA Validation Ends '''
            
        return redirect('index')
    else:
        form = forms.BecomeAnAffiliate()

    return render(request, 'business/affiliate_program.html',  {'form': form})


# Distributor View 
@login_required(login_url='/accounts/login/')
def become_distributor(request):
    if request.method == 'POST':
        form = forms.DistributorApplication(request.POST)
        if form.is_valid():
            ''' reCAPTCHA Validation Begins '''
            recaptcha_response = response.POST.get('g-recaptcha-response')
            values = {
                'secret_key': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' reCAPTCHA Validation Ends '''

            if result['success']:
                # Save data
                form.save()
                messages.success(request, 'Application as distributor was successfully!')   
            else:
                messages.error(request, 'reCaptcha validation failed, please retry.')
            
            return redirect('business/new_distributor')
    else:
        form = forms.DistributorApplication()

    return render(request, 'business/become_distributor.html',  {'form': form})
