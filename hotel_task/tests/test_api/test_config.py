import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestConfigAPI:
    collection_path = '/config/'
    detail_path = '/config/{parameter}/'
    parameter = 'overbooking'

    def test_list(self):
        factory = APIClient()
        response = factory.get(self.collection_path)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert 2 == len(data)

    def test_retrieve(self):
        factory = APIClient()
        response = factory.get(self.detail_path.format(parameter=self.parameter))
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert 'parameter' in data
        assert 'value' in data
        assert data['value'] == '100'

    def test_put(self):
        factory = APIClient()
        data = {
            'parameter': self.parameter,
            'value': '110'
        }
        response = factory.put(self.detail_path.format(parameter=self.parameter), data=data)
        assert response.status_code == 200
        response = factory.get(self.detail_path.format(parameter=self.parameter))
        assert response.status_code == 200
        assert isinstance(data, dict)
        assert 'parameter' in data
        assert 'value' in data
        assert data['value'] == '110'
