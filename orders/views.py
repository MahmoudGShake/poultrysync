from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from django.http import HttpResponse
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from .permissions import *
from django.utils.timezone import localtime
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

import csv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/orders.log', level=logging.INFO)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsNotViewer]

    def get_queryset(self):
        return Product.objects.filter(company=self.request.user.company, is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsNotViewer, CanEditOrderToday]

    def get_queryset(self):
        return Order.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        order = serializer.save()
        if order.status == "success":
            logger.info(
                f"📦 Order #{order.id} confirmed for {order.created_by.email} | Qty: {order.quantity} | Product: {order.product.name} | Company: {order.company.name}"
            )


@api_view(["GET"])
@permission_classes([IsAdminOrOperator])
def export_orders_csv(request):
    user = request.user
    orders = Order.objects.filter(company=user.company)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Product', 'Quantity', 'Status', 'Created By', 'Created At', 'Shipped At'])

    for order in orders:
        writer.writerow([
            order.id,
            order.product.name,
            order.quantity,
            order.status,
            order.created_by.username,
            localtime(order.created_at).strftime('%Y-%m-%d %H:%M:%S'),
            localtime(order.shipped_at).strftime('%Y-%m-%d %H:%M:%S') if order.shipped_at else ''
        ])

    return response


@login_required
def index(request):
    user = request.user

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.company = user.company
            product.created_by = user
            product.save()
            return redirect('index')
    else:
        form = ProductForm()

    products = Product.objects.filter(company=user.company).order_by('-created_at')
    return render(request, 'orders/index.html', {'form': form, 'products': products})