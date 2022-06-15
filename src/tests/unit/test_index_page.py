def test_get_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Welcome' and 'Portal' in response.data.decode()
