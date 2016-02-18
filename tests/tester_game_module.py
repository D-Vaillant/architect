import unittest
import mock
from collections import OrderedDict

from architect.game import Game
from architect.utils import JSON_Reader
from architect.ontology import Room, Item, Action, Inventory

# TODO: Find this guy a nice home.
class Game_Loader(unittest.TestCase):
    """ Abstract base class that testing units inherit from. """
    def setUp(self):
        self.Reader = JSON_Reader()
        self.Reader.main()
      
class Game_Tester(Game_Loader):
    def setUp(self):
        super().setUp()
        self.G = Game(*self.Reader.output())
        
        #Representing objects.
        self.bauble = self.G.items["bauble"]
        self.key = self.G.items["worn_key"]
        self.door = self.G.items["old_door"]
        
        self.initial = self.G.rooms["initial"]
        self.basement = self.G.rooms["basement"]
        self.entrance = self.G.rooms["entrance"]
        self.house = self.G.rooms["house"]
        self.flowers = self.G.rooms["flowers"]
        
        self.cry = self.G.actions["cry"]
      
class Game_EngineMethod_Tester(Game_Tester):
    """ Responsible for testing Blueprint functions. """
    def test_linking(self):
        self.assertNotIn(self.house, self.entrance.links)
        self.G._link("entrance", 'N', "house")
        self.assertIs(self.entrance.links[2], self.house)

    def test_move_roomXroom(self):
        """ Testing whether Items can be moved between Rooms. """
        self.assertIn(self.bauble, self.initial)
        self.G._move(self.bauble,
                         self.initial, self.basement)
        self.assertIn(self.bauble, self.basement)
        
    def test_move_roomXinv(self):
        """ Testing whether we can move Items from Rooms to Inventories. """
        self.assertIn(self.bauble, self.initial)
        self.G._move(self.bauble, 
                         self.initial, self.G.inventory)
        self.assertIn(self.bauble, self.G.inventory)
        
    def test_move_invXroom(self):
        """ Testing whether we can move Items from Inventories to Rooms. """
        self.G.inventory.add(self.key)
        self.G._move(self.key, 
                         self.G.inventory, self.initial)
        self.assertIn(self.key, self.initial)
    
    def test_move_errors(self):
        """ Testing error catching of _move method. """
        X = [1, 2]
        
        with self.assertRaises(AttributeError,
                               msg="Target lacks add() method."):
            self.G._move(self.bauble, self.initial, X)
            
        with self.assertRaises(AttributeError, msg="Item not in source."):
            self.G._move(self.bauble, X, self.flowers)
        
    def test_IDtoItem(self):
        """ Testing whether correct Item is returned. """
        self.assertEqual(self.G._IDtoItem("bauble"), self.bauble)
        self.assertEqual(self.G._IDtoItem("worn_key"), self.key)
        
    def test_IDtoItem_error(self):
        """ Testing error catching of _IDtoItem method. """
        with self.assertRaises(NameError, msg="No item with ID hat"):
            self.G._IDtoItem("hat")

class Game_Prompt_Tester(Game_Tester):
    @mock.patch.object(Game, '_movePlayer')
    def test_prompt_exe_movePlayer(self, mock__movePlayer):
        cardinal_list = ['north', 'south', 'east', 'west']
        assoc = {x:x[0] for x in cardinal_list}
        assoc.update({x:x for x in [_[0] for _ in cardinal_list]})
        
        for i, j in assoc.items():
            with self.subTest(i = i):
                self.G.prompt_exe(i)
                mock__movePlayer.assert_called_with(j)
            
    @mock.patch.object(Game, '_inv')
    def test_prompt_exe_inv(self, mock__inv):
        arr = ['inv', 'i']
        for x in arr:
            with self.subTest(x = x):
                self.G.prompt_exe(x)
                mock__inv.assert_called_with("open")
         
    @mock.patch.object(Game, '_act')
    def test_prompt_exe_act(self, mock__act):
       arr = ["take rocket ship", "unlock red door", "cry"]
       for x in arr:
           with self.subTest(x = x):
               self.G.prompt_exe(x)
               mock__act.assert_called_with(x.split())
    
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
    def test_itemNametoItem(self, mock__puts):
        self.G.loc = self.G.rooms['entrance']
        self.assertEqual(self.G._itemNametoItem('worn key'),
                         self.key)
        self.assertEqual(self.G._itemNametoItem('key'),
                         self.key)
        self.G._itemNametoItem('ascvas')
        mock__puts.assert_called_with(self.G.ERROR["item_not_found"])
    
class Game_ActionSystem_Tester(Game_Tester):
    @mock.patch('builtins.print', autospec=True)
    def test_nonaction(self, mock_print):
        self.G._act(['ast'])
        self.assertRaises(RunTimeError, self.G._act, ['ast'])
        #mock_print.assert_called_with("Non-action. Why are we here?")
    
    @mock.patch.object(Game, '_specialAct')
    def test_actToSpecialAct(self, mock__specialAct):
        self.G._act(["take", "rocketship", "moon"])
        mock__specialAct.assert_called_with("take", "rocketship moon")

    @mock.patch.object(Game, '_puts')
    def test_userAct_invalidAct(self, mock__puts):
        act_dict = {("unlock","door"):Game.ACT_MSGS["Input < Min"],
                    ("cry","door")   :Game.ACT_MSGS["Input > Max"],
                    ("unlock",)       :Game.ACT_MSGS["0 < Min"],}
        for cmd, output in act_dict.items():
            cmd = list(cmd)
            with self.subTest(cmd=cmd,output=output):
                self.G._act(cmd)
                mock__puts.assert_called_with(output)

    @mock.patch.object(Game, '_puts')
    def test_userAct_exceptionRaise(self, mock__puts):
        self.G._act("tap florgisborg".split())
        mock__puts.assert_called_with(Game.ERROR["item_not_found"])

    def test_unaryTester(self):
        prop_dict = {
                        "p:wooden"  :[False,False,True],
                        "p:metal"   :[False,True,False],
                        "p:glass"   :[True,False,False],
                        "bauble"    :[True,False,False],
                        "old_door"  :[False,False,True],
                        "p:locked"  :[False,False,True],
                        ""          :[True,True,True],
                        "grue"      :[False,False,False],
                    }
        test_arr = [self.bauble, self.key, self.door]
        for number, item in enumerate(test_arr):
            for key, value in prop_dict.items():
                with self.subTest(key=key,value=value):
                    self.assertEqual(Action.unaryTest(item, key),value[number])

    def test_pluralUnaryTester(self):
        prop_dict = {
                ("old_door","p:locked") :[False,False,True],
                ("p:wooden","p:locked") :[False,False,True],
                ("p:glass","p:wooden")  :[False,False,False],
                ("",)                   :[True,True,True],
                ("grue",)               :[False,False,False],
                ("p:glass","bauble")    :[True,False,False],
                ("p:wooden",)           :[False,False,True],
                ("p:metal",)            :[False,True,False],
                }
        test_arr = [self.bauble, self.key, self.door]
        for number,item in enumerate(test_arr):
            for key, value in prop_dict.items():
                with self.subTest(key=key,value=value):
                    self.assertEqual(Action.pluralUnaryTest(item,key),
                                     value[number])
    

if __name__ == '__main__': unittest.main()
