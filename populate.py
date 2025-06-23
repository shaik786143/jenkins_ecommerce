import os
import django
import random
from faker import Faker
from datetime import date
import sys

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_ecommerce.settings")
django.setup()

from testapp.models import Product, Sale
from reporting.models import DailySaleSummary

def populate_data(product_count=50, sale_count=200):
    """
    Populates the database with dummy data for Products and Sales.
    """
    fake = Faker()

    print("Clearing existing data...")
    Sale.objects.all().delete()
    Product.objects.all().delete()
    DailySaleSummary.objects.all().delete()

    products = []
    print(f"Creating {product_count} products...")
    for _ in range(product_count):
        product = Product.objects.create(
            name=fake.bs().title(),
            description=fake.paragraph(nb_sentences=3),
            price=round(random.uniform(10.0, 500.0), 2),
            inventory=random.randint(10, 100),
        )
        products.append(product)
    print("Products created successfully.")

    print(f"Creating {sale_count} sales...")
    for _ in range(sale_count):
        # Pick a random product for the sale
        product = random.choice(products)
        
        # Ensure quantity sold does not exceed available inventory
        if product.inventory > 0:
            quantity = random.randint(1, min(5, product.inventory))
            
            Sale.objects.create(
                product=product,
                quantity_sold=quantity
            )
            
            # Decrease the product inventory (optional, but good practice)
            product.inventory -= quantity
            product.save()

    print("Sales created successfully.")

    print("Aggregating sales data and creating daily summaries...")
    summaries = {}
    for sale in Sale.objects.all():
        sale_date = sale.sale_date.date()
        if sale_date not in summaries:
            summaries[sale_date] = {"total_revenue": 0, "products_sold_count": 0}
        
        summaries[sale_date]["total_revenue"] += sale.total_price
        summaries[sale_date]["products_sold_count"] += sale.quantity_sold

    for summary_date, data in summaries.items():
        DailySaleSummary.objects.create(
            summary_date=summary_date,
            total_revenue=data["total_revenue"],
            products_sold_count=data["products_sold_count"],
        )
    print("Daily summaries created successfully.")
    
    print("\nDatabase population complete!")

if __name__ == "__main__":
    # Allow command-line arguments for product and sale counts
    product_count = 50
    sale_count = 200
    if len(sys.argv) > 1:
        try:
            product_count = int(sys.argv[1])
        except ValueError:
            print("Invalid product count, using default (50).")
    if len(sys.argv) > 2:
        try:
            sale_count = int(sys.argv[2])
        except ValueError:
            print("Invalid sale count, using default (200).")
    populate_data(product_count, sale_count) 