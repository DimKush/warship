from unittest import TestCase

from back.game import Game


class Test(TestCase):
    def setUp(self):
        self.game = Game()

    def test_init_scene(self):
        self.game.load_objects()
        self.assertEqual(16, len(self.game.entities))
