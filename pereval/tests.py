from rest_framework.test import RequestsClient

client = RequestsClient()
response = client.get('http://127.0.0.1:8000/api/submit_data')
assert response.status_code == 200

response = client.get('http://127.0.0.1:8000/api/submit_data/sakjhiasd')
assert response.status_code == 404

response = client.get('http://127.0.0.1:8000/api/submit_data/?user__email=example@gmail.com')
assert response.status_code == 200
