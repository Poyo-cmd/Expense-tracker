from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.schemas import CategoriaCreate, CategoriaResponse
from app.models.models import Categoria
from app.dependencies import get_current_user

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/", response_model=List[CategoriaResponse])
def listar(db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    return db.query(Categoria).filter(Categoria.usuario_id == usuario.id).all()

@router.post("/", response_model=CategoriaResponse)
def crear(datos: CategoriaCreate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    categoria = Categoria(**datos.model_dump(), usuario_id=usuario.id)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    categoria = db.query(Categoria).filter(Categoria.id == id, Categoria.usuario_id == usuario.id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()
    return {"mensaje": "Categoría eliminada"}