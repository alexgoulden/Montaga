from components import Segment, Ship, Cell, InvalidPlacementException, InvalidPositionException, InvalidShipTypeException, Board

if __name__ == "__main__":
    board = Board()
    ships = []
    for ship_name in Ship._Ship__names:
        ship = Ship.createShip(ship_name)
        ships.append(ship)

    print("Welcome to Montaga\n")
    print("Setup Phase")
    print("Player 1 place your ships, Player 2 - no peeking.\n" + chr(9786))

    for ship in ships:
        ship_name = ship.name()
        print(board.display_setup())
        while True:
            try:
                ship_promt = print("Where would you like to place your " + ship_name + "?")
                position = input("Position: ")
                direction = input("Direction: ")
                board.place_ship(ship, position, direction)
                break
            except InvalidPlacementException:
                print("That is not a valid placement for that ship.")
            except InvalidPositionException:
                print("That position does not exist.")
    print(board.display_setup())

    print("Attack Phase")
    print("Player 2, sink the fleet!\n")


    count = 0
    while True:
        print(board.__str__())
        all_ships_sunk = all(ship.sunk() for ship in ships)
        if all_ships_sunk:
            break
        try:
            attack_promt = input("Enter a grid coordinate to attack: ")
            if board.has_been_hit(attack_promt):
                raise InvalidPlacementException()
            board.attack(attack_promt)
            count += 1
        except InvalidPositionException:
            print("That is not a valid position to attack.")
        except InvalidPlacementException:
            print("That position has already been attacked. Try again.")



    print("The fleet has been sunk in " + str(count) + " shots!")
    print("GAME OVER")