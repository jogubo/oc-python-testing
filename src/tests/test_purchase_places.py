def test_purchase_places_with_valid_data(mocker, client,  clubs, competitions):
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.competitions', competitions)
    data = {
        'club': clubs[0]['name'],
        'competition': competitions[0]['name'],
        'places': f"{1}",
    }
    response = client.post('purchase-places', data=data)
    assert response.status_code == 200
    assert 'Great-booking complete!' in response.data.decode()
    assert 'Competition over' not in response.data.decode()


def test_purchase_places_with_more_points_than_available(
    mocker, client, clubs, competitions
):
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.competitions', competitions)
    data = {
        'club': clubs[0]['name'],
        'competition': competitions[0]['name'],
        'places': f"{int(clubs[0]['points']) + 1}",
    }
    mocker.patch('server.MAX_BOOK', int(data['places']) + 1)
    response = client.post('purchase-places', data=data)
    data = response.data.decode()
    assert response.status_code == 200
    assert 'You do not have enough points' in response.data.decode()


def test_purchase_places_over_book_limit(mocker, client, clubs, competitions):
    mocker.patch('server.MAX_BOOK', 1)
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.competitions', competitions)
    data = {
        'club': clubs[0]['name'],
        'competition': competitions[0]['name'],
        'places': f"{2}",
    }
    response = client.post('purchase-places', data=data)
    assert response.status_code == 200
    assert 'You cannot purchase more than' in response.data.decode()


def test_purchase_places_over_date_limit(mocker, client,  clubs, competitions):
    for competition in competitions:
        competition['date'] = "2000-01-01 10:00:00"
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.competitions', competitions)
    data = {
        'club': clubs[0]['name'],
        'competition': competitions[0]['name'],
        'places': f"{1}",
    }
    response = client.post('purchase-places', data=data)
    assert response.status_code == 200
    assert 'Great-booking complete!' not in response.data.decode()
    assert 'Competition over' in response.data.decode()


def test_no_link_to_purchase_page_of_past_competition(
    mocker, client,  clubs, competitions
):
    for competition in competitions:
        competition['date'] = "2000-01-01 10:00:00"
    mocker.patch('server.clubs', clubs)
    mocker.patch('server.competitions', competitions)
    response = client.post('show-summary', data=clubs[0])
    assert response.status_code == 200
    assert 'Competition over' in response.data.decode()
