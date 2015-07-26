import unittest
import tempfile
from collections import OrderedDict
from file_management import File_Processor
from json_reader import InfoCollector
from game import *

""" To do: revamp Action dictionary. """
""" TESTS TO WRITE:
        Verify that Rooms only hold actual item IDs.
        Game logic stuff.
        """

def stringMaker_A(D):
    """ Used to turn Room and Thing info dicts into byte strings. """
    outer = ''
    for key, value in D.items():
        outer += "#IDEN {}\n".format(key)
        for type, entry in value.items():
            if type != 'IDEN':
                outer += "#{0} {1}\n".format(type, entry)
    return outer.encode('UTF-8')
    
def stringMaker_B(D):
    outer = ''
    for key, value in D.items():
        outer += "#{}\n".format(key)
        for first, second in value.items():
            if first == 0:
                outer += "0/{}\n".format(second)
            elif first in [1,2]:
                for cond, bp_code in second.items():
                    if first == 2: cond = cond[0].split('&')
                    outer += "{0}/{1}\n".format(cond, bp_code)
        outer += "\n"
    ##print(outer)
    return outer.encode('UTF-8')

"""
class FP_Core(unittest.TestCase):
    def setUp(self):
        self.r_dict = {'initial':
                            {'DESC':"Sick room bro",
                             'IDEN':"initial",
                             'NAME':"Kickin' pad",
                             'HOLD':"",},
                       'second':
                            {'NAME':"Cool Beans",
                             'IDEN':"second",
                             'HOLD':"bean_bag | rock",
                             'DESC':"Too Cool",},
                      }
        self.t_dict = {'bean_bag':
                            {'IDEN':"bean_bag",
                             'GRND':"It's just sitting there.",
                             'ALIA':"bean bag",
                             'NAME':"bean bag",
                             'PROP':"item",
                             'EXMN':"It smells skunky.",},
                       'rock':
                            {'IDEN':"rock",
                             'ALIA':"rock",
                             'NAME':"rock",
                             'PROP':"prop",
                             'GRND':"It's rocking out.",},
                        'vinyl_record':
                            {'IDEN':"vinyl_record",
                             'ALIA':"vinyl record",
                             'GRND':"There's a stylish record here.",
                             'PROP':"prop",
                             'NAME':"vinyl record",},
                      }
        self.a_dict = {'sit':
                            {0: 'sys.!On what?',
                             1: OrderedDict([(('bean_bag',),'sys.!Comfy.'),
                                             (('rock',),'sys.!Why?'),
                                             (('',),"sys.!That won't work.")]),
                             2: OrderedDict(),
                                             },
                        'throw':
                            {0: 'sys.!Throw what at what?',
                             1: OrderedDict([(('',),"sys.!Throw that at what?")]),
                             2: OrderedDict([((('rock',),('vinyl_record',)),
                                                       "sys.!Clang!"),
                                             ((('',),('',)),"sys.!Bop.")]),
                             'P2':"at"},
                       }
        self.tf = tempfile.TemporaryFile()
        self.tf.write(b"// This is a comment.\n"
                      b"\n")
                      
                      
        self.tf.write(b"~R\n" + stringMaker_A(self.r_dict))
        self.tf.write(b"~T\n" + stringMaker_A(self.t_dict))
        ##self.tf.write(b"~A\n" + stringMaker_B(self.a_dict))
        self.tf.seek(0)
       
        self.fp = File_Processor(self.tf, ut = True)
        
       
    def tearDown(self):
        self.tf.close()

class FP_Integrity_Tester(FP_Core):
    def test_rooms(self):
        self.assertDictEqual(self.fp.room_info, self.r_dict)
            
    def test_objects(self):
        self.assertDictEqual(self.fp.thing_info, self.t_dict)
        
    def test_actions(self):
        self.assertDictEqual(self.fp.action_info, self.a_dict)
        
    def test_links(self):
        return
 
class FP_Soundness_Tester(FP_Core):
    pass
"""

class JR_Tester(unittest.TestCase):
    def setUp(self):
        self.Reader = InfoCollector()
        self.Reader.main()

    def test_rooms(self):
        roomDict = Room.room_processor(self.Reader.room_info)
        for r in roomDict:
            self.subtest_room(self.Reader.room_info[r], roomDict[r])

    def subtest_room(self, roomJR, roomOBJ):
        for key, r_var in roomOBJ.codes.items():
                if key in roomJR:
                    self.assertEqual(getattr(roomOBJ, r_var), roomJR[key])
                else:
                    if key == "links":
                        self.assertEqual(roomOBJ.links == [None]*4)
                    else:
                        self.assertEqual(getattr(roomOBJ, r_var), '')
                    
    def test_actions(self):
        actDict = Action.action_processor(self.Reader.action_info)
        for a in actDict:
            self.subtest_action(self.Reader.action_info[a], actDict[a])
        
    def subtest_action(self, actionJR, actionOBJ):
        grabObjVar = lambda q: getattr(actionOBJ, q)

        for key, i_var in actionOBJ.codes.items():
            if key in actionJR:
                if key not in {"1", "2"}: 
                    self.assertEqual(grabObjVar(i_var), actionJR[key])
                else:
                    pass
            else:
                if key in {"1", "2"}:
                    self.assertEqual(grabObjVar(i_var), OrderedDict())
                else:
                    self.assertEqual(grabObjVar(i_var), '')
        
    
    def test_items(self):
        itemDict = Item.item_processor(self.Reader.action_info)
        for i in itemDict:
            ##self.subtest_item(self.Reader.item_info[i], itemDict[i])
            pass

if __name__ == '__main__': unittest.main()
