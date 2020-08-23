from unittest import TestCase

from back.entities import Player
from back.game import Game
from tests.helpers import remove_id


class Test(TestCase):
    def setUp(self):
        self.game = Game()
        self.game.init_scene()

    def test_init_scene(self):
        self.assertEqual(16, len(self.game.entities))

    def test_get_info_statics(self):
        self.game.entities.sort(key=lambda x: x.context_id)
        res = self.game.entities[0].get_info()

        self.assertEqual({'aabb': (3000, 0, 3000, 3000), 'context_id': 'frame_east', 'type': 'Statics'}, res)

    def test_add_player(self):
        self.game.add_player()

        self.assertEqual(17, len(self.game.entities))

    def test_del_player(self):
        pl = self.game.add_player()

        self.game.del_player(pl)
        self.assertEqual(16, len(self.game.entities))

        self.game.del_player(Player(0, 0))
        self.assertEqual(16, len(self.game.entities))

    def test_get_state_none(self):
        self.assertIsNone(self.game.get_state())

    def test_get_state(self):
        self.maxDiff = None
        exp_res = {'effects': [], 'entities': [
            {'aabb': (3000, 0, 3000, 3000), 'context_id': 'frame_east', 'type': 'Statics'},
            {'aabb': (0, 0, 3000, 0), 'context_id': 'frame_north', 'type': 'Statics'},
            {'aabb': (0, 3000, 3000, 3000), 'context_id': 'frame_south', 'type': 'Statics'},
            {'aabb': (0, 0, 0, 3000), 'context_id': 'frame_west', 'type': 'Statics'},
            {'aabb': (0, 0, 737, 1048), 'context_id': 'island_001', 'type': 'Statics'},
            {'aabb': (2, 1829, 890, 2997), 'context_id': 'island_002', 'type': 'Statics'},
            {'aabb': (864, 2633, 2996, 2995), 'context_id': 'island_003', 'type': 'Statics'},
            {'aabb': (1676, 2287, 2333, 2763), 'context_id': 'island_004', 'type': 'Statics'},
            {'aabb': (2542, 1504, 2994, 2625), 'context_id': 'island_005', 'type': 'Statics'},
            {'aabb': (2108, 967, 2992, 1495), 'context_id': 'island_00', 'type': 'Statics'},
            {'aabb': (2639, 457, 2992, 999), 'context_id': 'island_007', 'type': 'Statics'},
            {'aabb': (2479, 305, 2662, 684), 'context_id': 'island_008', 'type': 'Statics'},
            {'aabb': (1541, 800, 1789, 1063), 'context_id': 'island_009', 'type': 'Statics'},
            {'aabb': (1612, 624, 1953, 750), 'context_id': 'island_010', 'type': 'Statics'},
            {'aabb': (1315, 623, 1576, 768), 'context_id': 'island_011', 'type': 'Statics'},
            {'aabb': (720, 0, 1619, 194), 'context_id': 'island_012', 'type': 'Statics'},
            {'context_id': 'ship_0012', 'hp': 100, 'hp_max': 100, 'name': '', 'score': 0, 'type': 'Enemy'}
        ], 'entities_count': 17}

        self.game.exec_step(0.1)
        act_res = self.game.get_state()
        act_res['entities'] = list(map(remove_id, act_res['entities']))
        self.assertEqual(exp_res, act_res)
