# Documentación de API - El Toque Service

## Endpoints Disponibles

### 1. Endpoint Principal para Clientes

**GET** `/v1/trmi`

Endpoint único para consultar tasas de cambio históricas con validación de tiempo.

#### Autenticación
- **Header requerido:** `X-API-Key`
- Valor: La API KEY asignada al cliente (configurada en variable de entorno `API_KEY`)

#### Parámetros (Query String)
| Parámetro | Tipo | Obligatorio | Descripción |
|-----------|------|-------------|-------------|
| date_from | string | Sí | Fecha de inicio (formato: `YYYY-MM-DD HH:MM:SS`) |
| date_to | string | Sí | Fecha de fin (formato: `YYYY-MM-DD HH:MM:SS`) |

#### Restricciones
- El rango entre `date_from` y `date_to` no puede exceder **24 horas**
- Formato de fecha obligatorio: `YYYY-MM-DD HH:MM:SS`

#### Respuesta Exitosa (200)
```json
{
  "success": true,
  "data": [...]
}
```

#### Respuestas de Error
- **400:** Parámetros faltantes o rango mayor a 24 horas
- **401:** API Key no proporcionada
- **403:** API Key inválida
- **500:** Error del servidor

#### Ejemplo de CURL
```bash
curl -X 'GET' \
  'https://tu-dominio.pythonanywhere.com/v1/trmi?date_from=2026-04-28%2000%3A00%3A01&date_to=2026-04-28%2023%3A59%3A01' \
  -H 'accept: */*' \
  -H 'X-API-Key: tu_api_key_del_cliente'
```

---

### 2. Health Check

**GET** `/v1/salud`

No requiere autenticación.

#### Respuesta
```json
{
  "status": "ok",
  "message": "API funcionando correctamente"
}
```

---

## Configuración de Variables de Entorno

Para producción (PythonAnywhere), configurar:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `ELTOQUE_API_KEY` | Token JWT de El Toque (para consultas internas) | `eyJhbGci...` |
| `API_KEY` | API Key para autenticar clientes | `mi_api_key_secreta` |
| `ELTOQUE_API_URL` | URL de la API de El Toque | `https://tasas.eltoque.com/api/v1` |
| `DEBUG` | Modo debug | `False` |

---

## Arquitectura

```
[Cliente App] --> (X-API-Key) --> [Esta API] --> (Bearer Token) --> [API El Toque]
```

- Los clientes se autentican con `X-API-Key` (API KEY propia)
- Esta API usa `ELTOQUE_API_KEY` internamente para consultar a El Toque