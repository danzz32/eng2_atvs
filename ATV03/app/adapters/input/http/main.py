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

# Aqui você importa e inclui os routers conforme for criando os controllers
# Exemplo:
# from app.adapters.input.http.controllers import cliente_controller
# app.include_router(cliente_controller.router)
