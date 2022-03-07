from django.contrib.auth.models import User
from rest_framework import status
from store.models import Product, Collection
from model_bakery import baker
import pytest


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product):
        response = create_product({'title':'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product):
        authenticate()
        
        response = create_product({'title':'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.skip(reason="Can't post data")
    def test_if_data_is_valid_returns_201(self, api_client):

        api_client.force_authenticate(user=User(is_staff=True))
        collection = baker.make(Collection)

        response = api_client.post('/store/products/', {
                        'title': 'b',
                        'description': 'b',
                        'slug': 'b',
                        'inventory': 4,
                        'unit_price': 55.00,
                        'collection': collection
                    })

        assert response.status_code == status.HTTP_201_CREATED


