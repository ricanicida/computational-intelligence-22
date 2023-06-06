# General information
- This is a project for the Computational Intelligence course lectured by Professor Giovanni Squillero and Andrea Calabrese at Politecnico di Torino. 
- The code of the final-project directory was downloaded from https://github.com/squillero/computational-intelligence/tree/master/2022-23/quarto.
- My contributions are present in the main.py file in the IntuitivePlayer class.

# Quarto game
## Player and plays
- 2 players' game
- Step 1: Player 1 chooses piece
- Step 2: Player 2 places piece
- Step 3: Swap(player 1, player 2), goto step 1
## Board and pieces
### Board
- 4x4 board (16 positions)
### Pieces
- 16 pieces
- 4 binary characteristics for each piece (high/low, coloured/not coloured, square/round, full/hollow)
## Winner
- First player to form a Quarto wins
- Quarto: 4 aligned pieces with the same characteristic (at least one of the 4 characteristics must be equal for the 4 pieces) in horizontal, vertical, or diagonal direction

# About the IntuitivePlayer (rule-based player)
## choose_piece(self)
- For each piece left it counts the number of possible winning positions
- Chooses the piece with the minimum count (it follows the pieces index in case of multiple pieces with the minimum count)
## place_piece(self)
- Searches for a possible winning position for a given selected piece
- If there is no winning positions, it searches for the safest position
- Safest: position that minimizes the position risk
- Position risk: the mean over each piece characteristic risk
- Piece characteristic risk: the mean + standard deviation over the characteristic match count for each direction (horizontal, vertical, diagonal (if it is the case))
