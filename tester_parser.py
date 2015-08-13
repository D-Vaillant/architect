import unittest

from parsy import Parser
from game import Game
from item import Item
from rooms import Room
from inventory import Inventory
from actions import Actions

from tester_ontology import Game_Loader

class Parser_Tester(Game_Loader):
    def setUp(self):
        super().setUp()
        self.parser = Parser(self.G.rooms, self.G.items, self.G.actions)

    def test_bp_parsing(self):
        for cmd in self.parser.bp_commands:
            with self.subTest(cmd=cmd):
                self.subtest_bp_cmd_parse(self, cmd)
    
    def subtest_bp_cmd_parse(self, cmd):
        ''' Should probably refactor this.
            The question is: one test per command or one subtest for
            each command? '''
        pass
