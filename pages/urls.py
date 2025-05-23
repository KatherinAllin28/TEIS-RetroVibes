from django.urls import path, include
from .views import HomePageView, OptionsView, VinylIndexView, VinylShowView, CartView, CartRemoveAllView, VinylCreateView, VinylForm, OrderView, ShippingView, register,  VinylListAPIView, productos_aliados
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('options/', OptionsView.as_view(), name='index'),
    path('vinyls/', VinylIndexView.as_view(), name="vinyl_list"),
    path('vinyls/<str:id>', VinylShowView.as_view(), name='show'),
    path('cart/', CartView.as_view(), name='cart_index'),
    path('cart/add/<int:vinyl_id>', CartView.as_view(), name='cart_add'),
    path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
    path('vinyls/create/', VinylCreateView.as_view(), name='vinyl_create'),  # URL para crear un vinilo
    path('order/', OrderView.as_view(), name='order'),
    path('shipping/<int:order_id>/', ShippingView.as_view(), name='shipping'),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path('perfil/', views.profile_view, name='profile'),
    path("recibo/<int:order_id>/", views.download_receipt, name="download_receipt"),
    path('api/vinyls/', VinylListAPIView.as_view(), name='api_vinyl_list'),
    path('productos-aliados/', productos_aliados, name='productos_aliados'),
    path('i18n/', include('django.conf.urls.i18n'))

]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)