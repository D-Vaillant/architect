""" engine.py:
        This is where I begin the split between engine and module. """

class Engine():
    def __init__(self, initial_module, ):
        self.am = initial_module if initial_module.is_module else None
        self.am.activate(self)

# ---------------- Utility Functions ------------------------------------------
    def _local(self):
        """ Returns a list of Items near the player. """
        return self.am.loc.holding+list(self.am.pc.inventory)

    def _IDtoRoom(self, id_):
        """ Returns a Room instance R such that R.id = id. """
        try:
            return self.am.rooms[id_]
        except KeyError:
            raise KeyError("No room with ID {}.".format(id_))

    # TODO: Write a test for this.
    def _scopeGetter(self, scope):
        """ Takes a scope and returns a corresponding list of Items.

            scope parameters:
                held:       in inventory
                held.bag:   in inventory.holding[bag]
                around:     in self.loc
                local:      in self.loc or inventory
                [room_ids]: in one of the given rooms
                global:     in anything
        """
        val_list = []
        if scope == "held":
            val_list = list(self.am.pc.inventory)
        elif "held." in scope:
            try:
                val_list = list(self.am.pc.inventory.holding[scope[5:]])
            except KeyError:
                raise KeyError("Tried to access {}, but no bag exists with " +
                               "that name.".format(scope[5:]))
        elif scope == "around":
            val_list = self.loc.holding
        elif scope == "local":
            val_list = self.loc.holding+list(self.am.pc.inventory)
        elif scope == "global":
            val_list = list(self.items.values)
        else:
            raise InvalidBranchError("A bad scope was specified.") 
        return val_list

    def _IDtoItem(self, id, scope="global"):
        """ Returns an Item instance W such that W.id = id. """
        try:
            return self.items[id]
        except KeyError:
            raise NameError("No item with ID {}.".format(id))

    def _itemNametoItem(self, item_name, scope="local"):
        """ Gets an Item from its name or nickname.

            By default, only looks for Items in the local scope.
            If no item found, puts the appropriate error message and
                returns None.
        """
        search_arr = [x for x in self._scopeGetter(scope)
                              if (item_name == x.name or
                                  item_name == x.nickname)]

        out = None
        if len(search_arr) == 1:
            out = search_arr[0]
        elif len(search_arr):
            self.puts(self.ERROR["ambiguity"])
        else:
            self.puts(self.ERROR["item_not_found"])
        return out


# ----------------- Public "Doing" Functions ----------------------------------
    def add(self, item, container, target = None):
        """ Adds an Item to a container. """
        item = self._IDtoItem(item)
        if container == '_':
            container = self.am.pc.inventory
            container.add(item, target)
        else:
            container = self._IDtoRoom(container)
            container.add(item)

    def remove(self, item, container, target = None):
        """ Removes an Item from a container. """
        item = self._IDtoItem(item)
        if container == '_':
            container = self.am.pc.inventory
            container.remove(item, target)
        else:
            container = self._IDtoRoom(container)
            container.remove(item)

    def link(self, source, dir, dest):
        dir = self.cardinals[dir.lower()]
        source = self._IDtoRoom(source)
        dest = self._IDtoRoom(dest)

        source.link(dest, dir, self.is_euclidean)

    def move(self, moved_item, source, target):
        """ Removes moved_item from source and adds it to target. """
        if moved_item in source:
            try:
                target.add(moved_item)
            except AttributeError:
                raise AttributeError("Target lacks add() method.")
            try:
                source.remove(moved_item)
            except AttributeError:
                raise AttributeError("Source lacks remove() method.")
        else:
            raise AttributeError("Item not in source.")

    def addProperty(self, item, property):
        item = self._IDtoItem(item)
        item.setProperty(property)

    def removeProperty(self, item, property):
        item = self._IDtoItem(item)
        item.setProperty(property, False)

    def changeItem(self, item, attr, text):
        item = self._IDtoItem(item)
        if '_desc' in attr:
            print("WARNING: You should be calling changeDescription.")
            return
        try:
            setattr(item, attr, text)
        except AttributeError:
            raise AttributeError("%s is not an item attribute."%attr)

    def changeDescription(self, object, type, index=0, text=''):
        pass

    def changeRoom(self, room, attr, text):
        room = self._IDtoRoom(room)
        try:
            setattr(room, attr, text)
        except AttributeError:
            raise AttributeError("%s is not a room attribute."%attr)

    # NOTE: What the hell was this for?
    def changeInv(self, bag, attr, text):
        inv = self.am.pc.inventory()
        bag = inv.structuredHolding[bag]
        # TODO: Implement "add bag", "remove bag", and "change bag limits".
        return

    def err(self, msg):
        try:
            puts(Game.ACT_MSGS[msg])
        except KeyError:
            puts(Game.ACT_MSGS[0])

class Module():
    def __init__(self, rdata = None, idata = None, adata = None, mdata = None):
        self.rooms = ({id_:Room(data) for id_, data in rdata.items()} if rdata
                            else {})
        self.items = ({id_:Item(data) for id_, data in idata.items()} if idata
                            else {})

        self.pc = Actor(id = 'pc', adata.get('pc'))
        self.actors = ({id_:Actor(data) for id_, data in adata.items() if adata
                            else {})
                            
        self.static_output = ''
        self.dynamic_output = ''

    def activate(self, engine):
        assert isinstance(engine, Engine)
        self.E = engine

    def process_input(self, string):
        pass
