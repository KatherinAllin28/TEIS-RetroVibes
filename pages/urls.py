from django.urls import path
from .views import HomePageView, OptionsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('options/', OptionsView.as_view(), name='index')
]