from rest_framework import serializers
from Mesero.models import Pedidos

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'  # Puedes especificar los campos que necesitas si no quieres todos

