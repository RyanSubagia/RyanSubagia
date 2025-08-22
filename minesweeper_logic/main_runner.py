import os
import game
import renderer

def run():
    action = os.getenv('INPUT_ACTION')
    position_str = os.getenv('INPUT_POSITION')
    repo_url = os.getenv('GITHUB_REPOSITORY')

    state = game.load_state()

    if action == 'new' or not state:
        state = game.create_board(rows=8, cols=12, mines=15)
    
    elif action and position_str and not state.get("game_over"):
        row, col = map(int, position_str.split(','))
        
        if action == 'reveal':
            state = game.reveal_square(state, row, col)
        elif action == 'flag':
            state = game.flag_square(state, row, col)

    game.save_state(state)

    renderer.generate_svg(state, repo_url)

    print("Minesweeper board updated successfully.")

if __name__ == "__main__":
    run()
