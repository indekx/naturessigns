from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckOutForm

from .models import BillingAddress
from core.models import Order, OrderItem, Item


# Checkout view
class OrderPaymentView(View):
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