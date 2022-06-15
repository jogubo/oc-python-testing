from server import load_clubs, load_competitions


def test_load_clubs_and_check_data():
    clubs = load_clubs()
    for club in clubs:
        assert 'name' and 'email' and 'points' in club


def test_load_competitions_and_check_data():
    competitions = load_competitions()
    for competitions in competitions:
        assert 'name' and 'date' and 'places' in competitions
