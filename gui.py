import tkinter as tk
from idlelib.WidgetRedirector import WidgetRedirector
import game

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

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.GUI = tk.Frame(width = self.WIDTH, height = self.HEIGHT) 
        self.GUI.pack(side="top", fill="both", expand=True)
        
        """ Initializing text display area. """
        self.TextDisplay = ReadOnlyText(self.GUI)
        self.TextDisplay.pack(side="top", fill="both", expand=1)

        """ Intializing text entry area. """
        self.Entry = tk.Entry(self.GUI)
        self.Entry.pack(fill=tk.X)
        self.Entry.bind('<Return>', self._enter_text) 
        self.Entry.focus_set()

        """ Initializing buttons. """
        # Implement commands.
        self.Quit_Button = tk.Button(self.GUI, text="Quit", command=self._quit_button)
        self.Inventory_Button = tk.Button(self.GUI, text="Inventory", command=self._inv_button)

        self.Quit_Button.pack(side="left", expand=1, fill=tk.X)
        self.Inventory_Button.pack(side="left", expand=1, fill=tk.X)

        self.G = game.test_init()
        self.G.main()
        self._print_text(self.G.gets())


    def _call_game(self, entered_text):
        print("## Calling game. ##")
        if entered_text in ['q', 'quit', 'exit']:
            print('Quitting.')
            self.destroy()
        else:
            self.G.prompt_exe(entered_text)
            received_text = self.G.gets()
            print("Not quitting.")
            #print(received_text)
            self._print_text(received_text)

    def _print_text(self, print_me):
        self._wipe_display()
        self.TextDisplay.insert(tk.END, print_me)

    def _text_prettifier(self, received_text):
        return None

    def _enter_text(self, event, entered_text = None):
        print("## Entering enter text. ##")
        if entered_text == None: 
            entered_text = self.Entry.get()
        print("entered_text = {0}".format(entered_text))
        print("Entry.get() = {0}".format(self.Entry.get()))
        self._wipe_entry()
        self._call_game(entered_text)  

    def _quit_button(self):
        self._enter_text(tk.Event(), 'quit')

    def _inv_button(self):
        self._enter_text(tk.Event(), 'inv')

    def _wipe_entry(self):
        print("Wiping entry.")
        self.Entry.delete("0", tk.END)

    def _wipe_display(self):
        print("Wiping display.")
        self.TextDisplay.delete("0.0", tk.END)

if __name__ == "__main__":
    root = GUI_Holder()
    root.mainloop()
