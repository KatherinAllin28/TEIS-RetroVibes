from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Vinyl, Order, OrderItem, Shipping
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import uuid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import RegisterForm
from django.http import FileResponse
from .services.pdf_receipt_generator import ReceiptGenerator
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VinylSerializer
import requests
from django.contrib import messages

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class OptionsView(TemplateView):
    template_name = 'vinyl/index.html'

class VinylIndexView(TemplateView):
    template_name = 'vinyl/list.html'  # Asegúrate de que este template existe

    def get(self, request):
        vinyls = Vinyl.objects.all()
        context = {"vinyls": vinyls}
        return render(request, self.template_name, context)
    
     
class VinylShowView(TemplateView): 
    template_name = 'vinyl/show.html' 
    
    def get(self, request, id):  
        vinyl = get_object_or_404(Vinyl, pk=id)  # Esto ya maneja errores automáticamente
        return render(request, self.template_name, {"vinyl": vinyl})

class CartView(View):
    template_name = "cart/index.html"

    def get(self, request):
        # Obtener todos los productos desde la base de datos
        vinyls = {vinyl.id: {'name': vinyl.name, 'price': vinyl.price} for vinyl in Vinyl.objects.all()}

        cart_vinyls = {}
        cart_product_data = request.session.get('cart_vinyl_data', {})

        # Filtrar solo los productos que están en el carrito
        for key in cart_product_data.keys():
            if int(key) in vinyls:  
                cart_vinyls[key] = vinyls[int(key)]  # Convertimos a int para evitar problemas

        view_data = {
            'vinyls': vinyls,
            'cart_vinyls': cart_vinyls
        }

        return render(request, self.template_name, view_data)

    def post(self, request, vinyl_id):
        # Verificar si el producto existe en la base de datos
        vinyl = get_object_or_404(Vinyl, id=vinyl_id)

        cart_vinyl_data = request.session.get('cart_vinyl_data', {})
        cart_vinyl_data[str(vinyl.id)] = vinyl.id  # Asegurar que la clave es string
        request.session['cart_vinyl_data'] = cart_vinyl_data
        messages.success(request, "Tu producto ha sido agregado a tu carrito exitosamente 😉")
        return redirect('cart_index')

class CartRemoveAllView(View):
    def post(self, request):
        if 'cart_vinyl_data' in request.session:
            del request.session['cart_vinyl_data']
        
        return redirect('cart_index')
    
class VinylForm(forms.ModelForm):
    class Meta:
        model = Vinyl
        fields = ['name', 'size', 'colour']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError("The price must be greater than zero.")
        return price

class VinylCreateView(View):
    template_name = 'vinyl/create.html'

    def get(self, request):
        form = VinylForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = VinylForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect("/cart/")  

        return render(request, self.template_name, {"form": form})
    
@method_decorator(login_required, name='dispatch')
class OrderView(LoginRequiredMixin, TemplateView):
    template_name = "order/index.html"
    login_url = "/accounts/login/"  # Redirección si no está autenticado
#class OrderView(View, LoginRequiredMixin, TemplateView):

    def get(self, request):
        cart_vinyl_data = request.session.get('cart_vinyl_data', {})
        vinyls = Vinyl.objects.filter(id__in=cart_vinyl_data.keys())

        total_price = sum(vinyl.price for vinyl in vinyls)

        context = {
            'vinyls': vinyls,
            'total_price': total_price
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirige a la página de login si no está autenticado
        cart_vinyl_data = request.session.get('cart_vinyl_data', {})

        if not cart_vinyl_data:
            return redirect('cart_index')

        order = Order.objects.create(user=request.user, total_price=0)
        # ... lógica para agregar vinilos al pedido

        total_price = 0
        for vinyl_id, quantity in cart_vinyl_data.items():
            vinyl = Vinyl.objects.get(id=vinyl_id)
            OrderItem.objects.create(order=order, vinyl=vinyl, quantity=quantity)
            total_price += vinyl.price * quantity

        order.total_price = total_price
        order.save()

        # Limpiar carrito después de la compra
        del request.session['cart_vinyl_data']

        return redirect('shipping', order_id=order.id)

@login_required(login_url="/accounts/login/")
def order_view(request):
    return render(request, "order/index.html")
   
@method_decorator(login_required, name='dispatch')
class ShippingView(View):
    template_name = "shipping/index.html"

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        shipping, created = Shipping.objects.get_or_create(
            order=order,
            defaults={
                'tracking_number': str(uuid.uuid4()),
                'estimated_delivery': timezone.now().date() + timedelta(days=7)
            }
        )

        items = order.orderitem_set.select_related('vinyl')
        total_price = order.total_price

        context = {
            'order': order,
            'shipping': shipping,
            'items': items,
            'total_price': total_price,
        }
        return render(request, self.template_name, context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, "Creación de usuario exitosa ✅")
            return redirect("profile") 
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def download_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    shipping = get_object_or_404(Shipping, order=order)

    context = {
        "order": order,
        "shipping": shipping,
    }

    generator = ReceiptGenerator() 
    pdf_file = generator.generate(context)

    return FileResponse(pdf_file, as_attachment=True, filename=f"recibo_{order.id}.pdf")

class VinylListAPIView(APIView):
    def get(self, request):
        vinyls = Vinyl.objects.all()
        serializer = VinylSerializer(vinyls, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def productos_aliados(request):
    
    response = requests.get('http://localhost:8000/api/vinyls/') #<---------- link aqui
    
    if response.status_code == 200:
        productos = response.json()  
    else:
        productos = []  

    context = {
        'productos': productos
    }
    return render(request, 'JSON/productos_aliados.html', context)
