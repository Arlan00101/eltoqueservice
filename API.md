# API de Tasas de Cambio eltoque.com

API Flask que expoen las tasas de cambio del mercado cubano desde la API de eltoque.com.

## Requisitos

- Python 3.9+
- pip

## Instalación Local

```bash
# Clonar el repositorio
git clone <tu-repo-url>
cd DashboardStore

# Crear entorno virtual
python -m venv venv
# En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus API keys

# Ejecutar
python run.py
```

## Configuración

Editar el archivo `.env`:

| Variable | Descripción |
|----------|-------------|
| `ELTOQUE_API_KEY` | API Key de eltoque.com (solicitar en su sitio) |
| `API_KEY` | Tu propia API Key para autenticar clientes |
| `ELTOQUE_API_URL` | URL de la API de eltoque (por defecto ya configurada) |
| `DEBUG` | True/False para modo desarrollo |

## Endpoints

Todos los endpoints requieren autenticación via header `X-API-Key`.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/salud` | Health check (sin auth) |
| GET | `/api/v1/tasas` | Todas las tasas (informal + oficial) |
| GET | `/api/v1/tasas/informal` | Tasas mercado informal |
| GET | `/api/v1/tasas/oficial` | Tasas mercado oficial |
| GET | `/api/v1/tasas/historico?fecha_inicio=YYYY-MM-DD&fecha_fin=YYYY-MM-DD&tipo=informal` | Histórico |

### Ejemplo de request

```bash
curl -X GET http://localhost:5000/api/v1/tasas -H "X-API-Key: tu_api_key_aqui"
```

### Respuesta exitosa

```json
{
  "success": true,
  "data": {
    "informal": { ... },
    "oficial": { ... }
  }
}
```

## Desarrollo

```bash
# Ejecutar tests
pytest

# Ejecutar en modo desarrollo
python run.py
```