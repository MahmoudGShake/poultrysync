from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'is_active', 'created_by', 'created_at', 'last_updated_at']
        read_only_fields = ['created_by', 'created_at', 'last_updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['company'] = self.context['request'].user.company
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'status', 'created_by', 'created_at', 'shipped_at']
        read_only_fields = ['created_by', 'created_at', 'shipped_at', 'status']

    def validate(self, data):
        user = self.context['request'].user
        product = data.get('product')
        quantity = data.get('quantity')

        if product is not None and not product.is_active:
            raise serializers.ValidationError("Cannot order inactive product.")
        if quantity is not None and product is not None and product.stock < quantity:
            raise serializers.ValidationError("Not enough stock.")
        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['company'] = self.context['request'].user.company
        return super().create(validated_data)
