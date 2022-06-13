def test_purchase_places_with_valid_data(config, client,  club, competition):
    data = {
        'club': club['name'],
        'competition': competition['name'],
        'places': f"{1}",
    }
    response = client.post('purchase-places', data=data)
    assert response.status_code == 200
    assert 'Great-booking complete!' in response.data.decode()


def test_purchase_places_with_more_points_than_available(
    mocker, client,  config, club, competition
):
    data = {
        'club': club['name'],
        'competition': competition['name'],
        'places': f"{int(club['points']) + 1}",
    }
    mocker.patch('server.MAX_BOOK', int(data['places']) + 1)
    response = client.post('purchase-places', data=data)
    data = response.data.decode()
    assert response.status_code == 200
    assert 'You do not have enough points' in response.data.decode()


def test_purchase_places_over_book_limit(
    mocker, client, config, club, competition
):
    mocker.patch('server.MAX_BOOK', 1)
    data = {
        'club': club['name'],
        'competition': competition['name'],
        'places': f"{2}",
    }
    response = client.post('purchase-places', data=data)
    assert response.status_code == 200
    assert 'You cannot purchase more than' in response.data.decode()
