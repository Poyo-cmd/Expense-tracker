from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.models import TipoTransaccion

class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str

class UsuarioResponse(BaseModel):
    id: int
    email: str
    nombre: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CategoriaCreate(BaseModel):
    nombre: str
    color: Optional[str] = "#6366f1"

class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    color: str

    class Config:
        from_attributes = True

class TransaccionCreate(BaseModel):
    descripcion: str
    monto: float
    tipo: TipoTransaccion
    fecha: Optional[datetime] = None
    categoria_id: Optional[int] = None

class TransaccionResponse(BaseModel):
    id: int
    descripcion: str
    monto: float
    tipo: TipoTransaccion
    fecha: datetime
    categoria: Optional[CategoriaResponse] = None

    class Config:
        from_attributes = True