from flask_testing import LiveServerTestCase
from selenium import webdriver

import server


class UserTakesTheTest(LiveServerTestCase):

    def create_app(self):
        return server.app

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_main_page(self):
        self.driver.get(self.get_server_url())
        assert self.driver.current_url == 'http://localhost:5000/'
        assert 'GUDLFT Registration' == self.driver.title

    def test_points_board_page(self):
        self.driver.get('http://localhost:5000/points-board')
        assert 'Clubs Points Board | GUDLFT' == self.driver.title
