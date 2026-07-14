from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
from app.models.models import Usuario
from app.schemas.schemas import UsuarioCreate
from app.config import settings

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def crear_token(data: dict) -> str:
    payload = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def obtener_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def registrar_usuario(db: Session, datos: UsuarioCreate):
    if obtener_usuario_por_email(db, datos.email):
        raise ValueError("El email ya está registrado")
    usuario = Usuario(
        email=datos.email,
        password=hash_password(datos.password),
        nombre=datos.nombre
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def autenticar_usuario(db: Session, email: str, password: str):
    usuario = obtener_usuario_por_email(db, email)
    if not usuario or not verify_password(password, usuario.password):
        raise ValueError("Credenciales incorrectas")
    return usuario

def obtener_usuario_actual(db: Session, token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise ValueError("Token inválido")
        return obtener_usuario_por_email(db, email)
    except JWTError:
        raise ValueError("Token inválido")