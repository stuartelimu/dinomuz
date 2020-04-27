from django.shortcuts import render
from django.views import View

from .models import Subscriber
from .forms import SubscriberForm


class IndexView(View):
    form_class = SubscriberForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})     
