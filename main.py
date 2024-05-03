from fastapi import FastAPI, HTTPException

import json
from model import Music, Composer


app = FastAPI()


## *** COMPOSERS ***

with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

composers: list[Composer] = []

for composer in composers_list:
    composers.append(Composer(**composer))


@app.get("/composers")
async def get_composer() -> list[Composer]:
    return composers


@app.post("/composers")
async def create_composer(composer: Composer) -> str:
    for ecomposer in composers:
        if ecomposer.composer_id == composer.composer_id:
            raise HTTPException(status_code=400, detail="Duplicate composer_id")

    composer.composer_id = len(composers) + 1
    composers.append(composer)
    return "Composer created successfully"


@app.put("/composers/{composer_id}")
async def update_composer(updated_composer: Composer, composer_id: int = None):
    for composer in composers:
        if composer.composer_id == composer_id:
            composer.name = updated_composer.name
            composer.home_country = updated_composer.home_country
            return "Composer updated successfully"
    new_composer = Composer(name=updated_composer.name, home_country=updated_composer.home_country, composer_id=composer_id)
    composers.append(new_composer)
    return "Composer created successfully"


@app.delete("/composers/{composer_id}")
async def delete_composer(composer_id: int) -> str:
    for i, composer in enumerate(composers):
        if composer.composer_id == composer_id:
            composers.pop(i)
            return "Composer deleted."


## *** MUSIC ***

with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)

pieces: list[Music] = []

for piece in piece_list:
    pieces.append(Music(**piece))

@app.get("/pieces")
async def get_pieces(composer_id: int = None) -> list[Music]:
    if composer_id is None:
        return pieces
    pieces_by_composer = []
    for piece in pieces:
        if piece.composer_id == composer_id:
            pieces_by_composer.append(piece)
    return pieces_by_composer


@app.post("/pieces")
async def create_peices(piece: Music):
    if piece.difficulty < 1 or piece.difficulty > 10:
        raise HTTPException(status_code=400, detail="Difficulty must be between 1 and 10")
    
    existing_composer_ids = []
    for music in pieces:
        existing_composer_ids.append(music.composer_id)

    if piece.composer_id not in existing_composer_ids:
        raise HTTPException(status_code=400, detail="Composer ID does not exsist.")
        
    pieces.append(piece)
    return "Piece added successfully"


@app.put("/pieces/{piece_name}")
async def update_pieces(piece_name: str, updated_piece: Music) -> None:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces[i] = updated_piece
        else:
            HTTPException(status_code=404, detail="Piece already exsists.")
    

@app.delete("/pieces/{piece_name}")
async def delete_piece(piece_name) -> str:
    for i, piece in enumerate(pieces):
        if piece.name == piece_name:
            pieces.pop(i)
            return "Piece deleted."
