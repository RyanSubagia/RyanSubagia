import json
import random

def load_state():
    """Tries to load the game state from game_state.json."""
    try:
        with open('game_state.json', 'r') as f:
            content = f.read()
            if not content.strip():
                return None
            return json.loads(content)
    except FileNotFoundError:
        return None

def save_state(state):
    """Saves the current game state to game_state.json."""
    with open('game_state.json', 'w') as f:
        json.dump(state, f, indent=2)

def create_board(rows, cols, mines):
    """Creates a new board and game state."""
    board = [[{"is_mine": False, "is_revealed": False, "is_flagged": False, "adjacent_mines": 0} for _ in range(cols)] for _ in range(rows)]

    placed_mines = 0
    while placed_mines < mines:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if not board[r][c]["is_mine"]:
            board[r][c]["is_mine"] = True
            placed_mines += 1

    for r in range(rows):
        for c in range(cols):
            if not board[r][c]["is_mine"]:
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc]["is_mine"]:
                            count += 1
                board[r][c]["adjacent_mines"] = count

    return {"rows": rows, "cols": cols, "mines": mines, "game_over": False, "win": False, "board": board}

def reveal_square(state, r, c):
    """Handles revealing a square, including flood fill for empty squares."""
    board = state["board"]
    rows, cols = state["rows"], state["cols"]

    if board[r][c]["is_revealed"] or board[r][c]["is_flagged"] or state["game_over"]:
        return state

    board[r][c]["is_revealed"] = True

    if board[r][c]["is_mine"]:
        state["game_over"] = True
        return state

    if board[r][c]["adjacent_mines"] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    state = reveal_square(state, nr, nc)
    
    if check_win_condition(state):
        state["win"] = True
        state["game_over"] = True

    return state

def flag_square(state, r, c):
    """Toggles a flag on a square."""
    if not state["board"][r][c]["is_revealed"] and not state["game_over"]:
        state["board"][r][c]["is_flagged"] = not state["board"][r][c]["is_flagged"]
    return state

def check_win_condition(state):
    """Checks if all non-mine squares have been revealed."""
    rows, cols = state["rows"], state["cols"]
    for r in range(rows):
        for c in range(cols):
            cell = state["board"][r][c]
            if not cell["is_mine"] and not cell["is_revealed"]:
                return False
    return True
