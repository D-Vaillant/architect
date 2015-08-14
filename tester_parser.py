import unittest

from parsy import Parser
from game import Game
from item import Item
from rooms import Room
from inventory import Inventory
from actions import Action

from tester_game_module import Game_Tester

class Parser_Tester(Game_Tester):
    def setUp(self):
        super().setUp()
        self.parser = Parser(self.G.rooms, self.G.items, 
                             self.G.actions, self.G.inventory)

    def subtest_bp(self, w_q, phrase):
        w,q = w_q
        for n in phrase:
            with self.subTest(n=n):
                self.assertEqual(w([n]), self.parser.BP_Parse(q(n)))

    def test_bp_put(self):
        W = "puts"
        w_q = lambda i: (W, i), lambda j: (W+'!'+j)
        put_phrases = ["rocket hats", "worf@hat", "hi hi @ hi !",
                        "believe in Ur ha_t"]
        self.subtest_bp(w_q, put_phrases)

    def test_bp_link(self):
        W = "link"
        w_q = lambda i: (W, [i[:i.find('-')], i[i.find('>')+1:]]),\
              lambda j: (W+'!'+j)
        link_phrases = ["initial-W->basement", "basement-N->flowers",
                        "flowers-S->initial"]
        self.subtest_bp(w_q, link_phrases)

    def test_bp_add(self):
        W = "add"
        w_q = lambda i: ((W, i[:i.find('.')].split('@') + [i[i.find('.')+1:]])
                         if '.' in i else (W, i.split('@'))),\
              lambda j: (W+'!'+j)
        add_phrases = ["bauble@initial", "notebook@_",
                       "bauble@_.main"]
        self.subtest_bp(w_q, add_phrases)

    def test_bp_remove(self):
        W = "remove"
        w_q = lambda i: (W, i.split('@')),\
              lambda j: (W+'!'+j)
        remove_phrases = ["bauble@_", "notebook@initial",
                          "painting@basement"]
        self.subtest_bp(w_q, remove_phrases)

    def test_bp_changeItem(self):
        W = "changeItem"
        w_q = lambda i: (W, i[:i.find('=')].split('.') + [i[i.find('=')+1:]]),\
              lambda j: (W+'!'+j)
        change_phrases = ["bauble.nick=heckball", "bauble.name=black heckball",
                          "notebook.weight=5", "notebook.ground_desc=not real"]
        self.subtest_bp(w_q, change_phrases)
    
    def test_bp_changeRoom(self):
        change_phrases = ["basement.name=notbasement", "initial.name=house"]
        self.subtest_bp("changeRoom", change_phrases)


if __name__ == '__main__': unittest.main()
