from http.client import responses
from zoneinfo import available_timezones

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from admin_app.models import Cloth, Rental, Transaction

User = get_user_model()

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username="testuser", password="testpassword", role="admin")
    return user

def get_cloths(db):
    cloths = Cloth.objects.all()
    return cloths

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_tokens(create_user):
    refresh = RefreshToken.for_user(create_user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}

@pytest.fixture
def authenticated_client(api_client, create_user):
    """Fixture to return an authenticated client"""
    refresh = RefreshToken.for_user(create_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

def test_get_cloths_authenticated(authenticated_client):
    """Test GET request to /api/admin/cloths/ with authentication"""
    response = authenticated_client.get('/api/admin/cloths/')
    assert response.status_code == 200  # Check if request is successful

def check_cloths_approve(authenticated_client):
    """Test POST request to /api/admin/cloths/{id}/approve/ with authentication"""
    response = authenticated_client.post('/api/admin/cloths/1/approve/')
    assert  response.status_code == 200 # Check if request is successful

@pytest.fixture
def create_cloth(db, create_user):
    """Create a sample cloth owned by the admin user."""
    return Cloth.objects.create(
        owner=create_user,
        name="Winter Jacket",
        description="A warm jacket",
        size="M",
        available_from="2025-04-05",
        available_until="2025-04-26",
        condition="Good",
        price_per_day=10.0,
        is_approved=False
    )
def test_user_as_renter(create_user):
    """Test if a user with the 'renter' role is correctly identified."""
    user = User.objects.create_user(username='testuser1',password='testpassword', role=User.RENTER)

    assert user.is_renter() is True
    assert user.is_admin() is False
    assert user.is_borrower() is False
    assert user.role == User.RENTER


@pytest.mark.django_db
def test_approve_cloth(authenticated_client, create_cloth):
    """Test that an admin can approve a cloth listing."""
    url = f"/api/admin/cloths/{create_cloth.id}/approve/"
    response = authenticated_client.post(url)
    create_cloth.refresh_from_db()

    assert response.status_code == 200
    assert create_cloth.is_approved is True
    assert "approved by admin" in response.data["message"]

@pytest.mark.django_db
def test_reject_cloth(authenticated_client, create_cloth):
    """Test that an admin can reject a cloth listing"""
    url = f"/api/admin/cloths/{create_cloth.id}/reject/"
    response = authenticated_client.post(url)
    create_cloth.refresh_from_db()

    assert response.status_code == 200
    assert create_cloth.is_approved is False
    assert "rejected by admin" in response.data["message"]

def test_hold_cloth(authenticated_client, create_cloth):
    """Test that an admin can hold a cloth listing"""
    url = f"/api/admin/cloths/{create_cloth.id}/hold/"
    response = authenticated_client.post(url)
    create_cloth.refresh_from_db()

    assert response.status_code == 200
    assert create_cloth.is_approved is False
    assert  "put on hold by admin" in response.data["message"]

def test_login(api_client, create_user):
    response = api_client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_cloth_response():
    """Test if the __str__ method returns the cloth title correctly."""
    renter = User.objects.create_user(username='testuser2', password='testpassword', role=User.RENTER)

    cloth = Cloth.objects.create(
        owner=renter,
        name="Red jacket",
        description="A stylish red jacket",
        size="M",
        condition="Good",
        price_per_day=500,
        available_from="2025-04-01",
        available_until="2025-04-10",
        is_approved=True
    )
    assert str(cloth) == "Red jacket"
    if str(cloth) is cloth.title:
        print("__str__ method matched")
    else:
        print("__str__ method not matched")


@pytest.mark.django_db
def test_rental_model_response():
    """Test if the __str__ method returns the rental name correctly"""
    renter = User.objects.create_user(username='testuser2', password='testpassword', role=User.RENTER)
    cloth = Cloth.objects.create(
        owner=renter,
        name="black suit",
        description="A stylish black suit",
        size="L",
        condition="Good",
        price_per_day=1000,
        available_from="2025-04-01",
        available_until="2025-04-10",
        is_approved=True
    )

    borrower = User.objects.create_user(username='testuser3', password='testpassword', role=User.BORROWER)
    rental = Rental.objects.create(
        cloth=cloth,
        borrower=borrower,
        rental_start="2025-05-10",
        rental_end="2025-05-15",
        status='Pending',
        total_price=500
    )
    assert str(rental) == f"{borrower.username} renting {cloth.title}"
    print(f"rental model response is : {borrower.username} renting {cloth.title}")

@pytest.mark.django_db
def test_transaction_model_response():
    renter = User.objects.create_user(username='testuser2', password='testpassword', role=User.RENTER)
    cloth = Cloth.objects.create(
        owner=renter,
        name="black suit",
        description="A stylish black suit",
        size="L",
        condition="Good",
        price_per_day=1000,
        available_from="2025-04-01",
        available_until="2025-04-10",
        is_approved=True
    )

    borrower = User.objects.create_user(username='testuser3', password='testpassword', role=User.BORROWER)
    rental = Rental.objects.create(
        cloth=cloth,
        borrower=borrower,
        rental_start="2025-05-10",
        rental_end="2025-05-15",
        status='Pending',
        total_price=1000
    )
    transaction = Transaction.objects.create(
        rental = rental,
        amount = 1000,
        payment_date = "2025-05-10",
        status = "Success"
    )
    assert str(transaction) == f"Transaction for {transaction.rental.cloth.title} - {transaction.status}"
    print(f"Transaction model response: Transaction for {transaction.rental.cloth.title} - {transaction.status}")

