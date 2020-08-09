from unittest import TestCase

from starlette.testclient import TestClient

from back.main import app


class Test(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_load_data(self):
        response = self.client.get('/load_data')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'height': 71,
                          'hp_max': 100,
                          'offset_x': -25,
                          'offset_y': -35,
                          'points': [{'x': 18, 'y': 5},
                                     {'x': 32, 'y': 5},
                                     {'x': 50, 'y': 26},
                                     {'x': 25, 'y': 71},
                                     {'x': 0, 'y': 26}],
                          'texture': 'spaceship_main.png',
                          'type': 'ship',
                          'width': 50,
                          'x': 0,
                          'y': 0}, response.json()['ship_0019'])
