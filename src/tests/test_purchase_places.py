def test_purchase_places_with_valid_data(config, client,  club, competition):
    data = {
        'club': club['name'],
        'competition': competition['name'],
        'places': f"{1}",
    }
    response = client.post('purchase-places', data=data)
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Great-booking complete!' in data
