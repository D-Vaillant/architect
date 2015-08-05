import unittest
import mock

from collections import OrderedDict
from json_reader import InfoCollector
from game import Game
from rooms import Room
from item import Item
from actions import Action
from inventory import Inventory

from tester_ontology import Game_Loader
       
class Game_Tester(Game_Loader):
    def setUp(self):
        super().setUp()
        self.G = Game(*self.Reader.output())
        
        #Representing objects.
        self.bauble = self.G.items["bauble"]
        self.key = self.G.items["worn_key"]
        
        self.initial = self.G.rooms["initial"]
        self.basement = self.G.rooms["basement"]
        self.flowers = self.G.rooms["flowers"]
        
        self.cry = self.G.actions["cry"]
      
class Game_EngineMethod_Tester(Game_Tester):
    def test_moveItem_roomXroom(self):
        """ Testing whether Items can be moved between Rooms. """
        self.assertIn(self.bauble, self.initial)
        self.G._moveItem(self.bauble,
                         self.initial, self.basement)
        self.assertIn(self.bauble, self.basement)
        
    def test_moveItem_roomXinv(self):
        """ Testing whether we can move Items from Rooms to Inventories. """
        self.assertIn(self.bauble, self.initial)
        self.G._moveItem(self.bauble, 
                         self.initial, self.G.inventory)
        self.assertIn(self.bauble, self.G.inventory)
        
    def test_moveItem_invXroom(self):
        """ Testing whether we can move Items from Inventories to Rooms. """
        self.G.inventory.add(self.key)
        self.G._moveItem(self.key, 
                         self.G.inventory, self.initial)
        self.assertIn(self.key, self.initial)
    
    def test_moveItem_errors(self):
        """ Testing error catching of _moveItem method. """
        X = [1, 2]
        
        with self.assertRaises(AttributeError,
                               msg="Target lacks add() method."):
            self.G._moveItem(self.bauble, self.initial, X)
            
        with self.assertRaises(AttributeError, msg="Item not in source."):
            self.G._moveItem(self.bauble, X, self.flowers)
        
    def test_IDtoItem(self):
        """ Testing whether correct Item is returned. """
        self.assertEqual(self.G._IDtoItem("bauble"), self.bauble)
        self.assertEqual(self.G._IDtoItem("worn_key"), self.key)
        
    def test_IDtoItem_error(self):
        """ Testing error catching of _IDtoItem method. """
        with self.assertRaises(NameError, msg="No item with ID hat"):
            self.G._IDtoItem("hat")

class Game_Parser_Tester(Game_Tester):
    @mock.patch.object(Game, '_move')
    def test_prompt_exe_move(self, mock__move):
        cardinal_list = ['north', 'south', 'east', 'west']
        assoc = {x:x[0] for x in cardinal_list}
        assoc.update({x:x for x in [_[0] for _ in cardinal_list]})
        
        for i, j in assoc.items():
            with self.subTest(i = i):
                self.G.prompt_exe(i)
                mock__move.assert_called_with(j)
            
    @mock.patch.object(Game, '_inv')
    def test_prompt_exe_inv(self, mock__inv):
        arr = ['inv', 'i']
        for x in arr:
            with self.subTest(x = x):
                self.G.prompt_exe(x)
                mock__inv.assert_called_with("open")
         
    @mock.patch.object(Game, '_act')
    def test_prompt_exe_act(self, mock__act):
        pass
    
    @mock.patch.object(Game, '_help')
    def test_prompt_exe_help(self, mock__help):
        arr = ['', 'as', '32']
        for x in arr:
            with self.subTest(x = x):
                self.G.prompt_exe('? ' + x)
                mock__help.assert_called_with(x)
        
    def test_prompt_exe_empty(self):
        self.assertIsNone(self.G.prompt_exe(""))
        
    @mock.patch.object(Game, '_puts')
    def test_prompt_exe_error(self, mock__puts):
        self.G.prompt_exe("asdfas")
        mock__puts.assert_called_with(self.G.ERROR["exe_pass"])

    @mock.patch.object(Game, '_puts')
    def test_itemNametoID(self, mock__puts):
        self.G.loc = self.G.rooms['entrance']
        self.assertEqual(self.G._itemNametoID('worn key'),
                         'worn_key')
        self.assertEqual(self.G._itemNametoID('key'),
                         'worn_key')
        self.G._itemNametoID('ascvas')
        mock__puts.assert_called_with(self.G.ERROR["item_not_found"])
    
class Game_ActionParser_Tester(Game_Tester):
    @mock.patch('builtins.print', autospec=True)
    def test_nonaction(self, mock_print):
        self.G._act(['ast'])
        mock_print.assert_called_with("Non-action. Why are we here?")
    
if __name__ == '__main__': unittest.main()
