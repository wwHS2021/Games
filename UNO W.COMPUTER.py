import random

class UnoCard:
    '''represents an Uno card'''
 
    def __init__(self,rank,color):
        '''UnoCard(rank,color) -> UnoCard
        creates an Uno card with the given rank and color'''
        self.rank = rank
        self.color = color
 
    def __str__(self):
        '''str(Unocard) -> str'''
        return(self.color + ' ' + str(self.rank))
 
    def is_match(self,other):
        '''UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not'''
        return (self.color == other.color) or (self.rank == other.rank) or (self.rank == "card")

    def color_match(self,other):
        '''UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in color, False if not'''
        return (self.color == other.color)

class UnoDeck:
    '''represents a deck of Uno cards
    attribute:
      deck: list of UnoCards'''
 
    def __init__(self):
        '''UnoDeck() -> UnoDeck
        creates a new full Uno deck'''
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0,color))  # one 0 of each color
            for i in range(2):
                for n in range(1,10):  # two of each of 1-9 of each color
                    self.deck.append(UnoCard(n,color))

        for color in ['red', 'blue', 'green', 'yellow']:
            for i in range(2):
                for n in ["skip", "reverse", "draw two"]:
                    self.deck.append(UnoCard(n,color))   # two special cards of each color
                    

        for i in range(4):           
            self.deck.append(UnoCard("draw four", "wild"))
            self.deck.append(UnoCard("card", "wild"))
                    
        random.shuffle(self.deck)  # shuffle the deck
 
    def __str__(self):
        '''str(Unodeck) -> str'''
        return 'An Uno deck with '+str(len(self.deck))+' cards remaining.'
 
    def is_empty(self):
        '''UnoDeck.is_empty() -> boolean
        returns True if the deck is empty, False otherwise'''
        return len(self.deck) == 0
 
    def deal_card(self):
        '''UnoDeck.deal_card() -> UnoCard
        deals a card from the deck and returns it
        (the dealt card is removed from the deck)'''
        return self.deck.pop()
 
    def reset_deck(self,pile):
        '''UnoDeck.reset_deck(pile) -> None
        resets the deck from the pile'''
        if len(self.deck) != 0:
            return
        self.deck = pile.reset_pile() # get cards from the pile
        random.shuffle(self.deck)  # shuffle the deck

class UnoPile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''
 
    def __init__(self,deck):
        '''UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck'''
        card = deck.deal_card()
        self.pile = [card]  # all the cards in the pile
 
    def __str__(self):
        '''str(UnoPile) -> str'''
        return 'The pile has a '+str(self.pile[-1])+' on top.'
 
    def top_card(self):
        '''UnoPile.top_card() -> UnoCard
        returns the top card in the pile'''
        return self.pile[-1]
 
    def add_card(self,card):
        '''UnoPile.add_card(card) -> None
        adds the card to the top of the pile'''
        self.pile.append(card)
 
    def reset_pile(self):
        '''UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards'''
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck

class UnoPlayer:
    '''represents a player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards'''

    def __init__(self,name,deck):
        '''UnoPlayer(name,deck) -> UnoPlayer
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.name)+' has '+str(len(self.hand))+' cards.'

    def get_name(self):
        '''UnoPlayer.get_name() -> str
        returns the player's name'''
        return self.name

    def get_hand(self):
        '''get_hand(self) -> str
        returns a string representation of the hand, one card per line'''
        output = '' 
        for card in self.hand:
            output += str(card) + '\n'
        return output

    def find_wild_four(self):
        drawFourList = []
        for i in self.hand :
            if i.rank == "draw four":
                drawFourList.append(i)

        return drawFourList       

    def has_won(self):
        '''UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)'''
        return len(self.hand) == 0

    def draw_card(self,deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)   # add this card to the hand
        return card

    def play_card(self,card,pile):
        '''UnoPlayer.play_card(card,pile) -> None
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''
        self.hand.remove(card)
        pile.add_card(card)
        return card

    def take_turn_human(self,deck,pile):
        '''UnoPlayer.take_turn_human(deck,pile) -> None
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''
        
        # print player info
        print(self.name+", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        colorMatches = [card for card in self.hand if card.color_match(topcard)]

        if len(matches) > 0 or (len(colorMatches) == 0 and len(self.find_wild_four()) > 0):  # can play
            if len(colorMatches) == 0 and len(self.find_wild_four()) > 0:  #if no colors match, we can play the wild draw four
                matches.extend(self.find_wild_four())
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index+1) + ": " + str(matches[index]))
                
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
                    
            # play the chosen card from hand, add it to the pile
            card = self.play_card(matches[choice-1],pile)

            if str(card).find("wild") != -1:                
                #self.link_color_to_wild_card()
                inputColor = input("What color do you want to change to (r, g, y, b): ")
                while inputColor not in ['r', 'b', 'g', 'y']:
                    inputColor = input("What color do you want to change to: ")
                    if inputColor in ['r', 'b', 'g', 'y']:
                        break
                if inputColor in ['r', 'b', 'g', 'y']:
                    if inputColor == "r": 
                        card.color = "red"
                        return card
                    if inputColor == "b": 
                        card.color = "blue"
                        return card
                    if inputColor == "g": 
                        card.color = "green"
                        return card
                    else: 
                        card.color = "yellow"
                        return card

        else:  # can't play
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
                
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                return self.play_card(newcard,pile)
                
            else:   # still can't play
                print("Sorry, you still can't play.")
            input("Press enter to continue.")


#################################################################
    def take_turn_computer(self,deck,pile):
        '''UnoPlayer.take_turn(deck,pile) -> None
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''
        
        # print player info
        print(self.name+" turn.")
        print(pile)
        print("Computer hand: ")
        print(self.get_hand())
        
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        colorMatches = [card for card in self.hand if card.color_match(topcard)]

        if len(matches) > 0 or (len(colorMatches) == 0 and len(self.find_wild_four()) > 0):  # can play
            if len(colorMatches) == 0 and len(self.find_wild_four()) > 0:  #if no colors match, we can play the wild draw four
                matches.extend(self.find_wild_four())
            for index in range(len(matches)):
                #print the playable cards with their number
                print(str(index+1) + ": " + str(matches[index]))
                
            # computer chooses which card to play
            choice = random.randint(0, len(matches) - 1)
                    
            # play the chosen card from hand, add it to the pile
            card = self.play_card(matches[choice],pile)
            print("Computer played a", card)

            if str(card).find("wild") != -1:                
                inputNum = random.randint(0, 3)
                inputColor == ['r', 'b', 'g', 'y']
                card.color = inputColor[inputNum]
                return card

        else:  # can't play
            print("Computer can't play so it will have to draw.")
            input("Press enter to draw.")
            
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
                
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("It drew: "+str(newcard))
            
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                return self.play_card(newcard,pile)
                
            else:   # still can't play
                print("Computer still can't play.")
            input("Press enter to continue.")

        return card

#######################################################################
               

def play_uno(numPlayers): 
    '''play_uno(numPlayers) -> None
    plays a game of Uno with numPlayers'''

    reverse = False
    
    # set up full deck and initial discard pile
    deck = UnoDeck()
    pile = UnoPile(deck)
    
    # set up the players
    playerList = []
    for n in range(numPlayers):
        # get each player's name, then create an UnoPlayer
        name = input('Player #' + str(n+1) + ', enter your name: ')
        playerList.append(UnoPlayer(name,deck))

    playerList.append(UnoPlayer("Computer",deck))
    numPlayers += 1
        
    # randomly assign who goes first
    currentPlayerNum = random.randrange(numPlayers)
    
    # play the game
    while True:
        # print the game status
        print('-------')
        for player in playerList:
            print(player)
        print('-------')

        # take a turn
        increment = 1
        #a points to a card
        if playerList[currentPlayerNum].name == "Computer":
            a = playerList[currentPlayerNum].take_turn_computer(deck,pile)
        else:
            a = playerList[currentPlayerNum].take_turn_human(deck,pile)
        
        # check for a winner
        if playerList[currentPlayerNum].has_won():
            print(playerList[currentPlayerNum].get_name()+" wins!")
            print("Thanks for playing!")
            break

        if str(a).find("reverse") != -1:
            reverse = not reverse
        
        if str(a).find("skip") != -1:
            increment = 2
            currentPlayerNum = (currentPlayerNum + increment) % numPlayers
        elif str(a).find("four") != -1:
            cards = ""
            for i in range(3):
                card = (playerList[(currentPlayerNum + 1) % numPlayers]).draw_card(deck)
                cards += " a " + str(card)+ ", "
            lastCard = (playerList[(currentPlayerNum + 1) % numPlayers]).draw_card(deck)
            cards += "and a " + str(lastCard)
            print(str(playerList[(currentPlayerNum + 1) % numPlayers]) + ' They drew' + cards)
            
        elif str(a).find("draw") != -1:
            increment = 2          
            #next player draws two
            card1 = (playerList[(currentPlayerNum + 1) % numPlayers]).draw_card(deck)
            card2 = (playerList[(currentPlayerNum + 1) % numPlayers]).draw_card(deck)
            print(str(playerList[(currentPlayerNum + 1) % numPlayers]) + ' They drew a ' + str(card1) + ' and a ' + str(card2))
            #player after him goes
            currentPlayerNum = (currentPlayerNum + increment) % numPlayers
            
        elif reverse == True:   #when the game is actually going in reverse
            increment = -1
            currentPlayerNum = (currentPlayerNum + increment) % numPlayers
        else:        #when the game in reverse is reversed again or if no reverse card has been played
            currentPlayerNum = (currentPlayerNum + increment) % numPlayers

play_uno(4)
