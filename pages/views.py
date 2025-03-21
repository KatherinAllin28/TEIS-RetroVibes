from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class OptionsView(TemplateView):
    template_name = 'vinyl/index.html'