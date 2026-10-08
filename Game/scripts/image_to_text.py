import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149,  99),
    32: (246, 124,  95),
    64: (246,  94,  59),
    128: (237, 207, 114),
    256: (237, 204,  97),
    512: (237, 200,  80),
    1024: (237, 197,  63),
    2048: (237, 194,  46),
    4096: (60,  58,  50), 
}

MAX_DIST = 40

def classify(pixel):
    pixel = np.array(pixel, dtype=float)
    best = min(COLORS, key=lambda k: np.linalg.norm(pixel - COLORS[k])) # basically returns number whose colors has the min vector difference with pixel color
    
    return best if np.linalg.norm(pixel - COLORS[best]) <= MAX_DIST else -1

def sample(image, x, y, r=2):
    
    arr = np.array(image.crop((x - r, y - r, x + r + 1, y + r + 1)))
    return tuple(np.median(arr.reshape(-1, 3), axis=0))

def ocr_dark_tile(image, box):
    
    try:
        import pytesseract
        from PIL import ImageOps
        cell = ImageOps.grayscale(image.crop(box)).resize((200, 200))
        cell = ImageOps.invert(cell)
        
        txt = pytesseract.image_to_string(cell, config="--psm 10 -c tessedit_char_whitelist=0123456789").strip()
        
        return int(txt) if txt.isdigit() else 4096
    except Exception:
        return 4096
    
def read_board(source, n=4):
    
    if isinstance(source, Image.Image):
        img = source.convert("RGB")
    else:
        img = Image.open(source).convert("RGB")
    
    w, h = img.size
    cw, ch = w / n, h / n
    board = []
    for r in range(n):
        row = []
        for c in range(n):
            # sample 4 points near the tile's corners, then take the majority vote
            votes = []
            for fx, fy in [(0.25, 0.2), (0.75, 0.2), (0.25, 0.8), (0.75, 0.8)]:
                x = int(c * cw + cw * fx)
                y = int(r * ch + ch * fy)
                votes.append(classify(sample(img, x, y, r=3)))
            val = max(set(votes), key=votes.count)

            if val in (0, 2, 4):
                cell = np.array(img.crop((int(c * cw + cw * 0.3), int(r * ch + ch * 0.3),
                                          int(c * cw + cw * 0.7), int(r * ch + ch * 0.7))))
                dark = np.mean(cell.sum(axis=2) < 450)  # digit color is ~ (119,110,101)
                val = 0 if dark < 0.02 else (2 if val == 0 else val)

            if val == 4096:
                box = (int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch))
                val = ocr_dark_tile(img, box)
            row.append(val)
        board.append(row)
    return img, board

def annotate(img, board, path):
    n = len(board)
    w, h = img.size
    cw, ch = w / n, h / n
    out = img.copy()
    d = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", min(10, int(ch * 0.11)))
    except OSError:
        font = ImageFont.load_default()
    for r in range(n):
        for c in range(n):
            v = board[r][c]
            label = "#?" if v == -1 else f"#{v}"
            cx, cy =  (c * cw + cw * 0.1) + 5, (r * ch + ch * 0.1) + 5
            d.rectangle([cx - cw * 0.1, cy - ch * 0.09, cx + cw * 0.1, cy + ch * 0.09],
                        fill=(0, 0, 0))
            d.text((cx, cy), label, fill=(255, 255, 255), font=font, anchor="mm")
    out.save(path)
    return out

def board_to_text(board):
    width = max(len(str(v)) for row in board for v in row)
    return "\n".join(" ".join(str(v).rjust(width) for v in row) for row in board)

images_folder = os.path.join(os.getcwd(), "Game", "sample_images")
annotated_folder = os.path.join(os.getcwd(), "Game", "annotated_images")

for image in os.listdir(images_folder):
    path = os.path.join(images_folder, image)
    number = image.split(".")[0].split("_")[-1]
    out_path = os.path.join(annotated_folder, f"annotated_image_{number}.png")
    
    img, board = read_board(path)
    _ = annotate(img, board, out_path)
    