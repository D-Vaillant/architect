from rooms import processor, Room

class Room_Navigator():
    entry_msg = 'Room navigator started. Type \'q\' to quit.\n'
    entry_menu = 'r: Rooms.\n'
    room_entry_msg = 'Opening room display. \n' + \
                     'Type the number to open up more details,' + \
                     ' ` for previous page and - for next page.\n'

    def __init__(self, d):
        self.pages = self.dict_to_pages(d)
        self.loc = ['r',[None,None]]
        self.menu_0 = {'r'}
        
    def dict_to_pages(self, d):
        i = -1
        j = -1
        f = dict()
        f[0] = {}
        for k in d:
            i = (i+1)%10
            if i == 0: j += 1
            f[j][i] = k
        return f

    def page_displayer(self, page_num):
        for x in range(max(self.pages[page_num].keys())+1):
            print(str(x) + ' ' + self.pages[page_num][x] + '\n')
        return


    def room_displayer(self, page_num, room_num):
        print(self.pages[page_num][room_num])

    def prompt_exe(self, char):
        if (char in {'', ' ', '\n'}): return
        if self.loc[0] == None:
            if char in self.menu_0: 
                self.loc[0] = char
            else: print('Incorrect entry.')
        if self.loc[0] == 'r': 
            if char == 'p':
                self.page_displayer(0)
            elif char == '`':
                self.loc[1] = (self.loc[1]-1) % self.page_count
                print('Moving to page ' + self.loc[1])
                return
            elif char == '-':
                self.loc[1] = (self.loc[1]+1) % self.page_count
                print('Moving to page ' + self.loc[1])
                return
            elif char in range(max(self.pages\
            + 1):
                print('Moving to room ' + char)
                self.page_displayer(char)
                return
            else:
                print('Invalid entry.')
                return
        return
        
    def loc_exe(self):
        if self.loc[0] == None:
        
        if self.loc[0] == 'r': 
                print(self.room_entry_msg)
                self.page_displayer(0)
            

    def main(self):
        print(self.entry_msg)
        #print(self.entry_menu)
        prompt = ''
        while(prompt != 'q'):
            self.loc_exe()
            x = input('> ')
            prompt = x[0].lower() if x != '' else '' 
            self.prompt_exe(prompt)

        return
