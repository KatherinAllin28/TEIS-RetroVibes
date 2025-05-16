from rest_framework import serializers
from .models import Vinyl

class VinylSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Vinyl
        fields = ['id', 'name', 'price', 'colour', 'size', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        # Construye un link al detalle del producto (modifica según tu URL)
        return request.build_absolute_uri(f'/vinyl/{obj.id}/')
