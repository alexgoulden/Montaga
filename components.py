from __future__ import annotations

class Piece:

    __key = object()
    __lengths = {"white": 1, "black": 1, "married": 1}
    __names = {"white": "White", "black": "Black", "married": "Married"}
    __grid_rep = {"white": "W", "black": "B", "married": "M"}

    @classmethod
    def createPiece(cls, piece_type: str) -> Piece:
        if piece_type.lower() in {"white", "black", "married"}:
            return Piece(Piece.__key, piece_type.lower())
        else:
            return None

    def __init__(self, key: object, piece_type: str) -> None:
        assert key is Piece.__key, "Piece constructor should not be called directly."
        self.__piece_type = piece_type

    def length(self) -> int:
        return Piece.__lengths.get(self.__piece_type, 0)

    def name(self) -> str:
        return Piece.__names.get(self.__piece_type, "?")

    def __str__(self) -> str:
        return Piece.__grid_rep.get(self.__piece_type, "?")

    def __repr__(self) -> str:
        return self.__str__()

class Cell:

    def __init__(self, piece: Piece = None) -> None:
        self.__piece = piece
        self.__hit = False
        self.__married = False

    def has_been_hit(self) -> bool:
        return self.__hit

    def attack(self) -> None:
        if self.__piece is not None:
            self.__hit = True

    def get_piece(self) -> Piece:
        return self.__piece

    def place_piece(self, piece: Piece) -> None:
        if self.__piece is None:
            self.__piece = piece

    def is_married(self) -> bool:
        return self.__married

    def set_married(self, is_married: bool) -> None:
        self.__married = is_married

    def __str__(self) -> str:
        return self.__piece.__str__() if self.__piece is not None else "?"

    def __repr__(self) -> str:
        return self.__str__()

    def display_setup(self) -> str:
        if self.has_been_hit():
            return "X"
        elif self.is_married():
            return "M"
        elif self.__piece is not None:
            return self.__piece.__str__()
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
        self.__married_pairs = {} # Keep track of married pairs
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
            if i > Board.SIZE or self.__board[row][i].get_piece() is not None:
                raise InvalidPlacementException()

            # Check if the piece is being placed adjacent to another piece
            adjacent_positions = [(row-1, i), (row+1, i), (row, i-1), (row, i+1)]
            for adj_row, adj_col in adjacent_positions:
                if adj_row in self.__board.keys() and adj_col in self.__board[adj_row].keys():
                    adjacent_cell = self.__board[adj_row][adj_col]
                    if adjacent_cell.get_piece() is not None:
                        # If adjacent cell has a married piece, allow placement
                        if adjacent_cell.get_piece().name() == "Married":
                            continue
                        elif not adjacent_cell.is_married():
                            raise InvalidPlacementException("Can't place a piece adjacent to another piece unless they are married or adjacent to a married piece!")

        # Check if the cell is occupied
        if self.__board[row][col].get_piece() is not None:
            raise InvalidPlacementException()

        # Place piece on the cell
        self.__board[row][col].place_piece(piece)

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

        # Check if the cell being attacked is part of a married pair
        if (row, col) in self.__married_pairs:
            # If so, also attack the other cell in the pair
            other_row, other_col = self.__married_pairs[(row, col)]
            self.__board[other_row][other_col].attack()
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

    def mark_married(self, position1: str, position2: str) -> None:
        row1 = Board.__row_map.get(position1[:1].upper(), None)
        col1 = int(position1[1:])
        row2 = Board.__row_map.get(position2[:1].upper(), None)
        col2 = int(position2[1:])

        if row1 not in self.__board.keys() or col1 not in self.__board[row1].keys() or \
                row2 not in self.__board.keys() or col2 not in self.__board[row2].keys():
            raise InvalidPositionException()

        cell1 = self.__board[row1][col1]
        cell2 = self.__board[row2][col2]

        # Set is_married to True for both cells
        cell1.set_married(True)
        cell2.set_married(True)

        # Record the married pair in the dictionary
        self.__married_pairs[(row1, col1)] = (row2, col2)
        self.__married_pairs[(row2, col2)] = (row1, col1)

        married_piece = Piece.createPiece("married")

        # Overwrite pieces with the married piece
        cell1.place_piece(married_piece)
        cell2.place_piece(married_piece)

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