from rooms import processor, Room

class Room_Navigator():
    entry_msg = 'Room navigator started. Type \'q\' to quit.\n')
    room_entry_msg = 'Opening room display. \n' +
                     'Type the number to open up more details,'+
                     ' ` for previous page and - for next page.\n')

    def __init__(self, d):
        self.pages = dict_to_pages(d)
        self.loc = (0,None)

    def dict_to_pages(d):
        i, j = 0
        f = dict()
        f[0] = {}
        for k in d:
            f[j][i] = k
            i = (i+1)%10
            if i == 0: j += 1
        return f

    def page_displayer(page_num):
        for x in range(self.pages[page_num]):
           print(x + self.pages[page_num][x] + '\n')



    def room_displayer(page_num, room_num):
        print(self.pages[page_num][room_num])

    def prompt_exe(char):
        if (char in {'', ' ', '\n'}: return
        if loc[0] == 0:
            if char == 'r': 
                loc = ('r', 0)
                page_displayer(0)
            else: print('Incorrect entry.')
        if loc[0] == 'r':
        return

    def main():
        entry_msg = 'Room navigator started.\n')
        print(entry_msg)
        prompt = ''
        while(prompt != 'q'):
            self.prompt_exe(prompt)
            prompt = input('> ')[0].lower()
        return
