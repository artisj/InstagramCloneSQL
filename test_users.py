import pytest
from fastapi.testclient import TestClient
from main import app

token = ''
id = ''

client = TestClient(app)

def set_token(new_token):
  global token 
  token = new_token

def test_home():
  response = client.get('/')
  assert response.status_code == 200
  assert response.json() == 'Home'
  
def test_create_duplicate_user():
  response = client.post('/signup', json={'email':'aa@test.com', 'password': 'abc123'})
  assert response.status_code == 400
  assert response.json() == {'detail': 'User with this email already exist'}

def test_login_user():
  response = client.post('/login', data={'username':'aa@test.com', 'password': 'abc123'})
  assert response.status_code == 200
  set_token(response.json()['access_token'])
  
def test_get_me():
  global id
  response = client.get('/users/me/', headers={'Authorization': f'Bearer {token}'})
  id = response.json()
  assert response.status_code == 200
  

