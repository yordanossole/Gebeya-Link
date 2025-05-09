from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_killo = models.DecimalField(max_digits=6, decimal_places=2)
    inventory_killo = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category') # foreign_key to category_id

class Address(models.Model):
    REGION_CHOICES = [
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
    ]
    CITY_CHOICES = [
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
        ('Addis Ababa', 'Addis Ababa'),
    ]
    ZONE_CHOICES = [
        ('Arada', 'Arada'),
        ('Arada', 'Arada'),
        ('Arada', 'Arada'),
        ('Arada', 'Arada'),
        ('Arada', 'Arada'),
        ('Arada', 'Arada'),
        ('Arada', 'Arada'),
        ('Arada', 'Arada'),
        ('Arada', 'Arada'),
    ]
    WOREDA_CHOICES = [
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
    ]
    KEBELE_CHOICES = [
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
        ('01', '01'),
    ]
    STREET_CHOICES = [
        ('Street Name', 'Street Name'),
        ('Street Name', 'Street Name'),
        ('Street Name', 'Street Name'),
        ('Street Name', 'Street Name'),
        ('Street Name', 'Street Name'),
        ('Street Name', 'Street Name'),
        ('Street Name', 'Street Name'),
    ]

    region = models.CharField(max_length=255, choices=REGION_CHOICES)
    city = models.CharField(max_length=255, choices=CITY_CHOICES)
    zone = models.CharField(max_length=255, choices=ZONE_CHOICES)
    woreda = models.CharField(max_length=255, choices=WOREDA_CHOICES)
    kebele = models.CharField(max_length=255, choices=KEBELE_CHOICES)
    street = models.CharField(max_length=255, choices=STREET_CHOICES)
    house_number = models.CharField(max_length=10)

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    address = models.OneToOneField(Address, on_delete=models.PROTECT, related_name='address')

class Image(models.Model):
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    image = models.ImageField(upload_to="product_images/")
    download_url = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="image")

class Comment(models.Model):
    content = models.TextField()
    rating = models.SmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='customer') # foreign_key to product_it
    customer = models.ForeignKey(Customer, on_delete=models.SET_DEFAULT, default=0, related_name='customer') # foreign_key to customer_id


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),

    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer') # foreign_key to customer_id

class OrderItem(models.Model):
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_killo = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.PROTECT) # foreign_key to order_id
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # foreign_key to product_it

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE) # foreign_key to customer_id

class CartItem(models.Model):
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_killo = models.DecimalField(max_digits=6, decimal_places=2)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) # foreign_key to cart_id
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # foreign_key to product_id