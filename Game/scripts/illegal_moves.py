def slide_left(row):
    
    tiles = [v for v in row if v != 0]
    out, i = [], 0
    
    while i < len(tiles):
        
        if (i + 1) < len(tiles) and tiles[i] == tiles[i + 1]:
            out.append(tiles[i] * 2)
            i += 2
        
        else:
            out.append(tiles[i])
            i += 1
            
    return out + [0] * (4 - len(out))

def apply_move(board, move):
    b = [list(r) for r in board]
    
    if move == "left":
        return [slide_left(r) for r in b]
    
    if move == "right":
        return [slide_left(r[::-1])[::-1] for r in b]
    
    cols = [list(c) for c in zip(*b)]
    
    if move == "up":
        cols = [slide_left(c) for c in cols]
        
    elif move == "down":
        cols = [slide_left(c[::-1])[::-1] for c in cols]
        
    return [list(r) for r in zip(*cols)]

def legal_moves(board):
    return [m for m in ("down", "left", "right", "up") if apply_move(board, m) != [list(r) for r in board]]