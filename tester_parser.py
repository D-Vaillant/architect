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
        self.w_q = lambda word:(lambda i: (word, i)),
                               (lambda i: (word+'!'+j))

    def subtest_bp(self, word, phrases):
        w,q = self.w_q(word)
        for n in phrases:
            with self.subTest(n=n):
                self.assertEqual(w([n]), self.parser.BP_Parse(q(n)))

    def test_bp_put(self):
        put_phrases = ["rocket hats", "worf@hat", "hi hi @ hi !",
                        "believe in Ur ha_t"]
        self.subtest_bp("put", put_phrases)

    def test_bp_link(self):
        link_phrases = ["initial-W->basement", "basement-N->flowers",
                        "flowers-S->initial"]
        self.subtest_bp("link", link_phrases)

    def test_bp_add(self):
        add_phrases = ["bauble@initial", "notebook@_",
                       "bauble@_.main"]
        self.subtest_bp("add", add_phrases)

    def test_bp_remove(self):
        remove_phrases = ["bauble@_", "notebook@initial",
                          "painting@basement"]
        self.subtest_bp("remove", remove_phrases)

    def test_bp_changeItem(self):
        change_phrases = ["bauble.nick=heckball", "bauble.name=black heckball",
                          "notebook.weight=5", "notebook.ground_desc=not real"]
        self.subtest_bp("changeItem", change_phrases)
    
    def test_bp_changeRoom(self):
        change_phrases = ["basement.name=notbasement", "initial.name=house"]
        self.subtest_bp("changeRoom", change_phrases)
if __name__ == '__main__': unittest.main()
