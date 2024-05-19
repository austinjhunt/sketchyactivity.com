
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers import *
from rest_framework.response import Response
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.core.cache import cache
from ..models import PortfolioItem
from .util import *
from .s3 import s3_client

class MetaStuffView(viewsets.ModelViewSet):
    serializer_class = MetaStuffSerializer
    queryset = MetaStuff.objects.all()
    permission_classes = [IsAdminUser]



class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['bio'] = get_bio()
        ms = MetaStuff.objects.first()
        update_private_url_profile_image(ms, s3_client=s3_client)
        data['profile_image'] = ms.profile_image_private_url
        return data
