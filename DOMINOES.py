import random

class Dominoe:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "[" + str(self.left) + "-" + str(self.right) +"]"

    def is_match_end(self, pile):
        if len(pile) <= 0:
            return False
        other = pile[-1]
        if self.right == other.right:
            (self.right, self.left) = (self.left, self.right)
            return True
        return (self.left == other.right)

    def is_match_start(self, pile):
        if len(pile) <= 0:
            return False
        other = pile[0]
        if self.left == other.left:
            (self.right, self.left) = (self.left, self.right)
            return True
        return (self.right == other.left)

    def is_start(self):
        return self.left == 6 and self.right == 6

class DominoeDeck:
    def __init__(self):
        self.dominoes = []
        for i in range(7):
            for a in range(i, 7):
                k = [i, a]
                self.dominoes.append(Dominoe(i, a))

        for i in range(10):
            self.dominoes.append(Dominoe(6, i))
            self.dominoes.append(Dominoe(2, 2))
        random.shuffle(self.dominoes)

    def __str__(self):
        dominoStr = ""
        for i in self.dominoes:
            dominoStr += str(i) + "\n"
        return dominoStr

    def deal_dominoes(self):
        return self.dominoes.pop()

class DominoeChain:
    def __init__(self):       
        self.pile = []

    def __str__(self):
        output = ""
        for i in self.pile:
            output += str(i) + ", "
        return output

    def add_domino(self, domino):
        if domino.is_match_end(self.pile) == True:
            self.pile.append(domino)
        elif domino.is_match_start(self.pile) == True:
            self.pile.insert(0, domino)
        elif len(self.pile) == 0 and domino.is_start() == True:
            self.pile.append(domino)
            
    def get_pile(self) :
        return self.pile

class Player:
    def __init__(self,name, deck):
        self.name = name
        self.hand = [deck.deal_dominoes() for i in range(7)]

    def __str__(self):
        output = self.name
        for i in self.hand:
            output += "\n" + str(i) 
        return output

    def dominoes_to_play(self, chain):
        dominoList = []
        for domino in self.hand:
            if domino.is_match_start(chain.get_pile()) == True or domino.is_match_end(chain.get_pile()) == True:
                dominoList.append(domino)
        return dominoList        

    def play_domino(self, domino, chain):
        self.hand.remove(domino)
        chain.add_domino(domino)
        print(str(self.name), "played:", domino)
        print("\nThis is the domino chain:")
        print (chain)
        print("\n")
        return domino

    def play_if_eligible_to_start(self, chain):
        for i in self.hand:
            if i.is_start() == True:
                print (self.name, "played first")
                self.play_domino(i, chain)              
                return True
        return False
        
    def get_hand(self):
        output = ""
        for domino in self.hand:
            output += str(domino) + "\n"
        return output

    def take_turn_human(self, chain):            
        print(self.name, ", these are your dominoes:")
        print(self.get_hand())
        print("You can play: ")
        matches = self.dominoes_to_play(chain)
        count = 0
        for i in matches:
            count += 1
            print(str(count) + ":", i)

        num = input("Which domino do you want to play: ")
        while num.isalpha() == True or int(num) <= 0 or int(num) > len(matches):
            print(len(matches), "     len")
            num = input("Which domino do you want to play: ")
            if num.isalpha() != True and int(num) > 0 and int(num) <= len(matches):
                break

        num = int(num)
        dominoToPlay = matches[num - 1]
        self.play_domino(dominoToPlay, chain)

    def take_turn_computer(self, chain):            
        matches = self.dominoes_to_play(chain)
        count = 0
        for i in matches:
            count += 1

        num = random.randint(0, count - 1)
        d = self.play_domino(matches[num], chain)

def play_domino():
    # deal dominos to 4 players
    deck = DominoeDeck()
    chain = DominoeChain()
    playerList = []
    noDomino = []
    print("There are four players in this game")
    name = input('Enter your name: ')
    playerList.append(Player(name, deck))

    for n in range(1, 4):
        computer = "Computer " + str(n)
        playerList.append(Player(computer,deck))
        
    numPlayers = len(playerList)
    count = -1

    for player in (playerList):
        count += 1
        if player.play_if_eligible_to_start(chain) == True:
            currentPlayerNum = count
            break

    while True:
        currentPlayerNum = (currentPlayerNum + 1) % numPlayers
        a = playerList[currentPlayerNum].dominoes_to_play(chain)
        playerName = playerList[currentPlayerNum].name

        if len(a) == 0:
            noDomino.append(1)
            if len(noDomino) == 4:
                if playerName == name: 
                    print("Congratulations,", str(playerName), ", you won!")
                    break
                else:
                    print(str(playerName), "won")
                    break
            if playerName == name: 
                print(str(playerName), "you have no dominoes to play.")
                input("\nPress enter to go to the next player\n")
            else:
                print(str(playerName), "has no dominoes to play.")
                input("\nPress enter to go to the next player\n")
        else:
            noDomino = []
            if playerName == name:
                playerList[currentPlayerNum].take_turn_human(chain)
            else:
                playerList[currentPlayerNum].take_turn_computer(chain)
                input("Press enter to go to the next player\n")
           
play_domino()
