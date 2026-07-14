# Expense Tracker API

API REST para gestión de gastos personales construida con Python y FastAPI.

## Tech Stack

- **Python 3.13** + **FastAPI**
- **PostgreSQL** — persistencia de datos
- **SQLAlchemy** — ORM
- **JWT** — autenticación
- **Docker** + **Docker Compose** — contenerización
- **Swagger / OpenAPI** — documentación interactiva

## Requisitos

- Docker Desktop

## Levantar el proyecto

```bash
docker compose up --build
```

La API estará en `http://localhost:8000`  
La documentación Swagger en `http://localhost:8000/docs`

## Endpoints

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar usuario |
| POST | `/auth/login` | Iniciar sesión |

### Categorías (requiere JWT)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/categorias/` | Listar categorías |
| POST | `/categorias/` | Crear categoría |
| DELETE | `/categorias/{id}` | Eliminar categoría |

### Transacciones (requiere JWT)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/transacciones/` | Listar con filtros |
| POST | `/transacciones/` | Crear transacción |
| DELETE | `/transacciones/{id}` | Eliminar transacción |

### Reportes (requiere JWT)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/reportes/resumen` | Resumen mensual |
| GET | `/reportes/por-categoria` | Gastos por categoría |
| GET | `/reportes/exportar-csv` | Exportar CSV |

## Ejemplo de uso

**Registrarse:**
```json
POST /auth/register
{
  "email": "usuario@email.com",
  "password": "123456",
  "nombre": "Usuario"
}
```

**Crear transacción:**
```json
POST /transacciones/
Authorization: Bearer {token}

{
  "descripcion": "Supermercado",
  "monto": 25000,
  "tipo": "gasto",
  "categoria_id": 1
}
```

## Características

- Filtros por tipo, categoría y rango de fechas
- Resumen mensual con balance de ingresos y gastos
- Gastos agrupados por categoría
- Exportación de transacciones en CSV