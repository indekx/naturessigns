from django.shortcuts import render
from django.views.generic import ListView
from core.models import Item

class SearchItemView(ListView):
    template_name = 'search/search_results.html'
    model = Item

    def get_context_data(self, *args, **kwargs):
        context = super(SearchItemView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        meth_dict = request.GET
        query = meth_dict.get('q', None)
        
        if query is not None:
            return Item.objects.search(query)
        return Item.objects.featured()