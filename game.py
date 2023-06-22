from components import Segment, Piece, Cell, InvalidPlacementException, InvalidPositionException, \
    InvalidPieceTypeException, Board

if __name__ == "__main__":
    board = Board()
    pieces = []


    for piece_name in Piece._Piece__names:
        piece = Piece.createPiece(piece_name)
        pieces.append(piece)

# montaga code
    turns = board.SIZE * board.SIZE
    print("\nWelcome to Montaga...")
    print("A cruel wind blows,")
# first piece may only be placed
    print("\nWhite, begin.")

    # p: place, a: attack, ph: phantom placement, m: marry, ps: plot n scheme

    # reuse the attack code that is already further down

    for i in range(turns):
        print("\n" + str(turns - i) + " turns remain")
        # Alternate between the two players
        piece = pieces[i % 2]
        piece_name = piece.name()
        print(board.display_setup())
        action = ""
        while action not in ["p", "a", "m"]:
            print(piece_name + "'s Turn")
            action = input("Choose your action: ")
            if action.lower() == "p":
                while True:
                    print(board.display_setup())
                    try:
                        piece_prompt = print("\nWhere would you like to place, " + piece_name + "?")
                        position = input("Position: ")
                        board.place_piece(piece, position)
                        break
                    except InvalidPlacementException:
                        print("That is not a valid placement for that piece.")
                    except InvalidPositionException:
                        print("That position does not exist.")
            elif action.lower() == "a":
                # Code for handling attack action
                attack_success = False
                while not attack_success:
                    print(board.display_setup())
                    try:
                        attack_prompt = input("Enter a grid coordinate to attack: ")
                        if board.has_been_hit(attack_prompt):
                            raise InvalidPlacementException()
                        board.attack(attack_prompt)
                        attack_success = True  # Set flag to exit the loop
                    except InvalidPositionException:
                        print("That is not a valid position to attack.")
                    except InvalidPlacementException:
                        print("That position has already been attacked. Try again.")
            elif action.lower() == "m":
                while True:
                    try:
                        marry1 = input("Choose a white piece for the marriage")
                        marry2 = input("Choose a black piece for the marriage")
                        board.mark_married(marry1, marry2)
                        print("Pieces", marry1, "and", marry2, "are married!")


            else:
                print("Invalid action. Only 'p', 'a', 'm' allowed.")

    print(board.display_setup())

    print("The game is over," + winner + " has been declared the winner with" + str(count) + " children!")
