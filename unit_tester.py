import unittest
import tempfile
from collections import OrderedDict
##from file_management import File_Processor
from json_reader import InfoCollector
from game import Game
from rooms import Room
from item import Item
from actions import Action
from inventory import Inventory

class Game_Loader(unittest.TestCase):
    def setUp(self):
        self.Reader = InfoCollector()
        self.Reader.main()
        
class JR_Tester(Game_Loader):
    def test_JR_rooms(self):
        roomDict = Room.room_processor(self.Reader.room_info)
        for r in roomDict:
            self.subtest_room(self.Reader.room_info[r], roomDict[r])

    def subtest_room(self, roomJR, roomOBJ):
        grabObjVar = lambda q: getattr(roomOBJ, q)
        
        for key, r_var in roomOBJ.codes.items():
                if key in roomJR:
                    if key == "desc" and len(grabObjVar(r_var)) == 1:
                        self.assertEqual(grabObjVar(r_var)[0], roomJR[key])
                    else:
                        self.assertEqual(grabObjVar(r_var), roomJR[key])
                else:
                    if key == "links":
                        self.assertEqual(roomOBJ.links, [None]*4)
                    elif key == "desc":
                        self.assertEqual(roomOBJ.entry_desc, 
                                         ["This is a room."])
                    else:
                        self.assertEqual(grabObjVar(r_var), '')
                    
    def test_JR_actions(self):
        actDict = Action.action_processor(self.Reader.action_info)
        for a in actDict:
            self.subtest_action(self.Reader.action_info[a], actDict[a])
        
    def subtest_action(self, actionJR, actionOBJ):
        grabObjVar = lambda q: getattr(actionOBJ, q)

        for key, a_var in actionOBJ.codes.items():
            if key in actionJR:
                if key not in {"1", "2"}: 
                    self.assertEqual(grabObjVar(a_var), actionJR[key])
                else:
                    pass
            else:
                if key in {"1", "2"}:
                    self.assertEqual(grabObjVar(a_var), OrderedDict())
                else:
                    self.assertEqual(grabObjVar(a_var), '')
        
    
    def test_JR_items(self):
        itemDict = Item.item_processor(self.Reader.item_info)
        for i in itemDict:
            self.subtest_item(self.Reader.item_info[i], itemDict[i])

    def subtest_item(self, itemJR, itemOBJ):
        grabObjVar = lambda q: getattr(itemOBJ, q)
        
        for key, i_var in itemOBJ.codes.items():
            if key in itemJR:
                if key is "property":
                    self.assertEqual(grabObjVar(i_var), set(itemJR[key]))
                else:
                    self.assertEqual(grabObjVar(i_var), itemJR[key])
            else:
                if key == "weight":
                    self.assertEqual(grabObjVar(i_var), 0)
                elif key == "property":
                    self.assertEqual(grabObjVar(i_var), set())
                elif key == "nick":
                    if "name" in itemJR:
                        self.assertEqual(grabObjVar(i_var), itemJR['name'])
                    else:
                        self.assertEqual(grabObjVar(i_var), 'item')
                        
class Item_Tester(Game_Loader):
    def setUp(self):
        super().setUp()
        theItems = Item.item_processor(self.Reader.item_info)
        self.bauble = theItems["bauble"]
        self.painting = theItems["painting"]
        
    def test_Item_setProperty_adding_success(self):
        self.bauble.setProperty("static")
        self.assertIn("static", self.bauble.properties)
        
    def test_Item_setProperty_removing_success(self):
        self.bauble.setProperty("glass", False)
        self.assertNotIn("glass", self.bauble.properties)
        
    def test_Item_setProperty_removing_failure(self):
        self.assertTrue(self.bauble.setProperty("metal", False))
        
    def test_Item_setDescription_success(self):
        self.bauble.setDescription("ground", "Success.")
        self.assertEqual(self.bauble.ground_desc, "Success.")
        
    def test_Item_setDescription_failure(self):
        self.assertTrue(self.bauble.setDescription("stone", "Failure."))

class Room_Tester(Game_Loader):
    def setUp(self):
        super().setUp()
        theRooms = Room.room_processor(self.Reader.room_info)
        self.field = theRooms["flowers"]
        self.initial = theRooms["initial"]
       
    def test_Room_add(self):
        self.field.add("test_string")
        self.assertIn("test_string", self.field)
        
    def test_Room_add(self):
        x = self.initial.holding[0]
        self.initial.remove(x)
        self.assertNotIn(x, self.initial.holding)
        
    def test_Room_onEntry(self):
        self.assertFalse(self.field.is_visited)
        self.assertEqual(self.field.entry_desc, 
                         self.field.onEntry().split('\n'))          
        self.assertTrue(self.field.is_visited)
        
        self.assertFalse(self.initial.is_visited)
        self.assertEqual(self.initial.entry_desc,
                         self.initial.onEntry().split('\n'))
        self.assertTrue(self.initial.is_visited)
        
    def test_Room_link(self):
        self.field.link(self.initial, 0)
        self.assertEqual(self.field.links[0], self.initial)
        
class Action_Tester(Game_Loader):
    def setUp(self):
        super().setUp()
        theActions = Action.action_processor(self.Reader.action_info)
        self.unlock = theActions["unlock"]
        self.cry = theActions["cry"]
        self.tap = theActions["tap"]

    def test_Action_min_cry(self):
        self.assertEqual(self.cry.min, 0)

    def test_Action_min_unlock(self):
        self.assertEqual(self.unlock.min, 1)

    def test_Action_min_tap(self):
        self.assertEqual(self.tap.min, 1)

    def test_Action_max_cry(self):
        self.assertEqual(self.cry.max, 0)

    def test_Action_max_unlock(self):
        self.assertEqual(self.unlock.max, 2)

    def test_Action_max_tap(self):
        self.assertEqual(self.tap.max, 1)

    def test_Action_parseString_0_where_min_is_zero(self):
        self.assertEqual(self.cry.parseString([]), 0)

    def test_Action_parseString_0_where_min_greaterThan_zero(self):
        self.assertEqual(self.unlock.parseString([]), "$! 0 < Min")

    def test_Action_parseString_1_where_max_is_zero(self):
        self.assertEqual(self.cry.parseString(["rock"]), "$! Input > Min")

    def test_Action_parseString_1_successfully(self):
        self.assertEqual(self.unlock.parseString(["rock"]), ["rock"])

    def test_Action_parseString_2_where_prep_missing(self):
        self.assertEqual(self.unlock.parseString(["rock", "out"]), 
                                                 ["rock", "out"])

    def test_Action_parseString_2_successfully(self):
        self.assertEqual(self.unlock.parseString(["dance", "with", "style"]), 
                                                 ["dance", "style"])

class Game_Tester(Game_Loader):
    def setUp(self):
        super().setUp()
        self.G = Game(self.Reader.output)
        
        #Representing objects.
        self.bauble = self.G.items["bauble"]
        self.key = self.G.items["worn_key"]
        
        self.initial = self.G.rooms["initial"]
        self.basement = self.G.rooms["basement"]
        self.flowers = self.G.rooms["flowers"]
        
        self.cry = self.G.actions["cry"]
        
class Game_EngineMethod_Tester(Game_Tester):
    def setUp(self):
        super().setUp()
    
    def test_moveItem_roomXroom(self):
        self.assertIn(self.bauble, self.initial)
        self.G._moveItem(self.bauble,
                         self.initial, self.basement)
        self.assertIn(self.bauble, self.basement)
        
    def test_moveItem_roomXinv(self):
        self.assertIn(self.bauble, self.initial)
        self.G._moveItem(self.bauble, 
                         self.initial, self.G.inventory)
        self.assertIn(self.bauble, self.G.inventory)
        
    def test_moveItem_invXroom(self):
        self.G.inventory.add(self.key)
        self.G._moveItem(self.bauble, self.initial)
        self.assertIn(self.bauble, self.initial)
    
    @unittest.skip
    def test_moveItem_errors(self):
        return
    @unittest.skip
    def test_IDtoItem(self):
        return
    @unittest.skip
    def test_IDtoItem_error(self):
        return
    
if __name__ == '__main__': unittest.main()
