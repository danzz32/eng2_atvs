# app/adapters/input/http/main.py

from fastapi import FastAPI

from app.adapters.output.persistence.database import engine, Base


# Importa os modelos para registrar as tabelas no metadata


def create_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.on_event("startup")
def startup_event():
    create_tables()
    print("Tabelas criadas com sucesso.")


# IMPORTANDO ROTAS DA API
from app.adapters.input.http.controllers import cliente_controller, jogo_controller, locacao_controller, \
    utilizacao_console_controller, console_controller

app.include_router(cliente_controller.router)
app.include_router(jogo_controller.router)
app.include_router(locacao_controller.router)
app.include_router(console_controller.router)
app.include_router(utilizacao_console_controller.router)
