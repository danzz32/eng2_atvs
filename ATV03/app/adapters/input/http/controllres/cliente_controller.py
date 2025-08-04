from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.adapters.output.persistence import database
from app.adapters.input.http.schemas.cliente_schema import ClienteCreate, ClienteOut
from app.domain.models.cliente import Cliente
from app.adapters.output.persistence.repositories.cliente_repository import ClienteRepository

router = APIRouter(prefix="/clientes", tags=["Clientes"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    repo = ClienteRepository(db)
    novo_cliente = Cliente(**cliente.model_dump())
    return repo.create(novo_cliente)


@router.get("/", response_model=list[ClienteOut])
def list_clientes(db: Session = Depends(get_db)):
    repo = ClienteRepository(db)
    return repo.get_all()


@router.get("/{cliente_id}", response_model=ClienteOut)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteOut)
def update_cliente(cliente_id: int, dados: ClienteCreate, db: Session = Depends(get_db)):
    repo = ClienteRepository(db)
    cliente = repo.update(cliente_id, dados.dict())
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    repo = ClienteRepository(db)
    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    repo.delete(cliente)
