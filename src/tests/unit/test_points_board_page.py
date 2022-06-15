def test_get_points_board_page(client):
    response = client.get('/points-board')
    assert response.status_code == 200
    assert 'Clubs' in response.data.decode()
    assert 'Points' in response.data.decode()
