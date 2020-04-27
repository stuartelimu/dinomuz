from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import JsonResponse
from django.core import serializers
import requests
import json
from .models import Subscriber
from .forms import SubscriberForm


class IndexView(View):
    form_class = SubscriberForm
    template_name = 'index.html'

    # some variables for sendgrid
    api_key = settings.SENDGRID_API_KEY
    list_id = settings.LIST_ID
    base_url = 'https://api.sendgrid.com/v3'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(api_key)}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})    

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            form = self.form_class(self.request.POST)
            if form.is_valid():
                # get email
                email = form.cleaned_data['email']
                instance = form.save(commit=False)
                data = {
                    "list_ids": [self.list_id],
                    "contacts": [{"email": email}]
                }
                # add email to list
                response = requests.put(f"{self.base_url}/marketing/contacts", headers=self.headers, json=data)
                # check if the response valid
                if response.status_code >= 200:
                    instance.save()
                    ser_instance = serializers.serialize('json', [instance,])
                    return JsonResponse({'instance': ser_instance}, status=200)
                else:
                    return JsonResponse({'error': '[?] Unexpected Error'}, status=response.status_code)
                
            else:
                return JsonResponse({'error': form.errors}, status=400)

        return JsonResponse({"error": "failed"}, status=400)
