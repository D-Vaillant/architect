""" engine.py:
        This is where I begin the split between engine and module. """

class Engine():
    def __init__(self, initial_module, ):
        self.activeModule = initial_module if initial_module.is_module else None
        self.activeModule.activate(self)

class Module():
    def __init__(self, rdata = None, idata = None, mdata = None):
        self.rooms = ({id_:Room(data) for id_, data in rdata.items()} if rdata
                           else {})
        self.items = ({id_:Item(data) for id_, data in idata.items()} if idata
                            else {})
        self.static_output = ''
        self.dynamic_output = ''

    def activate(self, engine):
        assert isinstance(engine, Engine)
        self.E = engine

    def process_input(self, string):
        pass
