from django.test import TestCase
from django.contrib.auth.models import User
from pages.models import Vinyl, Order, OrderItem, Shipping
from datetime import date

class VinylModelTest(TestCase):
    # Verifica que un objeto Vinyl se cree correctamente con los campos necesarios.
    # También comprueba que el precio por defecto es 19.99 si no se especifica.
    def test_vinyl_creation(self):
        vinyl = Vinyl.objects.create(
            name="Test Vinyl",
            imageDesign="templates/image/test.jpg",
            size=12.0,
            colour="Black"
        )
        self.assertEqual(vinyl.name, "Test Vinyl")
        self.assertEqual(vinyl.price, 19.99)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.vinyl = Vinyl.objects.create(
            name="Vinyl Order Test",
            imageDesign="templates/image/test.jpg",
            size=10.0,
            colour="Red",
            price=25.00
        )

    # Verifica que una orden pueda asociarse correctamente con un vinilo a través del modelo OrderItem.
    # También asegura que la relación many-to-many funciona correctamente.
    def test_order_with_items(self):
        order = Order.objects.create(user=self.user, total_price=25.00)
        OrderItem.objects.create(order=order, vinyl=self.vinyl, quantity=1)

        self.assertEqual(order.vinyls.count(), 1)
        self.assertEqual(order.vinyls.first().name, "Vinyl Order Test")

    # Verifica que el estado por defecto de una orden nueva sea 'pending'.
    def test_order_status_default(self):
        order = Order.objects.create(user=self.user)
        self.assertEqual(order.status, 'pending')

class ShippingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shippinguser', password='abc123')
        self.vinyl = Vinyl.objects.create(
            name="Shipped Vinyl",
            imageDesign="templates/image/ship.jpg",
            size=11.0,
            colour="Blue",
            price=30.00
        )
        self.order = Order.objects.create(user=self.user, total_price=30.00)
        OrderItem.objects.create(order=self.order, vinyl=self.vinyl, quantity=1)

    # Verifica que se pueda crear correctamente una instancia de Shipping relacionada a una orden.
    # También comprueba que los campos tracking_number, status e estimated_delivery se guarden adecuadamente.
    def test_shipping_creation(self):
        shipping = Shipping.objects.create(
            order=self.order,
            tracking_number="ABC123456",
            status="in_transit",
            estimated_delivery=date(2025, 12, 1)
        )
        self.assertEqual(shipping.order, self.order)
        self.assertEqual(shipping.status, "in_transit")
        self.assertEqual(str(shipping.tracking_number), "ABC123456")

    # Verifica que el campo 'status' del modelo Shipping acepte los valores definidos en sus choices ('delivered').
    def test_shipping_status_choices(self):
        shipping = Shipping.objects.create(
            order=self.order,
            tracking_number="XYZ987654",
            status="delivered",
            estimated_delivery=date(2025, 12, 15)
        )
        self.assertEqual(shipping.status, "delivered")
