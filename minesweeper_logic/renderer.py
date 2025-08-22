
import json

def generate_svg(state, repo_url):
    """Generates the SVG representation of the game board."""
    if not state:
        svg = '<svg width="240" height="50" xmlns="http://www.w3.org/2000/svg">'
        new_game_url = f"https://github.com/{repo_url}/actions/workflows/minesweeper.yml?ref=main&inputs={{'action':'new'}}"
        svg += f'<a href="{new_game_url}">'
        svg += '<rect x="0" y="0" width="240" height="50" fill="#4CAF50" rx="5"/>'
        svg += '<text x="120" y="30" font-family="Arial, sans-serif" font-size="16" fill="white" text-anchor="middle" dominant-baseline="middle">Click here to Start New Game</text>'
        svg += '</a></svg>'
        with open('minesweeper.svg', 'w') as f:
            f.write(svg)
        return

    SQUARE_SIZE = 30
    board = state["board"]
    rows, cols = state["rows"], state["cols"]
    width, height = cols * SQUARE_SIZE, rows * SQUARE_SIZE
    
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    svg += '<style>.cell-text { font: 16px sans-serif; text-anchor: middle; dominant-baseline: middle; }</style>'

    for r, row_data in enumerate(board):
        for c, cell in enumerate(row_data):
            x, y = c * SQUARE_SIZE, r * SQUARE_SIZE
            
            reveal_url = f"https://github.com/{repo_url}/actions/workflows/minesweeper.yml?ref=main&inputs={{'action':'reveal','position':'{r},{c}'}}"
            flag_url = f"https://github.com/{repo_url}/actions/workflows/minesweeper.yml?ref=main&inputs={{'action':'flag','position':'{r},{c}'}}"

            svg += f'<a href="{reveal_url}">'
            
            fill_color = "#bdbdbd" 
            if cell['is_revealed']:
                fill_color = "#e0e0e0" 
            
            if state["game_over"] and cell["is_mine"]:
                fill_color = "#ffcdd2" 

            svg += f'<rect x="{x}" y="{y}" width="{SQUARE_SIZE}" height="{SQUARE_SIZE}" fill="{fill_color}" stroke="#757575" stroke-width="1"/>'
            
            text_content = ''
            text_fill = 'black'
            if cell['is_flagged'] and not cell['is_revealed']:
                text_content = '🚩'
            elif state["game_over"] and cell["is_mine"]:
                text_content = '💣'
            elif cell['is_revealed']:
                if cell['adjacent_mines'] > 0:
                    text_content = str(cell['adjacent_mines'])
                    colors = ["#1976D2", "#388E3C", "#D32F2F", "#7B1FA2", "#FF8F00", "#00838F", "#424242", "#AD1457"]
                    text_fill = colors[cell['adjacent_mines'] - 1]

            if text_content:
                svg += f'<text x="{x + SQUARE_SIZE / 2}" y="{y + SQUARE_SIZE / 2}" class="cell-text" fill="{text_fill}">{text_content}</text>'

            svg += '</a>'

    if state["game_over"]:
        msg = "You Won! 🎉" if state["win"] else "Game Over 💣"
        svg += f'<rect x="0" y="{height / 2 - 20}" width="{width}" height="40" fill="rgba(0,0,0,0.7)"/>'
        svg += f'<text x="{width / 2}" y="{height / 2}" font-size="20" fill="white" class="cell-text">{msg}</text>'


    svg += '</svg>'
    
    with open('minesweeper.svg', 'w') as f:
        f.write(svg)
