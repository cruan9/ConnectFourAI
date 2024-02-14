# Connect Four AI

Connect Four AI using Minimax algorithm that uses various heuristics. Create your own game by adding `game = Game(<Player1>, <Player2>)` into the main function of `agents.py`. Then, run the program by cloning the directory and entering `python agents.py` into the terminal. 

### Available players:
- `HumanPlayer():` Human player that inputs their move using columns 0-6.
- `MinimaxPlayer(depth, heuristic):` AI player that uses the minimax algorithm up to a specified depth to choose their next move.
    - Available heuristics include:
        - `my_heuristic:` Measures a heuristic based on the number of possible blocks of four where two or three out of the four are of one colour. Blocks of three have higher weighting than blocks of two. 
        - `three_line_heur:` Counts the number of three in a rows for each colour
        - `zero_heur:` Returns a zero heuristic for every board state
- `RandomPlayer():` Makes a random move each time
- `FirstMovePlayer():` Plays the first legal move
