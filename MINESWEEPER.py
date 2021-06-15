import random
from tkinter import *
from tkinter import messagebox

root = Tk()

class MinesweeperGrid(Frame):
    def __init__(self,master, width, height, numBombs):
        '''MinesweeperGrid(master)
        creates a new blank Minesweeper grid'''
        # initialize a new Frame and put it on grid
        Frame.__init__(self,master,bg='black')
        self.grid()
        #set up some attributes
        self.height = height
        self.width = width
        self.numBombs = numBombs
        self.cellDict = {} # set up dictionary for cells
        for row in range(height):
            for column in range(width):
                coord = (row,column) #key is cell coord
                self.cellDict[coord] = MinesweeperCell(self,coord) #value is object of type MinesweeperCell
                self.cellDict[coord].grid(row=row,column=column)
        #set up the label that will keep track of how many flags have been put
        self.flagLabel = Label(width=10,height=2,bg='black',\
                                  text = self.numBombs,font = ('Helvetica', 16), bd=8,relief=GROOVE)
        self.flagLabel.grid(row = self.width, column = 0, columnspan = 5)
        self.flagLabel['fg'] = 'white'
        
        self.bombList = []
        for i in range(numBombs):
            num1 = random.randint(0, height - 1)
            num2 = random.randint(0, width - 1)
            bombCoord = (num1, num2)     #set a random coord for the bomb
            if bombCoord not in self.bombList:     #if this coord in new,
                self.bombList.append(bombCoord)        #put it in the list
            else:      #if the coord is already a bomb
                while bombCoord in self.bombList:  #while the new coord is in the list,
                    num1 = random.randint(0, height - 1)
                    num2 = random.randint(0, width - 1)
                    bombCoord = (num1, num2)            #get new coords
                    if bombCoord not in self.bombList:   #when you get a new coord,
                        self.bombList.append(bombCoord)      #put it in bombList
                        break

        self.set_cell_attributes()

    def set_cell_attributes(self):
        for i in self.bombList:
            self.cellDict[i].bomb = True
        for cellCoord in self.cellDict:
            self.create_neighborCellList(cellCoord)

    def create_neighborCellList(self, cellCoord):
        tempNeighborList = []
        a = cellCoord[0]
        i = cellCoord[1]
        #all 8 poosible coords that can surround the cell
        tempNeighborList.extend([(a-1, i-1),(a, i-1), (a+1, i-1),\
                                 (a-1, i),(a+1, i), (a-1, i+1), (a, i+1),(a+1, i+1)])
        self.neighborCellList = []
        for i in tempNeighborList:
            if i[0]<0 or i[1]<0 or i[0]>=self.height or i[1]>=self.width:  #check which ones are valid
                pass
            else:
                self.neighborCellList.append(self.cellDict[i])
        count = 0
        for i in self.neighborCellList:
            if i.bomb == True:
                count += 1
        self.cellDict[cellCoord].number = count

##        if self.cellDict[cellCoord].bomb == True:
##            self.cellDict[cellCoord]['text'] = str(count) + "X"
##        else:
##            self.cellDict[cellCoord]['text'] = str(count)

        return self.neighborCellList
              

class MinesweeperCell(Label):
    def __init__(self, master, coord):
        Label.__init__(self,master,width=4,height=2,bg='white',text = "",font = ('Helvetica', 16), bd=8,relief=RAISED)
        self.coord = coord   #(row,column) coordinate tuple
        self.number = 0      # number of bombs around it
        self.numBombs = self.master.numBombs
        self.total = self.master.width * self.master.height
        self.winCount = 0    # number of squares that have been correctly identified as a bomb or not
        self.master = master
        self.click = True    #starts "clickable"
        self.bomb = False    #starts without a bomb
        self.flag = False    #starts without a flag
        self.highlighted = False  # starts unhighlighted
        # set up listeners
        self.bind('<Button-1>',self.play_minesweeper)
        self.bind('<Button-3>',self.bomb_check)

    def play_minesweeper(self, event):
        colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
        if self.click == True and self.highlighted == False:
            self.highlight()
            self['relief'] = SUNKEN
            if self.bomb == True:
                self['text'] = '*'
                messagebox.showerror('KABOOM! You lose.',parent=self)
                for i in self.master.cellDict:
                    self.master.cellDict[i].set_bomb()       #if the cell is a bomb, open it up
                    self.master.cellDict[i].click = False    #now, none of the cells can be clicked
            else:
                if self.number != 0:
                    self['fg'] = colormap[self.number]
                    self['text'] = self.number
                else:
                    self.master.create_neighborCellList(self.coord)
                    for i in self.master.neighborCellList:
                        i.highlight()
                        i['relief'] = SUNKEN
                        i['text'] = str(i.number)                    
        #check for a win at the end of every turn
        self.win()

    def bomb_check(self, event):
        if self.click == True and self.highlighted == False and self.master.numBombs != 0:
            if self.flag == False:   #if it doesn't have an flag
                self['text'] = '*'
                self.master.numBombs -= 1
                
            else:
                self['text'] = ''
                self.master.numBombs += 1
        self.master.flagLabel['text'] = self.master.numBombs
        self.flag = not self.flag
        self.win()

    def win(self):
        self.winCount = 0
        for i in self.master.cellDict:
            if self.master.cellDict[i].bomb == True: #it is a bomb
                if self.master.cellDict[i]['text'] == '*': #if it has been flagged
                    self.winCount += 1
            else: #if it is not a bomb
                if self.master.cellDict[i].highlighted == True: #if it has been clicked
                    self.winCount += 1

        if self.winCount == self.total:
            messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)

    def highlight(self):
        '''MinesweeperCell.highlight()
        highlights the cell (changes background to grey)'''
        self.highlighted = True
        self['bg'] = 'lightgrey'

    def set_bomb(self):
        if self.bomb == True:
            self['bg'] = 'red'
            self['text'] = '*'

frame = Frame(root)
test = MinesweeperGrid(root, 7, 7, 10)
frame.grid()
root.mainloop()
