# Guía de Despliegue en PythonAnywhere

Este documento detalla los pasos para desplegar la API de tasas de cambio en PythonAnywhere usando git clone desde la consola Bash.

## Requisitos Previos

- Cuenta en PythonAnywhere (cuenta gratuita o de pago)
- Repo git con el código de la API
- API Key de eltoque.com obtenida

---

## Paso 1: Preparar el Entorno local (Opcional)

Si aún no tienes el repo en GitHub:

```bash
# En tu máquina local
cd DashboardStore
git init
git add .
git commit -m "Initial commit: Flask API for eltoque tasas"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

---

## Paso 2: Acceder a PythonAnywhere

1. Ir a [pythonanywhere.com](https://www.pythonanywhere.com/)
2. Iniciar sesión con tus credenciales
3. Ir a la pestaña **Consoles** > **Bash**

---

## Paso 3: Clonar el Repositorio

En la consola Bash de PythonAnywhere:

```bash
# Navegar al directorio home
cd ~

# Clonar el repositorio (reemplazar con tu URL)
git clone https://github.com/TU_USUARIO/TU_REPO.git
```

---

## Paso 4: Crear Entorno Virtual

```bash
# Entrar al directorio del proyecto
cd ~/TU_REPO

# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
source venv/bin/activate

# Verificar que está activo (debería mostrar (venv) al inicio)
which python
```

---

## Paso 5: Instalar Dependencias

```bash
# Asegurarse de que el entorno virtual está activo
source ~/TU_REPO/venv/bin/activate

# Instalar las dependencias
pip install -r ~/TU_REPO/requirements.txt
```

---

## Paso 6: Configurar Variables de Entorno

### Opción A: Crear archivo .env

```bash
# Crear el archivo .env
nano ~/TU_REPO/.env
```

Agregar el siguiente contenido:

```env
ELTOQUE_API_KEY=tu_api_key_de_eltoque_aqui
API_KEY=tu_propia_api_key_para_clientes
ELTOQUE_API_URL=https://tasas.eltoque.com/api/v1
DEBUG=False
```

Guardar: `Ctrl + O`, `Enter`, `Ctrl + X`

### Opción B: Configurar en PythonAnywhere (Recomendado)

1. Ir a la pestaña **Web**
2. Click en la app (o crear una nueva)
3. Scroll hasta **Environment variables**
4. Agregar las variables:

| Variable | Valor |
|----------|-------|
| `ELTOQUE_API_KEY` | tu_api_key_de_eltoque |
| `API_KEY` | tu_api_key_personal |
| `ELTOQUE_API_URL` | https://tasas.eltoque.com/api/v1 |
| `DEBUG` | False |

---

## Paso 7: Configurar el WSGI

1. En la página **Web**, buscar **WSGI configuration file**
2. Click en el enlace para editar
3. Reemplazar el contenido con:

```python
import sys

# Añadir la ruta del proyecto al path
path = '/home/TU_USUARIO/TU_REPO'
if path not in sys.path:
    sys.path.append(path)

# Activar el entorno virtual
activate_this = '/home/TU_USUARIO/TU_REPO/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

# Importar y ejecutar la app
from run import app as application
```

**Importante:** Reemplazar `TU_USUARIO` y `TU_REPO` con tus datos reales.

Guardar el archivo.

---

## Paso 8: Configurar Archivos Estáticos (Opcional)

Si tienes archivos estáticos, en la página **Web**:

1. Ir a **Static files**
2. Agregar:
   - URL: `/static/`
   - Path: `/home/TU_USUARIO/TU_REPO/app/static/`

---

## Paso 9: Recargar la Aplicación

1. Ir a la pestaña **Web**
2. Click en el botón **Reload** (rojo/verde según el estado)
3. Esperar unos segundos

---

## Paso 10: Verificar el Despliegue

Probar los endpoints:

```bash
# Health check (sin autenticación)
curl https://TU_USUARIO.pythonanywhere.com/api/v1/salud

# Con autenticación
curl https://TU_USUARIO.pythonanywhere.com/api/v1/tasas \
  -H "X-API-Key: tu_api_key"
```

---

## Solución de Problemas

### Ver logs de errores

1. Ir a **Web** > **Logs**
2. Click en **Error log** para ver errores

### Errores comunes

**ModuleNotFoundError:**
- Verificar que las dependencias están instaladas en el venv
- Ejecutar `pip install -r requirements.txt` dentro del entorno virtual

**Import Error:**
- Verificar la ruta en el archivo WSGI
- Asegurarse de que `run.py` existe y tiene la variable `app`

**403 Forbidden:**
- Verificar que la API_KEY en .env coincide con la configurada
- Revisar que el header `X-API-Key` se envía correctamente

---

## Actualizar la Aplicación

Para actualizar cambios desde Git:

```bash
# En la consola Bash
cd ~/TU_REPO

# Traer cambios
git pull origin main

# Reactivar entorno virtual si es necesario
source venv/bin/activate

# Reinstalar dependencias si hay cambios en requirements.txt
pip install -r requirements.txt

# Recargar la app desde la página Web
```

---

## Configurar Tareas Programadas (Opcional)

Si necesitas tareas periódicas:

1. Ir a **Tasks**
2. Configurar el cron:
   - Siempre: `source ~/TU_REPO/venv/bin/activate && python ~/TU_REPO/run.py`

---

## Notas Adicionales

- La cuenta gratuita de PythonAnywhere solo funciona en el subdominio `tuusuario.pythonanywhere.com`
- El tráfico tiene límites en cuentas gratuitas
- La API de eltoque.com puede tener sus propios límites de uso
- Mantener las API Keys seguras y no exponerlas en el código público