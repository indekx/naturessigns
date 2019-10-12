from django import template
from core.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs_ = Order.objects.filter(user=user, ordered=False)
        if qs_.exists():
            return qs_[0].items.count()
    else:
        return 0