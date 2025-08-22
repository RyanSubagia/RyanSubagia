
import os
import game 
import renderer 

action = os.getenv('INPUT_ACTION')
position_str = os.getenv('INPUT_POSITION')
repo_url = os.getenv('GITHUB_REPOSITORY')

state = game.load_state()

if action == 'reveal' and position_str:
    row, col = map(int, position_str.split(','))
    state = game.reveal_square(state, row, col)

elif not state:
    state = game.create_board(rows=8, cols=8, mines=10)

game.save_state(state)

renderer.generate_svg(state, repo_url)

print("Game state updated and SVG rendered successfully!")
