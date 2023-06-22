from __future__ import annotations

class Piece:

    __key = object()
    __lengths = {"white": 1, "black": 1}
    __names = {"white": "White", "black": "Black"}
    __grid_rep = {"white": "W", "black": "B"}

    @classmethod
    def createPiece(cls, piece_type: str) -> Piece:
        if piece_type.lower() in {"white", "black"}:
            return Piece(Piece.__key, piece_type.lower())
        else:
            return None

    def __init__(self, key: object, piece_type: str) -> None:
        assert key is Piece.__key, "Piece constructor should not be called directly."
        self.__piece_type = piece_type
        self.__segments = dict((i, Segment(self)) for i in range(1, self.length() + 1))

    def length(self) -> int:
        return Piece.__lengths.get(self.__piece_type, 0)

    def get_segment(self, number: int) -> Segment:
        return self.__segments.get(number, None)

    def name(self) -> str:
        return Piece.__names.get(self.__piece_type, "?")

    def sunk(self) -> bool:
        return all(s.hit() for s in self.__segments.values())

    def __str__(self) -> str:
        return Piece.__grid_rep.get(self.__piece_type, "?")

    def __repr__(self) -> str:
        return self.__str__()


class Segment:

    def __init__(self, piece: Piece) -> None:
        self.__piece = piece
        self.__hit = False

    def hit(self) -> bool:
        return self.__hit

    def attack(self) -> None:
        self.__hit = True

    def get_piece(self) -> Piece:
        return self.__piece

    def __str__(self) -> str:
        return self.__piece.__str__() if self.__piece is not None else "?"

    def __repr__(self) -> str:
        return self.__str__()


class Cell:

    def __init__(self) -> None:
        self.__segment = None
        self.__hit = False
        self.__married = False

    def has_been_hit(self) -> bool:
        return self.__hit

    def attack(self) -> None:
        if self.__segment is not None:
            self.__segment.attack()
        self.__hit = True

    # Other methods...

    def mark_married(self) -> None:
        self.__married = True

    def is_married(self) -> bool:
        return self.__married

    def is_occupied(self) -> bool:
        return self.__segment is not None

    def place_segment(self, segment: Segment) -> None:
        if not self.is_occupied():
            self.__segment = segment

    def display_setup(self) -> str:
        if self.has_been_hit():
            cell_piece = self.__segment.__str__()
            return "X"
        elif self.is_occupied():
            return self.__segment.__str__()
        else:
            return "."


class InvalidPositionException(Exception):
    pass


class InvalidPieceTypeException(Exception):
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

    def place_piece(self, piece: Piece, position: str) -> None:
        if piece is None:
            raise InvalidPieceTypeException()

        row = Board.__row_map.get(position[:1].upper(), None)
        col = -1
        if position[1:].isdigit():
            col = int(position[1:])
        else:
            raise InvalidPositionException()

        if row not in self.__board.keys() or col not in self.__board[row].keys():
            raise InvalidPositionException()

        for i in range(col, col + piece.length()):
            if i > Board.SIZE or self.__board[row][i].is_occupied():
                raise InvalidPlacementException()

        for i in range(row, row + piece.length()):
            if i > Board.SIZE or self.__board[i][col].is_occupied():
                raise InvalidPlacementException()

        for i in range(col, col + piece.length()):
            self.__board[row][i].place_segment(piece.get_segment(i - col + 1))

        for i in range(row, row + piece.length()):
            self.__board[i][col].place_segment(piece.get_segment(i - row + 1))

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

    def mark_married(self, position1: str, position2: str) -> None:
        row1 = Board.__row_map.get(position1[:1].upper(), None)
        col1 = -1
        if position1[1:].isdigit():
            col1 = int(position1[1:])
        else:
            raise InvalidPositionException()

        row2 = Board.__row_map.get(position2[:1].upper(), None)
        col2 = -1
        if position2[1:].isdigit():
            col2 = int(position2[1:])
        else:
            raise InvalidPositionException()

        if row1 not in self.__board.keys() or col1 not in self.__board[row1].keys() or \
                row2 not in self.__board.keys() or col2 not in self.__board[row2].keys():
            raise InvalidPositionException()

        if self.__board[row1][col1].is_occupied() and self.__board[row2][col2].is_occupied():
            piece1 = self.__board[row1][col1].get_segment().get_piece()
            piece2 = self.__board[row2][col2].get_segment().get_piece()

            if piece1 != piece2:
                for row in self.__board.values():
                    for cell in row.values():
                        if cell.is_occupied() and cell.get_segment().get_piece() in [piece1, piece2]:
                            cell.mark_married()
            else:
                raise InvalidPlacementException()
        else:
            raise InvalidPlacementException()

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