from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.adapters.output.persistence import database
from app.domain.models.jogo import Jogo
from app.adapters.input.http.schemas.jogo_schema import JogoCreate, JogoOut
from app.adapters.output.persistence.repositories.jogo_repository import JogoRepository

router = APIRouter(prefix="/jogos", tags=["Jogos"])


@router.post("/", response_model=JogoOut, status_code=status.HTTP_201_CREATED)
def create_jogo(jogo_data: JogoCreate, db: Session = Depends(database.get_db)):
    repo = JogoRepository(db)
    novo_jogo = Jogo(**jogo_data.model_dump())
    return repo.create(novo_jogo)


@router.get("/", response_model=List[JogoOut])
def list_jogos(db: Session = Depends(database.get_db)):
    repo = JogoRepository(db)
    return repo.get_all()


@router.get("/{jogo_id}", response_model=JogoOut)
def get_jogo(jogo_id: int, db: Session = Depends(database.get_db)):
    repo = JogoRepository(db)
    jogo = repo.get_by_id(jogo_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo


@router.put("/{jogo_id}", response_model=JogoOut)
def update_jogo(jogo_id: int, jogo_data: JogoCreate, db: Session = Depends(database.get_db)):
    repo = JogoRepository(db)
    jogo_atualizado = repo.update(jogo_id, jogo_data.model_dump())
    if not jogo_atualizado:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo_atualizado


@router.delete("/{jogo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_jogo(jogo_id: int, db: Session = Depends(database.get_db)):
    repo = JogoRepository(db)
    jogo = repo.get_by_id(jogo_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    repo.delete(jogo)  # <-- passe o objeto, não o id
