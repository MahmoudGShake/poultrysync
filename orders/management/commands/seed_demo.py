# orders/management/commands/seed_demo.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Company, CustomUser, Product, Order
from django.contrib.auth.hashers import make_password
import random

class Command(BaseCommand):
    help = 'Seed demo data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Order.objects.all().delete()
        Product.objects.all().delete()
        CustomUser.objects.all().delete()
        Company.objects.all().delete()

        # Create a company
        company = Company.objects.create(name='DemoCorp')

        # Create users
        admin = CustomUser.objects.create(
            username='admin',
            email='admin@poultrysync.com',
            company=company,
            role='admin',
            password=make_password('admin123'),
            is_superuser=True,
            is_staff=True
        )

        operator = CustomUser.objects.create(
            username='operator',
            email='operator@poultrysync.com',
            company=company,
            role='operator',
            password=make_password('operator123')
        )

        viewer = CustomUser.objects.create(
            username='viewer',
            email='viewer@poultrysync.com',
            company=company,
            role='viewer',
            password=make_password('viewer123')
        )

        # Create products
        products = []
        for i in range(5):
            p = Product.objects.create(
                name=f"Product {i+1}",
                price=round(random.uniform(10, 100), 2),
                stock=random.randint(5, 20),
                created_by=admin,
                company=company
            )
            products.append(p)

        # Create orders
        for _ in range(3):
            product = random.choice(products)
            qty = random.randint(1, product.stock)
            Order.objects.create(
                product=product,
                quantity=qty,
                status='success',
                created_by=operator,
                company=company,
                shipped_at=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS("✅ Demo data seeded successfully!"))
