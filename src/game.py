from typing import Tuple
import random

TileValue = int
Board = list[TileValue]
Row = list[TileValue]

LEFT = 'a'
RIGHT = 'd'
UP = 'w'
DOWN = 's'
KEYS = [LEFT, RIGHT, UP, DOWN]

class Game2048:
    def __init__(self, size: Tuple[int,int] = (4,4)):
        self.size = size
        self.board = self.generate_board()
        self._tick()
        self._tick()

    def __str__(self) -> str:
        """ This will generate a 2048 string board. """
        line_section = '-' * (7 * self.total_col + 1) + '\n'

        repr = str()
        repr += line_section
        for row in range(self.total_row):
            row_value = [self._get_tile_value(row, col) for col in range(self.total_col)]
            row_string_value = [str(val).rjust(4, ' ') for val in row_value]
            middle = ' | '.join(row_string_value)
            row_repr = '| ' + middle + ' |\n'
            repr += row_repr
            repr += line_section
        return repr

    @property
    def total_row(self) -> int:
        """ Return number of rows in the board. """
        return self.size[0]

    @property
    def total_col(self) -> int:
        """ Return number of columns in the board. """
        return self.size[1]

    @property
    def is_won(self) -> bool:
        """ Return boolean if the game is won. """
        for tile in self.board:
            if tile == 2048:
                return True
        return False

    @property
    def is_lost(self) -> bool:
        """ Return boolean if the game is lost. """
        for tile in self.board:
            if tile == 0:
                return False
        return True

    def is_squishable(self, direction: str) -> bool:
        """ Check if tiles can be moved into certain direction. """
        if direction == UP or direction == DOWN:
            for col_idx in range(self.total_col):
                sequence = self.board[col_idx:: self.total_col]
                reverse = True if direction == DOWN else False
                updated_sequence = self.update(sequence, reverse)
                if sequence != updated_sequence:
                    return True
                
        elif direction == LEFT or direction == RIGHT:
            for row_idx in range(self.total_row):
                start = row_idx * self.total_col
                stop = start + self.total_col
                sequence = self.board[start:stop]

                reverse = True if direction == RIGHT else False
                updated_sequence = self.update(sequence, reverse)
                if sequence != updated_sequence:
                    return True

        return False

    def generate_new_value(self) -> int:
        """ Generate new random tile values, which return 2 for 90% and 4 for 10%. """
        value = random.choices([2,4],[0.9,0.1])[0]
        return value
                
    def generate_board(self) -> Board: 
        """ Generate a list type board from given size. """
        total_tile = self.total_row * self.total_col
        board = [0 for _ in range(total_tile)]
        return board

    def show_board(self) -> None:
        """ Print board on terminal. """
        print(self)

    def _get_tile_value(self, row: int, col: int) -> TileValue:
        """ Get tile value at particular row and column. """
        idx = (row * self.total_col) + col
        return self.board[idx]

    def _get_empty_tile_idx(self) -> int:
        """ Return one random empty tile on the board. """
        empty_tile_idxs = [tile_idx for tile_idx, tile in enumerate(self.board) if tile == 0]
        empty_tile_idx = random.choice(empty_tile_idxs)
        return empty_tile_idx

    def _get_user_input(self) -> str:
        """ Get user move input. """
        move = str(input(f"Move {KEYS}: "))
        if move not in KEYS:
            if move != 'exit':
                print('Please choose a given key to play!'.upper())
        return move

    def play(self) -> None:
        """ Start playing a game. """
        while True:
            self.show_board()

            if self.is_lost:
                print('You lost!')
                break

            while True:
                move = self._get_user_input()
                if self.is_squishable(move):
                    break
                else:
                    print('Tiles cannot be moved in that direction!'.upper())
                    self.show_board()

            if move == 'exit':
                break

            self._move_tiles(move)

            if self.is_won:
                print('You Win!')
                break

            self._tick()
    
    def _tick(self) -> None:
        """ Move to the next game tick, this will generate new random tile. """
        empty_tile = self._get_empty_tile_idx()
        new_value = self.generate_new_value()
        self.board[empty_tile] = new_value

    def _move_tiles(self, move: str) -> None:
        """ Move all tiles on the board, as user intended move. """
        if move == DOWN or move == UP:
            for col_idx in range(self.total_col):
                sequence = self.board[col_idx:: self.total_col]

                reverse = True if move == DOWN else False
                updated_row = self.update(sequence, reverse)
                for idx, num in enumerate(updated_row):
                    self.board[col_idx + (idx * self.total_col)] = num

        elif move == LEFT or move == RIGHT:
            for row_idx in range(self.total_row):
                start = row_idx * self.total_col
                stop = start + self.total_col
                sequence = self.board[start:stop]

                reverse = True if move == RIGHT else False
                updated_row = self.update(sequence, reverse)
                self.board[start:stop] = updated_row

    def update(self, row: Row, reverse: bool = False) -> Row:
        """ Update individual row. """
        row = list(reversed(row)) if reverse else row
        squished_row = self._squish(row)
        merged_row = self._merge(squished_row)
        squished_row = self._squish(merged_row)
        return list(reversed(squished_row)) if reverse else squished_row

    def _squish(self, row: Row) -> Row:
        """ Squish all the tile value inside the row to the left. """
        squished_row = [tile_val for tile_val in row if tile_val != 0]
        squished_row.extend([0] * (len(row) - len(squished_row)))
        return squished_row

    def _merge(self, row: Row) -> Row:
        """ Merge same tile value within the row to the left. """
        new_row = list()
        skip = False
        for idx in range(len(row) - 1):
            current_val, next_val = row[idx], row[idx+1]
            if skip:
                skip = False
                continue
            if current_val == next_val and current_val != 0:
                new_row.extend([current_val*2, 0])
                skip = True
            else:
                new_row.append(current_val)
        if not skip:
            new_row.append(next_val)
        return new_row

game = Game2048()
game.play()
