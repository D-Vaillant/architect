""" tester_ontology: 
        Tests the ability to read Game information from a JSON-formatted file 
        and various internal methods of objects. """

import unittest
import mock
from collections import OrderedDict

from architect.utils import JSON_Reader, Parser
from architect.ontology import Room, Item, Inventory, Action

from tests.tester_game_module import Game_Loader, Game_Tester

testing_JR = True
testing_actions = True
testing_items = True
testing_rooms = True
        
class JR_Tester(Game_Loader):
    """ Tests json_reader and processor abilities to translate info. """
    @unittest.skipUnless(testing_JR, "not testing this")
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
                    elif key == "hold":
                        self.assertEqual(roomOBJ.holding, [])
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
                if key not in {"0", "1", "2"}: 
                    self.assertEqual(grabObjVar(a_var), actionJR[key])
                elif key == "0":
                    self.assertEqual(grabObjVar(a_var), [actionJR[key]])
                else:
                    pass
            else:
                if key == '0': 
                    self.assertEqual(grabObjVar(a_var), ['pass'])
                elif key == '1':
                    self.assertEqual(grabObjVar(a_var), {'':['pass']})
                elif key == '2':
                    self.assertEqual(grabObjVar(a_var), {'|':['pass']})
                else: continue
    
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
    @unittest.skipUnless(testing_items, "not testing this")
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
    @unittest.skipUnless(testing_rooms, "not testing this")
    def setUp(self):
        super().setUp()
        theRooms = Room.room_processor(self.Reader.room_info)
        self.field = theRooms["flowers"]
        self.initial = theRooms["initial"]
       
    def test_Room_add(self):
        self.field.add("test_string")
        self.assertIn("test_string", self.field)
        
    def test_Room_remove(self):
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
    @unittest.skipUnless(testing_actions, "not testing this")
    def setUp(self):
        super().setUp()
        self.theActions = Action.action_processor(self.Reader.action_info)
        self.unlock = self.theActions["unlock"]
        self.cry = self.theActions["cry"]
        self.tap = self.theActions["tap"]

    def test_Action_min_cry(self):
        self.assertEqual(self.cry.min, 0)

    def test_Action_min_unlock(self):
        self.assertEqual(self.unlock.min, 2)

    def test_Action_min_tap(self):
        self.assertEqual(self.tap.min, 1)

    def test_Action_max_cry(self):
        self.assertEqual(self.cry.max, 0)

    def test_Action_max_unlock(self):
        self.assertEqual(self.unlock.max, 2)

    def test_Action_max_tap(self):
        self.assertEqual(self.tap.max, 1)

    def test_zeroAction_format(self):
        for x in self.theActions.values():
            if x.zero_act == '': continue
            else: self.assertIsInstance(x.zero_act, list)

    def test_unaryAction_format(self):
        for x in self.theActions.values():
            if x.unary_act == {'':['pass']}: continue
            self.assertIsInstance(x.unary_act, OrderedDict)
            for key, value in x.unary_act.items():
                with self.subTest(key=key,value=value):
                    self.assertIsInstance(key, tuple)
                    self.assertIsInstance(value, list)

    def test_binaryAction_format(self):
        for x in self.theActions.values():
            if x.binary_act == {'|':['pass']}: continue
            self.assertIsInstance(x.binary_act, OrderedDict)
            for key, value in x.binary_act.items():
                with self.subTest(key=key,value=value):
                    for _ in key:
                        self.assertIsInstance(_, tuple)
                        for __ in _: self.assertIsInstance(__, str)
                    self.assertIsInstance(value, list)

class Ontology_InventoryTester(Game_Tester):
    def setUp(self):
        super().setUp()
        self.inv = self.G.inventory
        self.inv.holding["main"] = set(self.key)

    def test_adding(self):
        self.inv.add(self.bauble)
        self.assertIn(self.bauble, self.inv.holding["main"])

    def test_contains:(self):
        self.assertTrue(self.key in self.inv)
        self.assertFalse(self.door in self.inv)

    def test_listCasting(self):
        self.assertEqual([self.key], list(self.inv))
        self.inv.add(self.bauble)
        self.assertEqual([self.key, self.bauble], list(self.inv))

if __name__ == '__main__': unittest.main()
