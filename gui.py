import tkinter as tk
from idlelib.WidgetRedirector import WidgetRedirector
import game

V = False

# Credit to tkinter.unpythonic.net/wiki/ReadOnlyText.
class ReadOnlyText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = \
            self.redirector.register("insert", lambda *args, **kw: "break")
        self.delete = \
            self.redirector.register("delete", lambda *args, **kw: "break")

class GUI_Holder(tk.Tk):
    WIDTH = 150 
    HEIGHT = 30

    def __init__(self, game, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.GUI = tk.Frame(width = self.WIDTH, height = self.HEIGHT) 
        self.GUI.pack(side="top", fill="both", expand=True)
        
        """ Initializing text display area. """
        self.TextDisplay = ReadOnlyText(self.GUI)
        self.TextDisplay.pack(side="top", fill="both", expand=1)
        self.TextDisplay.config(wrap=tk.WORD)

        """ Intializing text entry area. """
        self.Entry = tk.Entry(self.GUI)
        self.Entry.pack(fill=tk.X)
        self.Entry.bind('<Return>', self._enter_text) 
        self.Entry.focus_set()

        """ Initializing buttons. """
        # Implement commands.
        self.Quit_Button = tk.Button(self.GUI, text="Quit", 
                                     command=self._quit_button)
        self.Inventory_Button = tk.Button(self.GUI, text="Inventory",
                                          command=self._inv_button)

        self.Quit_Button.pack(side="left", expand=1, fill=tk.X)
        self.Inventory_Button.pack(side="left", expand=1, fill=tk.X)

        self.G = game
        self.G.main()
        self._print_text(self.G.gets())


    def _call_game(self, entered_text):
        """ Interface between the GUI and the Game class. 
        
            Catches quit messages and terminates the GUI before calling the
            Game class. Otherwise faciliates passing and receiving
            information. """
            
        print("## Calling game. ##")
        if entered_text in ['q', 'quit', 'exit']:
            if V: print('Quitting.')
            self.destroy()
        else:
            self.G.prompt_exe(entered_text)
            received_text = self.G.gets()
            if V: print("Not quitting.")
            #print(received_text)
            self._print_text(received_text)

    def _print_text(self, print_me):
        """ Faciliates printing text to the Text widget. """
        self._wipe_display()
        self.TextDisplay.insert(tk.END, print_me)

    def _text_prettifier(self, received_text):
        """ Used to bold some relevant words via tagging.
    
        I do not understand how tagging works so this is unimplemented. """
        return None

    def _enter_text(self, event, entered_text = None):
        if V: print("## Entering enter text. ##")
        if entered_text == None: 
            entered_text = self.Entry.get()
        if V: print("entered_text = {0}".format(entered_text))
        if V: print("Entry.get() = {0}".format(self.Entry.get()))
        self._wipe_entry()
        self._call_game(entered_text)  

    def _quit_button(self):
        self._enter_text(tk.Event(), 'quit')

    def _inv_button(self):
        self._enter_text(tk.Event(), 'inv')

    def _wipe_entry(self):
        if V: print("Wiping entry.")
        self.Entry.delete("0", tk.END)

    def _wipe_display(self):
        if V: print("Wiping display.")
        self.TextDisplay.delete("0.0", tk.END)
    
if __name__ == "__main__":
    G = game.gui_init()
    root = GUI_Holder(G)
    root.mainloop()
