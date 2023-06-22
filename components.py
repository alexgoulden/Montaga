from __future__ import annotations

class Ship:

    __key = object()
    __lengths = {"white": 1, "black": 1}
    __names = {"white": "White", "black": "Black"}
    __grid_rep = {"white": chr(0x26AA), "black": chr(0x25EF)}

    @classmethod
    def createShip(cls, ship_type: str) -> Ship:
        if ship_type.lower() in {"white", "black"}:
            return Ship(Ship.__key, ship_type.lower())
        else:
            return None

    def __init__(self, key: object, ship_type: str) -> None:
        assert key is Ship.__key, "Ship constructor should not be called directly."
        self.__ship_type = ship_type
        self.__segments = dict((i, Segment(self)) for i in range(1, self.length() + 1))

    def length(self) -> int:
        return Ship.__lengths.get(self.__ship_type, 0)

    def get_segment(self, number: int) -> Segment:
        return self.__segments.get(number, None)

    def name(self) -> str:
        return Ship.__names.get(self.__ship_type, "?")

    def sunk(self) -> bool:
        return all(s.hit() for s in self.__segments.values())

    def __str__(self) -> str:
        return Ship.__grid_rep.get(self.__ship_type, "?")

    def __repr__(self) -> str:
        return self.__str__()


class Segment:

    def __init__(self, ship: Ship) -> None:
        self.__ship = ship
        self.__hit = False

    def hit(self) -> bool:
        return self.__hit

    def attack(self) -> None:
        self.__hit = True

    def get_ship(self) -> Ship:
        return self.__ship

    def __str__(self) -> str:
        return self.__ship.__str__() if self.__ship is not None else "?"

    def __repr__(self) -> str:
        return self.__str__()


class Cell:

    def __init__(self) -> None:
        self.__segment = None
        self.__hit = False

    def has_been_hit(self) -> bool:
        return self.__hit

    def attack(self) -> None:
        if self.__segment is not None:
            self.__segment.attack()
        self.__hit = True

    def is_occupied(self) -> bool:
        return self.__segment is not None

    def place_segment(self, segment: Segment) -> None:
        if not self.is_occupied():
            self.__segment = segment

    def __str__(self) -> str:
        if not self.has_been_hit():
            return "."
        elif not self.is_occupied():
            return "O"
        elif not self.__segment.get_ship().sunk():
            return "X"
        else:
            return self.__segment.__str__()

    def display_setup(self) -> str:
        if self.is_occupied():
            return self.__segment.__str__()
        else:
            return "."


class InvalidPositionException(Exception):
    pass


class InvalidShipTypeException(Exception):
    pass


class InvalidPlacementException(Exception):
    pass


class Board:

    SIZE = 5
    __row_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}

    def __init__(self) -> None:
        self.__board = {}
        for row_key in range(1, Board.SIZE + 1):
            row = {}
            for col_key in range(1, Board.SIZE + 1):
                row[col_key] = Cell()
            self.__board[row_key] = row

    def place_ship(self, ship: Ship, position: str, direction: str) -> None:
        if ship is None:
            raise InvalidShipTypeException()

        row = Board.__row_map.get(position[:1].upper(), None)
        col = -1
        if position[1:].isdigit():
            col = int(position[1:])
        else:
            raise InvalidPositionException()

        if row not in self.__board.keys() or col not in self.__board[row].keys():
            raise InvalidPositionException()

        if direction.lower() not in {"across", "down"}:
            raise InvalidPlacementException()

        if direction.lower() == "across":
            for i in range(col, col + ship.length()):
                if i > Board.SIZE or self.__board[row][i].is_occupied():
                    raise InvalidPlacementException()

        if direction.lower() == "down":
            for i in range(row, row + ship.length()):
                if i > Board.SIZE or self.__board[i][col].is_occupied():
                    raise InvalidPlacementException()

        if direction.lower() == "across":
            for i in range(col, col + ship.length()):
                self.__board[row][i].place_segment(ship.get_segment(i - col + 1))

        if direction.lower() == "down":
            for i in range(row, row + ship.length()):
                self.__board[i][col].place_segment(ship.get_segment(i - row + 1))

    def attack(self, position: str) -> None:
        print("Attacking", position)
        row = Board.__row_map.get(position[:1].upper(), None)
        col = -1
        if position[1:].isdigit():
            col = int(position[1:])
        else:
            raise InvalidPositionException()
        if row not in self.__board.keys() or col not in self.__board[row].keys():
            raise InvalidPositionException()
        self.__board[row][col].attack()

    def has_been_hit(self, position: str) -> bool:
        row = Board.__row_map.get(position[:1].upper(), None)
        col = -1
        if position[1:].isdigit():
            col = int(position[1:])
        else:
            raise InvalidPositionException()
        if row not in self.__board.keys() or col not in self.__board[row].keys():
            raise InvalidPositionException()
        return self.__board[row][col].has_been_hit()

    def __str__(self) -> str:
        grid = "  1 2 3 4 5\n"
        for row in ['A', 'B', 'C', 'D', 'E']:
            grid += row + " "
            for col in range(1, Board.SIZE):
                grid += str(self.__board[Board.__row_map[row]][col]) + " "
            grid += str(self.__board[Board.__row_map[row]][Board.SIZE]) + "\n"
        return grid

    def __repr(self) -> str:
        return self.__str__()

    def display_setup(self) -> str:
        grid = "  1 2 3 4 5\n"
        for row in ['A', 'B', 'C', 'D', 'E']:
            grid += row + " "
            for col in range(1, Board.SIZE):
                grid += self.__board[Board.__row_map[row]][col].display_setup() + " "
            grid += self.__board[Board.__row_map[row]][Board.SIZE].display_setup() + "\n"
        return grid