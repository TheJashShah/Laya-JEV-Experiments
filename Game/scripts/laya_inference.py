from image_to_text import read_board, board_to_text

# import laya
# agent = laya.load("convaiinnovations/laya")

def ask_laya_prompt(agent, board, legal_moves):
    
    ALL_CRITERIA = {
        "up": "slide and merge all tiles upward",
        "down": "slide and merge all tiles downward",
        "left": "slide and merge all tiles to the left",
        "right": "slide and merge all tiles to the right",
    }
    
    questions = {
        "move": {
            "type": "choice",
            "instructions": f"Pick the best move for this 2048 board. Only these moves are legal for this position: {legal_moves}",
            "criteria": {m: ALL_CRITERIA[m] for m in legal_moves},
        }
    }
    
    result = agent.system_one(state=board, questions=questions)
    move = result["answers"]["move"]["choice"]
    
    return move



