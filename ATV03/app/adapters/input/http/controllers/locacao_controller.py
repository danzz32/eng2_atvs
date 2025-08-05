from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.adapters.output.persistence import database
from app.adapters.input.http.schemas.locacao_schema import LocacaoOut, LocacaoCreate
from app.domain.models.locacao import Locacao

from app.adapters.output.persistence.repositories.locacao_repository import LocacaoRepository
from app.adapters.output.persistence.repositories.cliente_repository import ClienteRepository
from app.adapters.output.persistence.repositories.item_locacao_repository import ItemLocacaoRepository
from app.adapters.output.persistence.repositories.jogo_plataforma_repository import JogoPlataformaRepository
from app.adapters.output.persistence.repositories.jogo_repository import JogoRepository
from app.adapters.output.persistence.repositories.plataforma_repository import PlataformaRepository

from app.domain.services.locacao_service import LocacaoService

router = APIRouter(prefix="/locacoes", tags=["Locações"])


@router.post("/", response_model=LocacaoOut, status_code=status.HTTP_201_CREATED)
def create_locacao(locacao_data: LocacaoCreate, db: Session = Depends(database.get_db)):
    # Instanciar os repositórios necessários
    locacao_repo = LocacaoRepository(db)
    cliente_repo = ClienteRepository(db)
    item_locacao_repo = ItemLocacaoRepository(db)
    jogo_plataforma_repo = JogoPlataformaRepository(db)
    jogo_repo = JogoRepository(db)
    plataforma_repo = PlataformaRepository(db)

    # Instanciar o serviço
    service = LocacaoService(
        locacao_repository=locacao_repo,
        cliente_repository=cliente_repo,
        item_locacao_repository=item_locacao_repo,
        jogo_plataforma_repository=jogo_plataforma_repo,
        plataforma_repository=plataforma_repo,
        jogo_repository=jogo_repo,
    )

    try:
        nova_locacao = service.criar_locacao(cliente_id=locacao_data.cliente_id)
        return nova_locacao
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[LocacaoOut])
def list_locacoes(db: Session = Depends(database.get_db)):
    repo = LocacaoRepository(db)
    return repo.get_all()


@router.get("/{locacao_id}", response_model=LocacaoOut)
def get_locacao(locacao_id: int, db: Session = Depends(database.get_db)):
    repo = LocacaoRepository(db)
    locacao = repo.get_by_id(locacao_id)
    if not locacao:
        raise HTTPException(status_code=404, detail="Locação não encontrada")
    return locacao


@router.put("/{locacao_id}", response_model=LocacaoOut)
def update_locacao(locacao_id: int, dados: LocacaoCreate, db: Session = Depends(database.get_db)):
    repo = LocacaoRepository(db)
    locacao = repo.get_by_id(locacao_id)
    if not locacao:
        raise HTTPException(status_code=404, detail="Locação não encontrada")

    locacao_atualizada = repo.update(locacao, dados.model_dump())
    return locacao_atualizada


@router.delete("/{locacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_locacao(locacao_id: int, db: Session = Depends(database.get_db)):
    repo = LocacaoRepository(db)
    locacao = repo.get_by_id(locacao_id)
    if not locacao:
        raise HTTPException(status_code=404, detail="Locação não encontrada")
    repo.delete(locacao)
