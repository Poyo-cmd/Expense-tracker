from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.schemas.schemas import TransaccionCreate, TransaccionResponse
from app.models.models import Transaccion, TipoTransaccion
from app.dependencies import get_current_user

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.get("/", response_model=List[TransaccionResponse])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
    tipo: Optional[TipoTransaccion] = None,
    categoria_id: Optional[int] = None,
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None
):
    query = db.query(Transaccion).filter(Transaccion.usuario_id == usuario.id)
    if tipo:
        query = query.filter(Transaccion.tipo == tipo)
    if categoria_id:
        query = query.filter(Transaccion.categoria_id == categoria_id)
    if desde:
        query = query.filter(Transaccion.fecha >= desde)
    if hasta:
        query = query.filter(Transaccion.fecha <= hasta)
    return query.order_by(Transaccion.fecha.desc()).all()

@router.post("/", response_model=TransaccionResponse)
def crear(datos: TransaccionCreate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    datos_dict = datos.model_dump()
    datos_dict['fecha'] = datos_dict.get('fecha') or datetime.utcnow()
    transaccion = Transaccion(**datos_dict, usuario_id=usuario.id)
    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)
    return transaccion

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    transaccion = db.query(Transaccion).filter(Transaccion.id == id, Transaccion.usuario_id == usuario.id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    db.delete(transaccion)
    db.commit()
    return {"mensaje": "Transacción eliminada"}