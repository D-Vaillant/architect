
__author__ = "David Vaillant"

class Item():
    """ Class used to represent items or props.
        ITEMS: Can be placed in player inventory and used from there.
        PROPS: Cannot be moved from their position in a room. """
    codes = {
        'id':'id',
        'name':'name',
        'nick':'nick',
        'examine':'examine_desc',
        'acquire':'on_acquire',
        'ground':'ground_desc',
        'property':'properties',
        'weight':'weight'
        }


    def __init__(self, itemD):
        """ Populates attributes using a Item info dictionary. """
        t = lambda s: itemD[s] if s in itemD.keys() else None
        
        self.id = t('id')
        self.name = t('name')
        
        self.nickname = t('nick') or t('name') or 'item'                
        self.properties = set(t('property') or [])
        self.weight = t('weight') or 0
        self.isProp = ('static' in self.properties)  
        
        self.examine_desc = t('examine') or ''
        self.ground_desc = t('ground') or ''
        
        self.on_acquire = t('acquire') or 'pass'

    def setProperty(self, property_input, isAdding = True):
        if isAdding:
            self.properties.add(property_input)
        else:
            try:
                self.properties.remove(property_input)
            except KeyError: return True 
        return False #if setProperty: error handle.

    def setDescription(self, type, text = ""):
        try:
            self.setattr(type, text)
            return False
        except AttributeError:
            return True


    # NOTE: Need to figure out how to do attribute changes. 
    """
    def safety(self, attributeType, source):
        # Used when changing Item attributes.
        if type(source) == str: valve = '' 
        elif type(source) == dict: valve = {}

        if attributeType in source.keys():
           return x
        else:
            return valve
    """
    
    def item_printer(holds):
        out_str = ''
        if holds:
            for x in holds:
                if x.ground_desc == 'pass':
                    pass
                elif x.ground_desc == 'default':
                    out_str = out_str + "\nThere is a " + x.name + " here."
                else:
                    out_str = out_str + "\n" + x.ground_desc
            return out_str
        else: return ''    
    
    @staticmethod
    def item_processor(item_dict):
        """ Returns a Item class dictionary using a Item info dictionary. """
        items = {}
        ##item_dict = item_fixer(item_dict)
         
        # iterates over 
        ##for t in item_dict.values():
        ##    x = Item(t)
        ##    key = x.id
        ##    items[key] = x
        return {x:Item(item_dict[x]) for x in item_dict}
        
    """
    def item_fixer(input_dict):
        sourceList = obj_reader(fileIn) if type(fileIn) is str else fileIn
        for ele in input_dict:
            for code in Item.codes:
                if code[1:] not in ele.keys():
                    ele[code[1:]] = {} if code == '#AC' \
                                    else 'pass'
        return fixed_dict
    """
