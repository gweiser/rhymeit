from functions import instructions, playgame, prompt_x_y, clear, check_connection, playgame_offline
import sys

def main():
    """Main functionality of the program"""
    print("\nWelcome to RhymeIt, a command-line game to test your rhyming skills!")
    print()
    play = prompt_x_y("Press x to play, or i to see the gameplay instructions! ", "x", "i").lower()
    if play == "x":
            if check_connection():
                playgame()
            else:
                playgame_offline()
    elif play == "i":
        # Show play instructions
        print(instructions())

        game = prompt_x_y("Do you want to play a game of RhymeIt? [Y/N] ", "y", "n")
        if game == "y":
            clear()
            if check_connection():
                playgame()
            else:
                playgame_offline()
        else:
            sys.exit("Good Bye!")
    else:
        sys.exit("Good Bye!")
    

if __name__ == "__main__":
    main()    