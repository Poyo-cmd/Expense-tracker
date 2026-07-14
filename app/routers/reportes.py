from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime
import csv
import io
from fastapi.responses import StreamingResponse
from app.database import get_db
from app.models.models import Transaccion, Categoria, TipoTransaccion
from app.dependencies import get_current_user

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/resumen")
def resumen_mensual(
    año: int = Query(default=datetime.utcnow().year),
    mes: int = Query(default=datetime.utcnow().month),
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    query = db.query(Transaccion).filter(
        Transaccion.usuario_id == usuario.id,
        func.extract('year', Transaccion.fecha) == año,
        func.extract('month', Transaccion.fecha) == mes
    )
    transacciones = query.all()
    ingresos = sum(t.monto for t in transacciones if t.tipo == TipoTransaccion.ingreso)
    gastos = sum(t.monto for t in transacciones if t.tipo == TipoTransaccion.gasto)
    return {
        "año": año,
        "mes": mes,
        "ingresos": ingresos,
        "gastos": gastos,
        "balance": ingresos - gastos
    }

@router.get("/por-categoria")
def por_categoria(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    resultados = db.query(
        Categoria.nombre,
        func.sum(Transaccion.monto).label("total")
    ).join(Transaccion).filter(
        Transaccion.usuario_id == usuario.id,
        Transaccion.tipo == TipoTransaccion.gasto
    ).group_by(Categoria.nombre).all()

    return [{"categoria": r.nombre, "total": r.total} for r in resultados]

@router.get("/exportar-csv")
def exportar_csv(db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    transacciones = db.query(Transaccion).filter(Transaccion.usuario_id == usuario.id).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Descripción", "Monto", "Tipo", "Categoría", "Fecha"])
    for t in transacciones:
        writer.writerow([
            t.id, t.descripcion, t.monto, t.tipo.value,
            t.categoria.nombre if t.categoria else "",
            t.fecha.strftime("%Y-%m-%d")
        ])
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transacciones.csv"}
    )