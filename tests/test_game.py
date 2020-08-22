from unittest import TestCase

from back.game import Game


class Test(TestCase):
    def setUp(self):
        self.game = Game()
        self.game.load_objects()

    def test_init_scene(self):
        self.assertEqual(16, len(self.game.entities))

    def test_get_info_statics(self):
        res = self.game.entities[0].get_info()
        self.assertEqual({'aabb': (3000, 0, 3000, 3000), 'context_id': 'frame_east', 'type': 'Statics'}, res)

