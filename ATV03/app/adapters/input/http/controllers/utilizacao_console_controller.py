from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.adapters.output.persistence.database import get_db
from app.adapters.output.persistence.repositories.utilizacao_console_repository import UtilizacaoConsoleRepository
from app.adapters.output.persistence.repositories.console_repository import ConsoleRepository
from app.domain.services.utilizacao_console_service import UtilizacaoConsoleService
from app.domain.models.utilizacao_console import UtilizacaoDoConsolePeloCliente
from app.adapters.input.http.schemas.utilizacao_console_schema import UtilizacaoConsoleCreate, UtilizacaoConsoleOut

router = APIRouter(prefix="/utilizacoes", tags=["Utilização do Console"])


def get_service(db: Session) -> UtilizacaoConsoleService:
    utilizacao_repo = UtilizacaoConsoleRepository(db)
    console_repo = ConsoleRepository(db)
    return UtilizacaoConsoleService(utilizacao_repo, console_repo)


@router.post("/", response_model=UtilizacaoConsoleOut, status_code=status.HTTP_201_CREATED)
def iniciar_utilizacao(uso_data: UtilizacaoConsoleCreate, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        uso = service.iniciar_utilizacao(cliente_id=uso_data.cliente_id, console_id=uso_data.console_id)
        return uso
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{uso_id}/finalizar", response_model=float)
def finalizar_utilizacao(uso_id: int, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        custo_total = service.finalizar_utilizacao(utilizacao_id=uso_id)
        return custo_total
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[UtilizacaoConsoleOut])
def listar_utilizacoes(db: Session = Depends(get_db)):
    service = get_service(db)
    return service.utilizacao_repo.get_all()


@router.get("/{uso_id}", response_model=UtilizacaoConsoleOut)
def buscar_utilizacao(uso_id: int, db: Session = Depends(get_db)):
    service = get_service(db)
    uso = service.utilizacao_repo.get_by_id(uso_id)
    if not uso:
        raise HTTPException(status_code=404, detail="Utilização não encontrada")
    return uso


@router.delete("/{uso_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_utilizacao(uso_id: int, db: Session = Depends(get_db)):
    service = get_service(db)
    uso = service.utilizacao_repo.get_by_id(uso_id)
    if not uso:
        raise HTTPException(status_code=404, detail="Utilização não encontrada")
    service.utilizacao_repo.delete(uso)
