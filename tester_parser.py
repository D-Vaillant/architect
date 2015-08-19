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

class bpParser_Tester(Parser_Tester):
    def subtest_bp(self, W, test_dict):
        E_ = lambda x: W+'!'+x
        P_ = lambda x: (W, x)
        for entry, parsed in test_dict.items():
            with self.subTest(entry=entry,parsed=parsed):
                self.assertEqual(self.parser.bpParse(E_(entry)),
                                 P_(parsed))

    def test_bp_put(self):
        put_dict = {"rocket hats":["rocket hats"],
                    "worf@hat"   :["worf@hat"],
                    "hi hi @ hi !":["hi hi @ hi !"],
                    "believe in Ur ha_t":["believe in Ur ha_t"],}
        self.subtest_bp("put",put_dict)

    def test_bp_link(self):
        link_dict = {"initial-W->basement":["initial","W","basement"],
                    "basement-N->flowers":["basement","N","flowers"],
                    "flowers-S->initial":["flowers","S","initial"],}
        self.subtest_bp("link",link_dict)

    def test_bp_add(self):
        add_dict = {"bauble@initial":["bauble", "initial"],
                    "notebook@_":["notebook", "_"],
                    "bauble@_.main":["bauble", "_", "main"]}
        self.subtest_bp("add",add_dict)

    def test_bp_remove(self):
        remove_dict = {"bauble@_"         :["bauble", "_"],
                       "notebook@initial" :["notebook", "initial"],
                       "painting@basement":["painting", "basement"]}
        self.subtest_bp("remove",remove_dict)

    def test_bp_changeItem(self):
        change_dict = {
            "bauble.nick=heckball":["bauble","nick","heckball"],
            "bauble.name=black heckball":["bauble","name","black heckball"],
            "notebook.weight=5":["notebook","weight","5"], 
            "notebook.ground_desc=not real":
                    ["notebook","ground_desc","not real"],
                         }
        self.subtest_bp("changeItem",change_dict)
    
    def test_bp_changeRoom(self):
        change_dict = {
            "basement.name=notbasement":["basement","name","notbasement"],
            "initial.name=house":["initial","name","house"]
                      }
        self.subtest_bp("changeRoom",change_dict)

class Action_Parser_Tester(Parser_Tester):
    def setUp(self):
        super().setUp()
        theActions = self.parser.actions
        self.unlock = theActions["unlock"]
        self.cry = theActions["cry"]
        self.tap = theActions["tap"]

    def test_Action_actionParse_0_where_min_is_zero(self):
        self.assertEqual(self.parser.actionParse(self.cry, ''), 
                         [])

    def test_Action_actionParse_0_where_min_greaterThan_zero(self):
        self.assertEqual(self.parser.actionParse(self.unlock, ''),
                         "$! 0 < Min")

    def test_Action_actionParse_1_where_max_is_zero(self):
        self.assertEqual(self.parser.actionParse(self.cry, "bauble"), 
                         "$! Input > Min")

    def test_Action_actionParse_1_successfully(self):
        self.assertEqual(self.parser.actionParse(self.tap, "bauble"), 
                         ["bauble"])

    def test_Action_actionParse_2_where_prep_missing(self):
        self.assertEqual(self.parser.actionParse(self.unlock, "door key"), 
                                                 "$! Input < Min")

    def test_Action_actionParse_2_successfully(self):
        self.assertEqual(self.parser.actionParse(self.unlock, "door with key"), 
                                                 ["door", "key"])
  


if __name__ == '__main__': unittest.main()
