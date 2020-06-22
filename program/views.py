from django.shortcuts import render, redirect
from .forms import PartnerJoinForm, SellApplyForm
from .models import PartnerJoin, SellApply

from django.contrib.auth.decorators import login_required

# Create your views here.


def partner_program_view(request):
    return render(request, 'programs/join_partner.html')


def partner_reg_success(request):
    return render(request, 'programs/partner_reg_success.html')


def partner_interest_view(request):
    if request.method == 'POST':
        form = PartnerJoinForm(request.POST or None)  # Initialize the form
        if form.is_valid():
            form_instance_create = form.save(commit=False)
            form_instance_create.save()
            return redirect('partner_register_success')
    else:
        form = PartnerJoinForm
    return render(request, 'programs/partner_form.html', {'form': form})


def sell_apply_success(request):
    return render(request, 'programs/sell_apply_success.html')


#@login_required(login_url='/accounts/login/')
def sell_apply_view(request):
    if request.method == 'POST':
        form = SellApplyForm(request.POST, request.FILES)  # Initialize the form
        if form.is_valid():
            sell_form_instance_create = form.save(commit=False)
            sell_form_instance_create.save()
            return redirect('sell_apply_success')
    else:
        form = SellApplyForm
    return render(request, 'programs/sell_apply.html', {'form': form})
