import factory

from .models import Vinyl

class VinylFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vinyl
    name = factory.Faker('sentence', nb_words=3)
    price = factory.Faker('random_int', min = 200, max = 9000)
    colour = factory.Faker('color_name')
    size = factory.Faker('pyfloat', left_digits=2, right_digits=1, positive=True)