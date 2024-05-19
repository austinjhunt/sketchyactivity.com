# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.core.cache import cache
from ..models import PortfolioItem
from .util import *
from .s3 import s3_client

class PortfolioItemEdit(UpdateView):
    model = PortfolioItem
    template_name = 'super/portfolio_item_edit.html'
    fields = ['tag', 'portrait_name', 'date']
    success_url = '/'



class PortfolioItemDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PortfolioItem
    template_name = 'super/portfolio_item_delete.html'
    success_url = '/'

    def test_func(self):
        return self.request.user.is_superuser


class PortfolioManage(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'super/manage_portfolio.html'

    def get(self, request):
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'portfolio': PortfolioItem.objects.all().order_by('-date')
            }
        )

    def test_func(self):
        return self.request.user.is_superuser

