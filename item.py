
__author__ = "David Vaillant"

class Item():
    """ Class used to represent items or props.
        ITEMS: Can be placed in player inventory and used from there.
        PROPS: Cannot be moved from their position in a room. """
    codes = {
        'id':'id',
        'name':'name',
        'nick':'nickname',
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
        self.properties = set(t('property') or {})
        self.weight = t('weight') or 0
        self.isProp = ('static' in self.properties)  
        
        self.examine_desc = t('examine') or ''
        self.ground_desc = t('ground') or ''
        
        self.on_acquire = t('acquire') or 'pass'

    def setProperty(self, property_input, isAdding = True):
        error = False
        
        if isAdding:
            self.properties.add(property_input)
        else:
            try:
                self.properties.remove(property_input)
            except KeyError: error = True
        return error #if setProperty: error handle.

    def setDescription(self, type, text = ""):
        error = False
        
        if hasattr(self, type+"_desc"):
            setattr(self, type+"_desc", text)
        else:
            error = True #if setDescription: error handle.
        return error

    ### NOTE: This could probably be moved elsewhere. ###
    ### Related: __str__ method for Items. ###
    @staticmethod
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
