import random
guessesLeft = 6

def set_up():
    global letterList
    global word
    
    #read the word file into a list
    file = open("HangmanWords.txt", "r")
    wordList = []
    for line in file:
        #only add words which have more than 3 letters
        if len(line.strip()) > 3:
            wordList.append(line.strip())

    word = wordList[random.randint(0, len(wordList))] #a random word from the cumulative words list
    letterList = list(word) 

    print("Welcome to Hangman!") #instructions
    print("You can make up to 6 incorrect guesses.")
    print("\nLet's begin! I'm thinking of word with", len(letterList), "letters")
    print("---------------\n")
    return letterList

#prints the hangman based on how many guesses the user has left
def print_hangman(guessesLeft):
    if guessesLeft == 5:
        print("  O   ")
    elif guessesLeft == 4:
        print("  O   ")
        print("  |   ")
        print("  |   ")
    elif guessesLeft == 3:
        print("  O   ")
        print(" \|   ")
        print("  |   ")
    elif guessesLeft == 2:
        print("  O   ")
        print(" \|/  ")
        print("  |   ")
    elif guessesLeft == 1:
        print("  O   ")
        print(" \|/  ")
        print("  |   ")
        print(" /    ")
    elif guessesLeft == 0:
        print("  O   ")
        print(" \|/  ")
        print("  |   ")
        print(" / \  ")

def check_if_won(hangmanList):
    for i in hangmanList:
        if i == "_": #is there is a blank, user hasn't guessed all letters
            return False
    return True #user guessed all letters so they won

def print_word(hangmanList):
    for a in hangmanList:
        print(a, end=" ") #prints what the correct letters the user guessed

#checks if the user's guess is a valid letter
def valid_input(letter, lettersGuessed):
    global guessesLeft

#if the character(s) the user entered is
            #already guessed,         not a letter,              more than one character
    while letter in lettersGuessed or letter.isalpha() == False or len(letter) != 1: 
        guessesLeft -= 1
        print_hangman(guessesLeft)
        print("\n---------------\n")
        if guessesLeft > 0: #if they have more guesses left
            print("You have", guessesLeft, "incorrect guesses left.")
            letter = input("Please enter a valid guess: ") #keep asking them to guess 
        else:
            return False #no more guesses

    lettersGuessed.append(letter) #add letter to list of letters guessed
    return letter

def play_hangman(letterList):
    hangmanList = [] #the list which will hold the user's correct guesses in the correct location
    lettersGuessed = [] #the list holding the letters the user guessed
    global guessesLeft
    global word

    #start off with an empty list for the user
    for i in range(len(letterList)):
        hangmanList.append("_")

    while guessesLeft > 0:
        print("You have", guessesLeft, "incorrect guesses left.")
        letter = input("Please guess a letter: ")
        checkedLetter = valid_input(letter, lettersGuessed) #make sure they guessed is a new letter
            
        if checkedLetter in letterList: #user guessed a letter in the word
            print("Good guess:", end = " ")
            for a in range(len(letterList)): #go through the word
                if letterList[a] == checkedLetter: #where ever the letter is,
                    hangmanList[a] = checkedLetter #change it in hangmanList

            if check_if_won(hangmanList): #if they won, let them know
                print_word(hangmanList)
                return("\n\nCongratulations, you won!")
                    
        else: #user's guess was not in the word
            guessesLeft -= 1
            print_hangman(guessesLeft) #print updated hangman
            if checkedLetter != False:
                print("\nSorry - '" + checkedLetter + "' isn't in the word!:", end = " ")

        if checkedLetter != False:
            print_word(hangmanList)
            print("\n---------------\n")

    #no more guesses left which means they lost
    return "\nSorry, you lost! The word was '" + word + "'"

print(play_hangman(set_up()))
