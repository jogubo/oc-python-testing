def test_logout(client):
    response = client.get('logout')
    assert response.status_code == 302
