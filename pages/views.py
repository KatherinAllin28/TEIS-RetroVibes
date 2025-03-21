from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Vinyl



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

        return redirect('cart_index')

class CartRemoveAllView(View):
    def post(self, request):
        if 'cart_vinyl_data' in request.session:
            del request.session['cart_vinyl_data']
        
        return redirect('cart_index')
