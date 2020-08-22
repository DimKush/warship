from unittest import TestCase

from back.effects import EffectFactory, ActionFactory


class TestEffectFactory(TestCase):
    def setUp(self):
        self.eff_fact = EffectFactory()

    def test_add_to_pool(self):
        self.eff_fact.add_to_pool('explodes_01', 10, 130)
        self.eff_fact.add_to_pool('explodes_04', 25, 25)

        self.assertEqual([{'id': 'explodes_01', 'x': 10, 'y': 130}, {'id': 'explodes_04', 'x': 25, 'y': 25}],
                         self.eff_fact.pool)

    def test_get_effects(self):
        self.eff_fact.add_to_pool('explodes_04', 25, 25)

        res = self.eff_fact.get_effects()
        self.assertEqual([{'id': 'explodes_04', 'x': 25, 'y': 25}], res)
        self.assertEqual([], self.eff_fact.pool)


class TestActionFactory(TestCase):
    def setUp(self):
        self.act_fact = ActionFactory()

    def test_add_to_pool(self):
        def my_action_func(a, b):
            return a + b

        self.act_fact.add_to_pool(6, my_action_func, 6, 7)
        self.assertEqual([{'args': (6, 7), 'count': 6, 'func': my_action_func}], self.act_fact.pool)

    def test_do_tick(self):
        gl_list = []

        def my_action_func(a, b):
            gl_list.append(a + b)

        self.act_fact.add_to_pool(2, my_action_func, 6, 7)
        self.act_fact.do_tick()

        self.assertEqual([13], gl_list)
        self.assertEqual(1, self.act_fact.pool[0]['count'])

        self.act_fact.do_tick()
        self.act_fact.do_tick()
        self.assertEqual([13, 13], gl_list)
        self.assertEqual([], self.act_fact.pool)

    def test_clear_pool(self):
        self.act_fact.clear_pool()
        self.assertEqual([], self.act_fact.pool)
