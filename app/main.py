from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, categorias, transacciones, reportes
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="API para gestión de gastos personales",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(transacciones.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {"mensaje": "Expense Tracker API funcionando"}