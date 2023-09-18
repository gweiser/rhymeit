"""All functions are stored here"""
from wonderwords import RandomWord
from colorama import Fore
import requests
import sys
import os
import json
import random

# Global variables
points = 0
jokerUsed = False
internetConnection = False
cache = []

def generate(length):
    """Generate a random word using the wonderwords library"""
    r = RandomWord()
    word = r.word(word_min_length=length, word_max_length=length)
    return word 


def instructions():
    """Show gameplay instructions"""
    with open("instructions.txt") as file:
        return file.read()


def prompt_x_y(prompt, x, y):
    """For 50/50 questions (eg.: Y/N)"""
    while True:
        answer = input(prompt).lower().strip()
        if answer in [x, y]:
            return answer
        print(f"Please answer with {x.upper()} or {y.upper()} only")


def find_rhymes(word):
    """Checks if there are rhymes to this word"""
    # Make API call
    try:
        response = requests.get("https://api.datamuse.com/words?rel_rhy=" + word, timeout=3).json()
        rhymingWords = []
        for dict in response:
            # Check for all rhymes
            rhymingWords.append(dict["word"])

        return rhymingWords
    except requests.ConnectionError:
        print("There was a problem connecting to the server, you will be redirected to offline mode")
        playgame_offline()     


def get_highscore():
    """Display the high score"""
    if internetConnection:
        with open("highscore.txt") as file:
            return file.read()
    else:
        with open("offlinehighscore.txt") as file:
            return file.read()       
    

def game_over(points):
    """When game is lost"""
    global internetConnection
    print(f"\n{Fore.RED}Incorrect rhyme! Game Over!")
    print(Fore.WHITE)
    print(f"Your streak was {Fore.YELLOW}{points}")
    print(Fore.WHITE)
    highscore = int(get_highscore())
    if points > highscore:
        highscore = points
        if internetConnection:
            with open("highscore.txt", "w") as file:
                file.write(str(highscore))
        else:
            with open("offlinehighscore.txt", "w") as file:
                file.write(str(highscore))            
        print(f"{Fore.CYAN}Congratulations, your new highscore is {Fore.YELLOW}{highscore}")
        print(Fore.WHITE)
    else:
        print(f"Your high score is {Fore.YELLOW}{get_highscore()}")
        print(Fore.WHITE)
    print("Saving your progress...")
    # Write cache back to file
    write_cache()
    again = prompt_x_y("Do you want to play again? [Y/N] ", "y", "n")
    if again == "y":
        clear()
        reset()
        if internetConnection:
            playgame()
        else:
            playgame_offline()
    else:
        print(f"\n{Fore.YELLOW}Thank you for playing RhymeIt! Good Bye!\n")
        sys.exit(Fore.WHITE)


def joker():
    """One-time joker"""
    global points
    global jokerUsed
    global internetConnection

    if not jokerUsed:
        print(Fore.RED)
        print("Wrong answer!")
        response = prompt_x_y(f"{Fore.CYAN}Do you want to use your joker? You will be able to continue playing but will lose 3 points. [Y/N] ", "y", "n")
        print(Fore.WHITE)
        if response == "y":
            points -= 3
            jokerUsed = True
            clear()
            if internetConnection:
                playgame()
            else:
                playgame_offline()
        else:
            game_over(points)
    else:
        game_over(points)




def clear():
    """Clear the screen"""
    os.system("cls")


def reset():
    """Reset global points variable"""
    global points
    points = 0


def check_connection():
    """Check the user's internet connection"""
    try:
        requests.get("https://google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False


def read_cache():
    """Read cache into memory"""
    global cache
    with open("cache.txt") as file:
        for line in file:
            node = json.loads(line)
            cache.append(node)    



# def write_cache():
#     """Write cache back to file"""



def check_cache(word):
    """Search cache for the word, return rhymes if in cache"""
    global cache
    for node in cache:
        if node["word"] == word:
            return node["rhymes"]
    return False


def add_to_cache(word, rhymes):
    """Store a node consisting of a word and its rhymes in the cache"""
    global cache
    node = {"word": word, "rhymes": rhymes}
    cache.append(node)


def playgame():
    """Play a game of RhymeIt"""
    global points
    global internetConnection
    internetConnection = True
    # read cache into memory
    read_cache()
    while True:
        word_length = 3 if points <= 5 else 5 if points <= 7 else 7 if points <= 10 else 10
        word = generate(word_length) 

        while len(find_rhymes(word)) == 0: # type: ignore
            word_length = 3 if points <= 5 else 5 if points <= 7 else 7 if points <= 10 else 10
            word = generate(word_length)

        # If the word is already cached
        if check_cache(word):
            # Get rhymes from cache
            rhymes = check_cache(word)
        else:
            # Make API call for rhymes
            rhymes = find_rhymes(word)
            # Add the word and corresponding rhymes to cache
            add_to_cache(word, rhymes)

        print(f"\nYour word is {word}, can you find a rhyme?")
        userRhyme = input("Rhyme: ").strip().lower() 
        while userRhyme == "":
            userRhyme = input("Rhyme: ").strip().lower() 
        if userRhyme in rhymes: # type: ignore
            points += 1
            print(f"{Fore.GREEN}Correct! You get a point!")
            print(Fore.WHITE)
        else:
            # If incorrect rhyme
            joker()    



def playgame_offline():
    """Play a game without internet connection"""
    global points
    global internetConnection
    internetConnection = False
    global cache

    print("You are now playing in offline mode\n")

    read_cache() 

    while True:
        selectedNode = random.choice(cache)
        word = selectedNode["word"]
        rhymes = selectedNode["rhymes"]

        print(f"Your word is {word}, can you find a rhyme?")

        userRhyme = input("Rhyme: ").strip().lower() 
        while userRhyme == "":
            userRhyme = input("Rhyme: ").strip().lower() 
        
        if userRhyme in rhymes:
            points += 1
            print(f"\n{Fore.GREEN}Correct! You get a point!")
            print(Fore.WHITE)
        else:
            joker()