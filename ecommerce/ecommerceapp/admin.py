import django.apps
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path

from ecommerceapp import dao
from ecommerceapp.models import User

class CustomAdminSite(AdminSite):
    def get_urls(self):
        return [
                   path('stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        if request.method == 'GET':
            stats = dao.stat_products(request.GET.get('select-type'), request.GET.get('select-value'))
            print(stats)
            return TemplateResponse(request, 'admin/stats.html', {
                'stats': stats
            })
        else:
            return TemplateResponse(request, 'admin/stats.html')



custom_admin_site = CustomAdminSite(name='customadmin')
models = django.apps.apps.get_models()
for model in models:
    try:
        custom_admin_site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

