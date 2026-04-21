# Portal de Viaticos de Benchmarking en IA

Aplicacion empresarial demo construida con Python Dash para gestionar el ciclo completo de viaticos de viajes de benchmarking en IA:

- solicitud
- aprobaciones
- generacion documental
- pagos
- legalizacion
- analitica ejecutiva
- apoyo documental con Gemini

El proyecto sigue una arquitectura por capas para que la UI no concentre la logica de negocio y quede listo para evolucionar hacia integraciones corporativas como Azure AD, SharePoint, SAP ECC HCM y automatizaciones posteriores.

## Estado del proyecto

La implementacion del plan definido en la especificacion ya esta completa del `Modulo 0` al `Modulo 11`.

- `Modulo 0`: bootstrap del proyecto y app Dash base
- `Modulo 1`: dominio, reglas, workflow y modelo de datos inicial
- `Modulo 2`: repositories, consultas de bandeja, auditoria y seed local
- `Modulo 3`: services de solicitud y aprobacion con contratos Pydantic
- `Modulo 4`: UI de Solicitud con formulario, callbacks y prueba e2e basica
- `Modulo 5`: UI de Aprobaciones con bandeja, timeline y acciones
- `Modulo 6`: integracion Gemini y apoyo documental con esquemas Pydantic
- `Modulo 7`: generacion documental y almacenamiento mock/local
- `Modulo 8`: pagos y notificacion estructurada con UI Dash
- `Modulo 9`: legalizacion financiera con UI Dash y calculos monetarios
- `Modulo 10`: dashboard ejecutivo con indicadores y visualizaciones
- `Modulo 11`: endurecimiento de configuracion, logging y placeholders corporativos

## Capacidades principales

- App Dash multipagina con `pages/`
- Navegacion lateral y encabezado profesional con Bootstrap
- Configuracion tipada con variables de entorno
- Dominio desacoplado de la UI
- Persistencia con SQLAlchemy
- SQLite local y base preparada para PostgreSQL
- Servicios de negocio para solicitud, aprobacion, pagos, legalizacion y dashboard
- Cliente Gemini con salida estructurada, validacion Pydantic y modo mock
- Generacion documental con plantillas Jinja2 y storage mock/local
- Logging estructurado con `correlation_id`
- Placeholders corporativos para AAD, SAP y notificaciones
- Suite de pruebas unitarias, integracion y e2e
- Validacion de calidad con `ruff`, `black` y `mypy`

## Stack tecnico

- `Dash`
- `dash-bootstrap-components`
- `dash-ag-grid`
- `SQLAlchemy`
- `Pydantic`
- `google-genai`
- `Jinja2`
- `pytest`
- `ruff`
- `black`
- `mypy`

## Requisitos

- Python `3.11` o superior

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## Configuracion

Variables relevantes de `.env`:

```env
APP_ENV=local
DEBUG=true
DATABASE_URL=sqlite:///./viaticos.db
LOG_LEVEL=INFO
DEFAULT_TIMEZONE=America/Bogota

ENABLE_GEMINI=true
GEMINI_MODE=mock
GEMINI_MODEL=gemini-3-flash-preview
GEMINI_API_KEY=

DOCUMENTS_STORAGE_PATH=./generated_documents

SHAREPOINT_MODE=mock
SAP_MODE=mock
AUTH_MODE=mock
ENABLE_CORPORATE_PLACEHOLDERS=true
```

Notas:

- En local, la app usa seed automatico cuando la base esta vacia.
- `GEMINI_MODE=mock` evita llamadas reales y deja la demo totalmente funcional.
- Si vas a usar Gemini real, cambia `GEMINI_MODE=live` y define `GEMINI_API_KEY`.

## Ejecucion

```bash
python run.py
```

La app queda disponible en:

- `http://127.0.0.1:8050`

## Recorrido rapido de la demo

Cuando levantas la aplicacion por primera vez:

- se inicializa la base local
- se cargan empleados y centros de costo demo
- se crea una solicitud en aprobaciones
- se crea una solicitud lista para pagos/legalizacion

Recorrido sugerido para probar el flujo:

1. En `Solicitud`, crea un borrador o radica una nueva solicitud.
2. En `Aprobaciones`, revisa la bandeja por rol y ejecuta aprobar, rechazar o devolver.
3. En `Pagos`, trabaja la solicitud lista para pago y registra notificacion y confirmacion.
4. En `Legalizacion`, agrega gastos, revisa diferencias y cierra la legalizacion.
5. En `Dashboard`, valida KPIs, SLA y comparativos operativos.

## Gemini

La integracion Gemini vive en [integrations/gemini_client.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/integrations/gemini_client.py) y esta pensada como apoyo documental controlado.

Casos implementados:

- extraccion estructurada de invitaciones
- clasificacion de documentos
- resumen de comentarios de aprobacion
- normalizacion de items de gasto

Seguridad operativa actual:

- feature flag para activar o desactivar Gemini
- modo mock para pruebas y demos
- validacion Pydantic de la salida
- sin llamadas reales en pruebas unitarias

## Calidad y pruebas

Comandos principales:

```bash
python -m pytest
python -m ruff check .
python -m black .
python -m mypy .
```

Estado actual del proyecto:

- `pytest`: pasa
- `ruff`: pasa
- `mypy`: pasa

## Estructura del proyecto

```text
.
├── app.py
├── run.py
├── assets/
├── callbacks/
├── components/
├── config/
├── database/
├── domain/
├── integrations/
├── pages/
├── repositories/
├── schemas/
├── services/
├── templates/
└── tests/
```

Responsabilidad por capa:

- `pages/`: layout por pagina
- `components/`: piezas reutilizables de UI
- `callbacks/`: orquestacion de eventos Dash
- `services/`: casos de uso y reglas aplicadas
- `repositories/`: acceso a datos
- `domain/`: estados, reglas y entidades
- `schemas/`: contratos Pydantic
- `integrations/`: Gemini y adapters externos
- `database/`: modelos, seed y sesion
- `templates/`: plantillas documentales
- `tests/`: unitarias, integracion y e2e

## Archivos clave

- [app.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/app.py)
- [config/settings.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/config/settings.py)
- [services/solicitud_service.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/services/solicitud_service.py)
- [services/aprobacion_service.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/services/aprobacion_service.py)
- [services/documentos_service.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/services/documentos_service.py)
- [services/pagos_service.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/services/pagos_service.py)
- [services/legalizacion_service.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/services/legalizacion_service.py)
- [services/dashboard_service.py](/c:/Users/JoseOrellana/OneDrive%20-%20K%20Lab%20Inc/Escritorio/universidadproyectoia/services/dashboard_service.py)

## Limitaciones actuales

- Es una demo funcional empresarial, no producto final.
- Las integraciones corporativas reales siguen como adapters mock o placeholders.
- El dashboard trabaja con la data local existente; no hay warehouse externo ni Power BI.
- La generacion documental es HTML con plantillas locales; no hay SharePoint real conectado.

## Siguientes pasos recomendados

- Conectar autenticacion real con Azure AD
- Reemplazar adapters mock de SharePoint, SAP y notificaciones
- Agregar migraciones formales
- Endurecer autorizacion por rol dentro de la UI
- Incorporar background jobs para tareas pesadas
- Preparar despliegue en entorno corporativo
