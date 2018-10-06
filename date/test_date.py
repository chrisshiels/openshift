import json


import pytest


import date


@pytest.fixture
def app():
  return date.app


def test_date(client):
  response = client.get('/date')
  assert response.status_code == 200
  data = json.loads(response.data)
  assert isinstance(data['year'], int)
  assert isinstance(data['month'], int)
  assert isinstance(data['day'], int)
