from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model with Roles
class User(AbstractUser):
    ADMIN = 'admin'
    RENTER = 'renter'
    BORROWER = 'borrower'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (RENTER, 'Renter'),
        (BORROWER, 'Borrower'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BORROWER)

    def is_admin(self):
        return self.role == self.ADMIN
    
    def is_renter(self):
        return self.role == self.RENTER
    
    def is_borrower(self):
        return self.role == self.BORROWER

# Clothing Items listed by Renters
class Cloth(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'renter'})
    name = models.CharField(max_length=255)
    description = models.TextField()
    size = models.CharField(max_length=10)  # Example: S, M, L, XL
    condition = models.CharField(max_length=50, choices=[('New', 'New'), ('Good', 'Good'), ('Worn', 'Worn')])
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='clothes_images/', blank=True, null=True)
    available_from = models.DateField()
    available_until = models.DateField()
    is_approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return self.name

# Rental Requests
class Rental(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    RETURNED = 'Returned'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (RETURNED, 'Returned'),
    ]
    
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'borrower'})
    rental_start = models.DateField()
    rental_end = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.borrower.username} renting {self.cloth.name}"

# Payment Transactions
class Transaction(models.Model):
    SUCCESS = 'Success'
    FAILED = 'Failed'
    PENDING = 'Pending'
    
    STATUS_CHOICES = [
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (PENDING, 'Pending'),
    ]
    
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Transaction for {self.rental.cloth.name} - {self.status}"

# Admin Approval Queue (For approving clothes before they go live)
class ApprovalQueue(models.Model):
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Approval Status for {self.cloth.name}"

