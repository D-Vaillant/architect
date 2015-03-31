from rooms import processor, Room
from copy import deepcopy as dc

#class Navigator():
    #Abstraction of Room_Navigator, for use in other projects.
    
class Room_Navigator():
    entry_msg = 'Navigator started. Type \'q\' to quit.\n'
    entry_menu = 'r: Rooms.\n'
    entry2_msgs =  {'r': 'Type a number to open up more details,' + \
                    ' ` for previous page and - for next page.\n' + \
                    '\'m\' returns to this screen.\n' + \
                    'Pages: ' }
    entry2_codes = {'r':'room'}

    def __init__(self, d):
        self.pages = self.dict_to_pages(d)
        self.default_loc = ['r',[None,None]]
        self.loc = dc(self.default_loc)
        self.menu_0 = {'r'}
        self.menu_r = set()        
        for x in self.pages.keys():
            self.menu_r.add(x)
        self.page_count = max(self.menu_r)+1
        
    def dict_to_pages(self, d):
        i = -1
        j = -1
        f = dict()
        f[0] = {}
        for k in d:
            i = (i+1)%10
            if i == 0:
                j += 1
                f[j] = {}
            f[j][i] = k

        return f

    def page_displayer(self, page_num):
        for x in range(max(self.pages[page_num].keys())+1):
            print(str(x) + ' ' + self.pages[page_num][x])
        return


    def room_displayer(self, pg_rn):
        page_num, room_num = pg_rn
        print(self.pages[page_num][room_num])

    def prompt_exe(self, chr):
        if chr == 'q': return
        if chr.isdigit(): chr = int(chr)
        
        if self.loc[0] == None:
            if chr in self.menu_0: 
                self.loc[0] = chr
                print('Entering {} menu.'.format(entry2_codes[chr]))
            else:
                print('Invalid entry.')
                self.loc[0] = '!'
                return
        if self.loc[0] == 'r': 
            if self.loc[1][0] == None:
                if chr == '':
                    return
                if chr in self.menu_r:
                    self.loc[1][0] = chr
                else:
                    print('Invalid entry.')
                    self.loc[1][0] = '!'
                    return
            elif self.loc[1][0] in self.menu_r:
                if chr == '`':
                    self.loc[1][0] = (self.loc[1][0]-1) % self.page_count
                    print('Moving to page ' + str(self.loc[1][0]) + '.')
                    return
                elif chr == '-':
                    self.loc[1][0] = (self.loc[1][0]+1) % self.page_count
                    print('Moving to page ' + str(self.loc[1][0]) + '.')
                    return
                elif chr == 'm':
                    self.loc[1][0] = None
                    print('Returning to room menu.')
                    return
                elif chr in self.pages[self.loc[1][0]].keys():
                    self.loc[1][1] = chr
                    return
                else:
                    self.loc[1][1] = '!'
                    print('Invalid entry.')
                    return
        return
        
    def loc_exe(self):
        if self.loc[0] == None:
            print(self.entry_menu)
            return
        if self.loc[0] == '!':                   
            self.loc[0] = None
            return
        if self.loc[0] == 'r': 
            if self.loc[1][0] == None:
                print(self.entry2_msgs['r'] + str(self.menu_r)[1:-1])                   
                return
            elif self.loc[1][0] == '!':
                self.loc[1][0] == None
                return
            else:
                if self.loc[1][1] == None:
                    self.page_displayer(self.loc[1][0])
                    return
                elif self.loc[1][1] == '!':
                    self.loc[1][1] = None
                    return
                elif self.loc[1][1] in self.pages[self.loc[1][0]].keys():
                    print(self.room_displayer(self.loc[1]))
                    return
                return
            return
        return
                    
                    

    def main(self):
        print(self.entry_msg)
        prompt = ''
        while(prompt != 'q'):
            self.loc_exe()
            x = input('> ')
            prompt = x[0].lower() if x != '' else '' 
            self.prompt_exe(prompt)
        self.loc = dc(self.default_loc)
        prompt = ''
        return
