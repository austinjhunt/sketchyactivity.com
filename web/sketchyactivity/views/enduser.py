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


class HomeView(View):
    @csrf_exempt
    def get(self, request, pg=0):
        portfolio = PortfolioItem.objects.order_by(
            '-date').all()[8*pg: 8*pg + 8]
        for p in portfolio:
            if not cache.get(f'updated_private_url_pitem_{p.id}'):
                _, small_url = update_private_url_single(
                    p, s3_client)
                # half the max expiration time of the private urls for the media files in s3.
                cache.set(
                    f'updated_private_url_pitem_{p.id}', small_url, timeout=302400)
        return render(
            request=request,
            template_name='index.html',
            context={
                'title': 'Austin Hunt Portraiture',
                'portfolio': portfolio,
                'pg': pg
            }
        )


class CommissionsView(View):
    def get(self, request):
        ms = MetaStuff.objects.first()
        sale_active = ms.sale_still_active()
        traditional_prices = Price.objects.filter(style='TR')
        traditional_unique_sizes = traditional_prices.order_by(
            'size').distinct().values_list('size', flat=True)
        traditional_unique_sizes = sorted(
            traditional_unique_sizes, key=lambda el: float(el.split('x')[0]))
        traditional_unique_num_subjects = traditional_prices.order_by(
            'num_subjects').distinct().values_list('num_subjects', flat=True)

        digital_prices = Price.objects.filter(style='DI')
        digital_unique_num_subjects = digital_prices.order_by(
            'num_subjects').distinct().values_list('num_subjects', flat=True)

        drawing_choices = []

        for traditional in Price.objects.filter(style='TR'):
            people_person_string = 'people' if traditional.num_subjects > 1 else 'person'
            amount = traditional.amount if not sale_active else ms.get_sale_price(
                original_price=traditional.amount)

            drawing_choices.append({
                'value': f'tr-{traditional.size}-{traditional.num_subjects}',
                'display_name': f'Ballpoint Pen | {traditional.size} | {traditional.num_subjects} {people_person_string} | ${amount}'
            })
        for digital in Price.objects.filter(style='DI'):
            people_person_string = 'people' if digital.num_subjects > 1 else 'person'
            amount = digital.amount if not sale_active else ms.get_sale_price(
                original_price=digital.amount)

            drawing_choices.append({
                'value': f'di-{digital.num_subjects}',
                'display_name': f'Digital | {digital.num_subjects} {people_person_string} | {amount}'
            })
        return render(
            request,
            'commissions.html',
            context={
                'title': 'Austin Hunt Portraiture Commissions',
                'drawing_choices': drawing_choices,
                'traditional_prices': traditional_prices,
                'traditional_unique_sizes':  traditional_unique_sizes,
                'traditional_unique_num_subjects':  traditional_unique_num_subjects,
                'sale':  MetaStuff.objects.all()[0].sale,
                'digital_prices': traditional_prices,
                'digital_unique_num_subjects':  digital_unique_num_subjects,
                'sale':  MetaStuff.objects.all()[0].sale,
                'sale_amount':  MetaStuff.objects.all()[0].sale_amount
            }
        )


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


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['bio'] = get_bio()
        ms = MetaStuff.objects.first()
        update_private_url_profile_image(ms, s3_client=s3_client)
        data['profile_image'] = ms.profile_image_private_url
        return data
