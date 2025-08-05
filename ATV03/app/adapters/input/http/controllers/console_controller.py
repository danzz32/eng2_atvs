from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.adapters.output.persistence.database import get_db
from app.adapters.output.persistence.repositories.console_repository import ConsoleRepository
from app.adapters.input.http.schemas.console_schema import ConsoleCreate, ConsoleOut
from app.domain.models import Console

router = APIRouter(prefix="/consoles", tags=["Consoles"])


@router.post("/", response_model=ConsoleOut, status_code=status.HTTP_201_CREATED)
def criar_console(console_data: ConsoleCreate, db: Session = Depends(get_db)):
    repo = ConsoleRepository(db)
    novo_console = Console(nome=console_data.nome, preco_por_hora=console_data.preco_por_hora)
    criado = repo.create(novo_console)
    return criado


@router.get("/", response_model=List[ConsoleOut])
def listar_consoles(db: Session = Depends(get_db)):
    repo = ConsoleRepository(db)
    consoles = repo.get_all()
    return consoles


@router.get("/{console_id}", response_model=ConsoleOut)
def buscar_console(console_id: int, db: Session = Depends(get_db)):
    repo = ConsoleRepository(db)
    console = repo.get_by_id(console_id)
    if not console:
        raise HTTPException(status_code=404, detail="Console não encontrado")
    return console


@router.put("/{console_id}", response_model=ConsoleOut)
def atualizar_console(console_id: int, console_data: ConsoleCreate, db: Session = Depends(get_db)):
    repo = ConsoleRepository(db)
    console = repo.get_by_id(console_id)
    if not console:
        raise HTTPException(status_code=404, detail="Console não encontrado")

    console.nome = console_data.nome
    console.preco_por_hora = console_data.preco_por_hora

    atualizado = repo.update(console)
    return atualizado


@router.delete("/{console_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_console(console_id: int, db: Session = Depends(get_db)):
    repo = ConsoleRepository(db)
    console = repo.get_by_id(console_id)
    if not console:
        raise HTTPException(status_code=404, detail="Console não encontrado")

    repo.delete(console)
