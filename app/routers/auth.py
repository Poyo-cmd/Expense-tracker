from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import UsuarioCreate, UsuarioResponse, Token
from app.services.auth import registrar_usuario, autenticar_usuario, crear_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UsuarioResponse)
def register(datos: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return registrar_usuario(db, datos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(datos: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        usuario = autenticar_usuario(db, datos.email, datos.password)
        token = crear_token({"sub": usuario.email})
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))