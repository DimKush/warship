from unittest import TestCase

from back.entities import Enemy, Player, Statics


class TestEnemy(TestCase):
    def setUp(self):
        self.enemy = Enemy(50, 50)

    def test_action_on_collision_with_player(self):
        prev_hp = self.enemy.hp
        self.enemy.action_on_collision(Player(0, 0))
        self.assertEqual(prev_hp, self.enemy.hp)

    def test_action_on_collision_with_statics(self):
        prev_hp = self.enemy.hp
        self.enemy.action_on_collision(Statics(0, 0))
        self.assertEqual(prev_hp, self.enemy.hp)

    def test_action_on_collision_with_bad_type(self):
        prev_hp = self.enemy.hp
        self.enemy.action_on_collision(None)
        self.assertEqual(prev_hp, self.enemy.hp)

    def test_next(self):
        # Со старта не сталкивается, немного поездить надо
        for _ in range(0, 10):
            self.enemy.next(1, [])

        prev_coords = int(self.enemy.x), int(self.enemy.y)
        self.enemy.action_on_collision(Statics(0, 0))
        for _ in range(0, 10):
            self.enemy.next(1, [])

        self.assertNotEqual(prev_coords, (int(self.enemy.x), int(self.enemy.y)))
