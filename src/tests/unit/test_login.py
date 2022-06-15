def test_with_know_email(mocker, client, clubs):
    mocker.patch('server.clubs', clubs)
    response = client.post('show-summary', data=clubs[0])
    assert response.status_code == 200


def test_with_unknow_email(mocker, client, clubs):
    mocker.patch('server.clubs', clubs)
    response = client.post('show-summary', data={'email': 'test@unlisted'})
    assert response.status_code == 302
