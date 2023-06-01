# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import logging
import argparse
import random
import quarto

import numpy as np


class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)
    

class IntuitivePlayer(quarto.Player):
    """Intuitive player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def _get_pieces_on_board(self, binary_board: np.array) -> np.array:
        return np.array([binary_board[i][j] for i in range(len(binary_board)) for j in range(len(binary_board[i])) if not np.isnan(binary_board[i][j].any())])

    def _return_piece_from_int(self, n: int, sorted_index: list) -> quarto.Piece:
        binary_str = '0'*(4-len(bin(n)[2:])) + bin(n)[2:]
        sorted_booleans = np.full(shape=4, fill_value=np.nan)
        for i in range(len(binary_str)):
            sorted_booleans[sorted_index[i]] = bool(int(binary_str[i]))
        
        return quarto.Piece(*sorted_booleans)
    
    def _return_piece_index(self, piece: quarto.Piece) -> int:
        return int("".join(str(x) for x in piece.binary), 2)
    
    def _return_winning_position_horizontal(self, piece: quarto.Piece, boards: list, vertical: bool=False, occurrences: int=3) -> tuple[int, int]:
        if vertical:
            boards = [np.transpose(board) for board in boards]
        
        for b in range(len(boards)):
            for i in range(len(boards[b])):
                value_count = dict(zip(*np.unique(boards[b][i], return_counts=True)))
                characteristic_present = piece.binary[b] in value_count.keys()
                available_space = np.isnan(boards[b][i]).any()

                if characteristic_present and available_space:
                    if value_count[piece.binary[b]] == occurrences:
                        y = i
                        x = np.where(np.isnan(boards[b][i]))[0][0]
                        if vertical:
                            return y, x
                        else:
                            return x, y
        return -1, -1
    
    def _return_winning_position_diagonal(self, piece: quarto.Piece, boards: list, occurrences: int=3):
        for b in range(len(boards)):
            diagonals = [np.diagonal(boards[b]), np.diagonal(np.fliplr(boards[b]))] 

            for i in range(2):
                value_count = dict(zip(*np.unique(diagonals[i], return_counts=True)))
                characteristic_present = piece.binary[b] in value_count.keys()
                available_space = np.isnan(diagonals[i]).any()

                if characteristic_present and available_space:
                    if value_count[piece.binary[b]] == occurrences:
                        y = np.where(np.isnan(diagonals[i]))[0][0]
                        x = abs(y - (len(diagonals[0])-1) * i)
                        return x, y
        return -1, -1
    
    def _return_winning_position(self, piece: quarto.Piece, binary_board: np.array, occurrences: int=3) -> tuple[int, int]:
        high_board = binary_board[:,:,0]
        coloured_board = binary_board[:,:,1]
        solid_board = binary_board[:,:,2]
        square_board = binary_board[:,:,3]
        boards = [high_board, coloured_board, solid_board, square_board]

        x, y = self._return_winning_position_horizontal(piece, boards, occurrences=occurrences)
        if x != -1:
            return x, y
        
        x, y = self._return_winning_position_diagonal(piece, boards, occurrences=occurrences)
        if x != -1:
            return x, y

        x, y = self._return_winning_position_horizontal(piece, boards, vertical=True, occurrences=occurrences)
        if x != -1:
            return x, y

        return -1, -1

    def choose_piece(self) -> int:
        game = self.get_game()
        pieces_on_board = self._get_pieces_on_board(game._binary_board)
        total_sum = np.sum(pieces_on_board, axis=0)
        # sort the indexes of the piece characteristics by appearance descending order
        sorted_index = sorted(range(len(total_sum)), key=lambda i:total_sum[i], reverse=True)
        n = 1
        piece = self._return_piece_from_int(n, sorted_index)
        piece_index = self._return_piece_index(piece)

        while piece_index in game._board and n < 15:
            n += 1
            piece = self._return_piece_from_int(n, sorted_index)
            piece_index = self._return_piece_index(piece)

        if n == 15:
            piece = self._return_piece_from_int(0, sorted_index)
            piece_index = self._return_piece_index(piece)

        return piece_index

    def place_piece(self) -> tuple[int, int]:
        game = self.get_game()
        binary_board = game._binary_board
        board = game._board
        piece_index = game.get_selected_piece()
        piece = self._return_piece_from_int(piece_index, [0,1,2,3])

        x, y = self._return_winning_position(piece, binary_board)

        if x != -1:
            return x, y
        
        x, y = self._return_winning_position(piece, binary_board, occurrences=1)

        if x != -1:
            return x, y
        else:
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if board[y][x] < 0:
                        print(y, x)
                        return x, y


def main():
    game = quarto.Quarto()
    game.set_players((IntuitivePlayer(game), RandomPlayer(game)))
    winner = game.run()
    logging.warning(f"main: Winner: player {winner}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count',
                        default=0, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()
