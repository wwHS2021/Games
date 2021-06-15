from tkinter import *

class CheckerCell(Canvas):
    def __init__(self, master, color, r, c):
        Canvas.__init__(self,master,width=50,height=50,bg=color, highlightbackground='black')
        self.grid(row=r, column=c)
        self.hasCircle = False #starts out without a circle
        self.circleColor = None #starts out without a circle, so there is no color
        self.coord = (r, c)  #circle coord on grid
        self.color = color
        self.bind('<Button>',self.get_click)
        self.master = master
        self.jumpLeft = False
        self.jumpRight = False
        self.checkBoard = self.master.checkerBoard
        self.dict = self.master.cellsDict
        self.moveList = []
        self.isJumped = False
        
    def get_click(self, event):
        '''CheckerCell.get_click gets a click
            and acts accordingly based on what
            was clicked
        '''
        if len(self.checkBoard.jumpMoveList) != 0 :         
            if self.coord in self.checkBoard.jumpMoveList :
                self.move_cell()
            else:
                return
                
    #if it has a circle and is the right color
        if self.hasCircle == True and \
           self.circleColor == self.checkBoard.colorList[self.checkBoard.currentPlayer]:
            self.checkBoard.cellClicked = self.coord
            self.master.change_highlight(self)
            if self.circleColor == 'white':
                self.moveList = self.get_possible_moves(-1, self.coord[0]>1, self.coord[0]>0)
            else:
                self.moveList = self.get_possible_moves(1, self.coord[0]<6, self.coord[0]<7)
            print(self.moveList)
    #clicking on the wrong person's circle
        elif self.hasCircle == True and self.checkBoard.cellClicked != 0 and \
             self.circleColor != self.checkBoard.colorList[self.checkBoard.currentPlayer]:
            self.dict[self.checkBoard.cellClicked]['highlightbackground'] = 'SystemButtonFace'
            self.checkBoard.cellClicked = 0
    #clicked a good circle
        elif self.hasCircle == False and self.color != 'blanched almond' and \
             self.checkBoard.cellClicked != 0 and \
             self.coord in self.dict[self.checkBoard.cellClicked].moveList:
            self.move_cell()
            
    def move_cell(self):
            self.master.change_highlight(self)        
            self.make_oval(self.dict[self.checkBoard.cellClicked].circleColor)  #make a circle of the clicked cell's color
            self.dict[self.checkBoard.cellClicked].delete_oval()
            
            win = self.master.check_and_act_for_win(self.dict[self.checkBoard.cellClicked], self)  #check for a win
            if win == 1:
                self.master.end_game()
            else:
                #change the player
                self.checkBoard.currentPlayer = 1 - self.checkBoard.currentPlayer
                self.master.change_turn_color()
            self.cell_jump()
            self.checkBoard.cellClicked = 0
            if self.circleColor == 'white':
                self.check_for_continue_jump('white')
            else:
                self.check_for_continue_jump('red')

    def check_for_continue_jump(self, color):
        if(self.isJumped == False) :
            return
        if self.circleColor == 'white':
            self.checkBoard.jumpMoveList = self.get_possible_moves_for_jump(-1, self.coord[0]>1, self.coord[0]>0)
        else:
            self.checkBoard.jumpMoveList = self.get_possible_moves_for_jump(1, self.coord[0]<6, self.coord[0]<7)
        if len(self.checkBoard.jumpMoveList) != 0:
            self.master.continueJump['text']='Must continue jump'
            self.checkBoard.cellClicked = self.coord
            self.checkBoard.currentPlayer = 1 - self.checkBoard.currentPlayer
            self.master.change_turn_color()

    def get_possible_moves_for_jump(self, multiplier, cond1, cond2):
        '''CheckerCell.get_possible_moves_for_jump
            returns a list of the possible
            moves a checker can make
            '''
        x = self.coord[0]
        y = self.coord[1]
        possibleMovesList =  []
        #all possible moves are added to possibleMovesList
        if cond1 and y > 1: #checking if a white or red cell can jump to the left
            diagonalLeft = (x+2*multiplier, y-2)
            jumpCell = (x+1*multiplier, y-1)
            if self.dict[jumpCell].hasCircle == True and \
               self.dict[jumpCell].circleColor != self.circleColor \
               and self.dict[diagonalLeft].hasCircle == False:
                print('jump to the left')
                possibleMovesList.append(diagonalLeft)
                self.jumpLeft = True
        if cond1 and y < 6: #checking if a white or red cell can jump to the right
            diagonalRight = (x+2*multiplier, y+2)
            jumpCell = (x+1*multiplier, y+1)
            if self.dict[jumpCell].hasCircle == True and \
               self.dict[jumpCell].circleColor != self.circleColor \
               and self.dict[diagonalRight].hasCircle == False:
                print('jump to the right')
                possibleMovesList.append(diagonalRight)
                self.jumpRight = True   
        return possibleMovesList
    
    def cell_jump(self):
        '''CheckerCell.cell_jump(self)
            If a cell can jump and it did jump,
            this method removes the circle
            in the middle
        '''
        self.isJumped = False
        self.master.continueJump['text'] = ''
        if self.dict[self.checkBoard.cellClicked].circleColor == 'white':
            if self.coord[0] == self.checkBoard.cellClicked[0] - 2 and \
               self.coord[1] == self.checkBoard.cellClicked[1] - 2:
                #if it jumped a cell to the left
                jumpCoord = (self.coord[0]+1, self.coord[1]+1) #the cell jumped
                self.dict[jumpCoord].delete_oval()
                self.isJumped = True
            elif self.coord[0] == self.checkBoard.cellClicked[0] - 2 and \
               self.coord[1] == self.checkBoard.cellClicked[1] + 2:
                #if it jumped a cell to the right
                jumpCoord = (self.coord[0]+1, self.coord[1]-1) #the cell jumped
                self.dict[jumpCoord].delete_oval()
                self.isJumped = True                
        else:
            if self.coord[0] == self.checkBoard.cellClicked[0] + 2 and \
               self.coord[1] == self.checkBoard.cellClicked[1] + 2:
                #if it jumped a cell to the right
                self.isJumped = True
                jumpCoord = (self.coord[0]-1, self.coord[1]-1) #the cell jumped
                self.dict[jumpCoord].delete_oval()
            elif self.coord[0] == self.checkBoard.cellClicked[0] + 2 and \
               self.coord[1] == self.checkBoard.cellClicked[1] - 2:
                #if it jumped a cell to the left
                self.isJumped = True
                jumpCoord = (self.coord[0]-1, self.coord[1]+1) #the cell jumped
                self.dict[jumpCoord].delete_oval()
        
    def get_possible_moves(self, multiplier, cond1, cond2):
        '''CheckerCell.get_possible_moves
            returns a list of the possible
            moves a checker can make
            '''
        x = self.coord[0]
        y = self.coord[1]
        possibleMovesList =  []
        #all possible moves are added to possibleMovesList
        if cond1 and y > 1: #checking if a white or red cell can jump to the left
            diagonalLeft = (x+2*multiplier, y-2)
            jumpCell = (x+1*multiplier, y-1)
            if self.dict[jumpCell].hasCircle == True and \
               self.dict[jumpCell].circleColor != self.circleColor \
               and self.dict[diagonalLeft].hasCircle == False:
                print('jump to the left')
                possibleMovesList.append(diagonalLeft)
                self.jumpLeft = True
        if cond1 and y < 6: #checking if a white or red cell can jump to the right
            diagonalRight = (x+2*multiplier, y+2)
            jumpCell = (x+1*multiplier, y+1)
            if self.dict[jumpCell].hasCircle == True and \
               self.dict[jumpCell].circleColor != self.circleColor \
               and self.dict[diagonalRight].hasCircle == False:
                print('jump to the right')
                possibleMovesList.append(diagonalRight)
                self.jumpRight = True
        if self.jumpLeft != True and self.jumpRight != True: #only if a cell can't jump,
            if cond2 and y > 0: #check if it can move to the left
                diagonalLeft = (x+1*multiplier, y-1)
                if self.dict[diagonalLeft].hasCircle == False:
                    print('move left')
                    possibleMovesList.append(diagonalLeft)
            if cond2 and y < 7: #check if it can move to the right
                diagonalRight = (x+1*multiplier, y+1)
                if self.dict[diagonalRight].hasCircle == False:
                    print('move right')
                    possibleMovesList.append(diagonalRight)
        return possibleMovesList

    def make_oval(self,color):
        '''CheckerCell.make_oval(color)
        changes color of piece on square to specified color'''
        self.ovalList = self.find_all()  # remove existing piece(s)
        for oval in self.ovalList:
            self.delete(oval)
        self.create_oval(10,10,44,44,fill=color)    #create a new one
        self.hasCircle = True
        self.circleColor = color

    def delete_oval(self):
        '''CheckerCell.delete_oval()
        deletes oval on square'''
        self.ovalList = self.find_all()  # remove existing piece(s)
        for oval in self.ovalList:
            self.delete(oval)
        self.hasCircle = False

class CheckerBoard:
    def __init__(self):
        self.currentPlayer = 0
        self.colorList = ['red', 'white']
        self.cellClicked = 0
        self.jumpMoveList = []
        self.gotoCell = 0
        self.board = {}
        for r in range(3):
            for c in range(8):
                coord = (r, c)
                if (r % 2 != 0 and c % 2 == 0) or (r%2 == 0 and c%2 != 0):
                    self.board[coord] = 0 #red player
        for r in range(5, 8):
            for c in range(8):
                coord = (r, c)
                if (r % 2 != 0 and c % 2 == 0) or (r%2 == 0 and c%2 != 0):
                    self.board[coord] = 1   #white player
        
class CheckerGrid(Frame):
    def __init__ (self, master):
        Frame.__init__(self,master,bg='white')
        self.grid()
        self.checkerBoard = CheckerBoard()
        # set up scoreboard and status markers
        self.colors = ['red', 'white']  #red is player 0, white is player 1
        self.rowconfigure(8,minsize=3)  # leave a little space
        self.cellsDict = {}        
        # create indicator square
        self.turnSquare = CheckerCell(self,'red', 9,2)
        self.turnSquare['highlightthickness'] = 5
        self.turnSquare['width']=43
        self.turnSquare['height']=45
        self.turnSquare.unbind('<Button>')
        self.continueJump = Label(self, text=" test")
        self.continueJump.grid(row=9,column=3, columnspan=3)       
        for r in range(8):
            for c in range(8):
                coord = (r, c)
                if (r % 2 == 0 and c % 2 == 0) or ((r+1) % 2 == 0 and (c+1) % 2 == 0):
                    color = 'blanched almond'
                else:
                    color = 'dark green'
                self.cellsDict[coord] = CheckerCell(self, color, r, c)
        for i in self.checkerBoard.board:
            self.cellsDict[i].update()
            if self.checkerBoard.board[i] == 0:
                self.cellsDict[i].make_oval('red')
                self.cellsDict[i].circleColor = 'red'
                self.cellsDict[i].hasCircle = True
            else:
                self.cellsDict[i].make_oval('white')
                self.cellsDict[i].circleColor = 'white'
                self.cellsDict[i].hasCircle = True

    def change_turn_color(self):
        if self.checkerBoard.currentPlayer == 0:
            self.turnSquare = CheckerCell(self,'red', 9,2)
        else:
            self.turnSquare = CheckerCell(self,'white', 9,2)

    def change_highlight(self, highlightCell):
        for i in self.cellsDict:
            if self.cellsDict[i]['highlightbackground' ] == 'white':
                self.cellsDict[i]['highlightbackground' ] = 'black'
                break
        highlightCell['highlightbackground'] = 'white'

    def check_and_act_for_win(self, cellMoved, cellLanded):
        if cellMoved.circleColor == 'white':
            if cellLanded.coord[0] == 0:
                cellLanded.create_text(27, 38, font =("", 40), text='*', fill="dark blue")
                return 1
        else:
            if cellLanded.coord[0] == 7:
                cellLanded.create_text(27, 38, font =("", 40), text='*', fill="dark blue")
                return 1

    def end_game(self):
        for i in self.cellsDict:
            self.cellsDict[i].unbind('<Button>')
        self.turnSquare.create_text(27, 38, font =("", 40), text=self.checkerBoard.currentPlayer+1, fill="dark blue")
        self.continueJump['text'] = ''
    
root = Tk()
root.title('Checkers')
CH = CheckerGrid(root)
CH.mainloop()
