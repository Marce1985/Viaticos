# Especificación para Codex — Portal de Viáticos de Benchmarking en IA (Python Dash + Gemini API)

## 1\) Objetivo

Construir una aplicación web empresarial en **Python Dash** para gestionar el ciclo completo de viáticos de viajes de benchmarking en IA: **solicitud, aprobaciones, generación documental, notificación a pagos, legalización y analítica operativa**.

La implementación debe:

* seguir una **arquitectura recomendada para Dash**;
* usar la **API de Gemini** para apoyo documental y extracción/validación asistida;
* desarrollarse **paso a paso, módulo por módulo**;
* incluir **pruebas unitarias** desde el inicio;
* dejar la base lista para integrarse luego con **Azure AD/SSO, SharePoint, SAP ECC HCM, Power Automate y Power BI**.

\---

## 2\) Principios de arquitectura

### 2.1 Arquitectura recomendada para Dash

Adoptar una estructura **multi-page con `pages/`**, separando:

* **UI / layout**
* **callbacks**
* **servicios de aplicación**
* **dominio**
* **persistencia**
* **integraciones externas**

### 2.2 Reglas de diseño

1. **No meter lógica de negocio compleja dentro de los callbacks**.
2. Los callbacks deben delegar a **services/**.
3. El acceso a datos debe vivir en **repositories/**.
4. Las entidades y reglas de negocio deben vivir en **domain/**.
5. Las integraciones externas (Gemini, SharePoint, SAP, correo) deben vivir en **integrations/**.
6. Toda regla importante debe tener **tests unitarios**.
7. La app debe poder correr primero en modo **mock/local** y luego en modo corporativo.
8. La configuración debe venir por **variables de entorno**.

\---

## 3\) Stack técnico base

* **Frontend web**: Dash
* **Componentes UI**: dash, dash-bootstrap-components
* **Tablas**: dash-ag-grid
* **Backend HTTP opcional**: Flask/FastAPI para endpoints auxiliares
* **ORM / acceso a datos**: SQLAlchemy
* **Base de datos**: PostgreSQL (producción) / SQLite (local)
* **Validación de datos**: Pydantic
* **IA**: Google GenAI SDK (Gemini API)
* **Pruebas unitarias**: pytest
* **Pruebas de app Dash**: dash\[testing]
* **Calidad**: ruff, black, mypy
* **Plantillas documentos**: python-docx / Jinja2 / WeasyPrint o reportlab
* **Autenticación futura**: Azure AD / OIDC
* **Observabilidad**: logging estructurado

\---

## 4\) Estructura del proyecto

```text
viaticos\_app/
├─ app.py
├─ run.py
├─ pyproject.toml
├─ requirements.txt
├─ .env.example
├─ README.md
├─ assets/
│  ├─ styles.css
│  └─ theme.css
├─ config/
│  ├─ settings.py
│  └─ logging.py
├─ pages/
│  ├─ home.py
│  ├─ solicitud.py
│  ├─ aprobaciones.py
│  ├─ pagos.py
│  ├─ legalizacion.py
│  └─ dashboard.py
├─ components/
│  ├─ navbar.py
│  ├─ sidebar.py
│  ├─ forms.py
│  ├─ tables.py
│  ├─ timeline.py
│  └─ alerts.py
├─ callbacks/
│  ├─ solicitud\_callbacks.py
│  ├─ aprobaciones\_callbacks.py
│  ├─ pagos\_callbacks.py
│  ├─ legalizacion\_callbacks.py
│  └─ dashboard\_callbacks.py
├─ domain/
│  ├─ enums.py
│  ├─ entities.py
│  ├─ rules.py
│  ├─ workflows.py
│  └─ value\_objects.py
├─ services/
│  ├─ solicitud\_service.py
│  ├─ aprobacion\_service.py
│  ├─ documentos\_service.py
│  ├─ pagos\_service.py
│  ├─ legalizacion\_service.py
│  ├─ auditoria\_service.py
│  └─ dashboard\_service.py
├─ repositories/
│  ├─ base.py
│  ├─ solicitud\_repository.py
│  ├─ aprobacion\_repository.py
│  ├─ pago\_repository.py
│  ├─ legalizacion\_repository.py
│  └─ catalog\_repository.py
├─ integrations/
│  ├─ gemini\_client.py
│  ├─ sharepoint\_client.py
│  ├─ sap\_client.py
│  ├─ aad\_client.py
│  └─ notification\_client.py
├─ schemas/
│  ├─ solicitud\_schema.py
│  ├─ aprobacion\_schema.py
│  ├─ pago\_schema.py
│  └─ legalizacion\_schema.py
├─ database/
│  ├─ models.py
│  ├─ session.py
│  ├─ migrations/
│  └─ seed.py
├─ docs/
│  ├─ architecture.md
│  ├─ api\_contracts.md
│  └─ prompts\_codex.md
└─ tests/
   ├─ unit/
   │  ├─ test\_rules.py
   │  ├─ test\_workflows.py
   │  ├─ test\_solicitud\_service.py
   │  ├─ test\_aprobacion\_service.py
   │  ├─ test\_pagos\_service.py
   │  ├─ test\_legalizacion\_service.py
   │  └─ test\_gemini\_client.py
   ├─ integration/
   │  ├─ test\_repositories.py
   │  └─ test\_document\_generation.py
   └─ e2e/
      └─ test\_smoke\_dash.py
```

\---

## 5\) Modelo funcional del proceso

### Estados del trámite

```text
BORRADOR
RADICADA
EN\_APROBACION\_JEFE
EN\_VALIDACION\_GH
EN\_VALIDACION\_PRESUPUESTO
EN\_VALIDACION\_COMPRAS
EN\_VALIDACION\_SEGURIDAD\_TI
EN\_VALIDACION\_JURIDICA
APROBADA\_PARA\_PAGO
PAGO\_NOTIFICADO
PAGO\_CONFIRMADO
EN\_LEGALIZACION
LEGALIZADA
CERRADA
RECHAZADA
DEVUELTA\_A\_AJUSTES
```

### Reglas iniciales

1. Si `requiere\_tiquetes = true` -> pasa por Compras.
2. Si `requiere\_herramienta\_externa = true` -> pasa por Seguridad TI.
3. Si `requiere\_nda = true` -> pasa por Jurídica.
4. Si `destino\_internacional = true` -> exige moneda, tasa referencial y documentos extra.
5. Si falta centro de costo o jefe -> no permite radicar.
6. Si la solicitud supera umbral monetario configurable -> exige aprobación adicional.
7. Ningún pago se notifica si el workflow no está completamente aprobado.
8. La legalización compara:

   * valor aprobado
   * anticipo girado
   * valor soportado
   * saldo a favor / reintegro

\---

## 6\) Modelo de datos mínimo

### Tablas principales

* `employees`
* `cost\_centers`
* `travel\_requests`
* `approval\_steps`
* `approval\_events`
* `documents`
* `payment\_orders`
* `payment\_notifications`
* `expense\_reports`
* `expense\_items`
* `audit\_log`

### Campos críticos por solicitud

* id
* request\_code
* employee\_id
* manager\_id
* cost\_center\_id
* destination
* country
* start\_date
* end\_date
* travel\_purpose
* requires\_tickets
* requires\_external\_tools
* requires\_nda
* estimated\_amount
* currency
* status
* created\_at
* updated\_at

\---

## 7\) Integración con Gemini API

## Objetivo de Gemini en esta solución

Gemini NO debe decidir aprobaciones financieras. Debe usarse como apoyo controlado para:

1. **extraer campos** desde invitaciones o documentos adjuntos;
2. **clasificar documentos**;
3. **resumir observaciones**;
4. **validar consistencia documental preliminar**;
5. **proponer borradores** de cartas o cláusulas;
6. **normalizar conceptos de facturas** en la legalización.

## Reglas de seguridad

* No enviar secretos.
* Enmascarar datos sensibles cuando aplique.
* Registrar prompts/respuestas de manera controlada.
* Implementar `feature\_flag` para activar/desactivar IA.
* Toda salida IA debe pasar por validación de esquema.

## Cliente Gemini

Crear `integrations/gemini\_client.py` con:

* lectura de `GEMINI\_API\_KEY` desde entorno;
* método `generate\_structured(...)`;
* soporte para respuestas JSON validadas con Pydantic;
* timeouts, retries y manejo de errores;
* un modo `mock` para pruebas.

### Casos de uso concretos

* `extract\_invitation\_data(file\_text) -> InvitationData`
* `classify\_supporting\_document(text) -> DocumentClassification`
* `summarize\_approval\_comments(comments) -> ApprovalSummary`
* `normalize\_expense\_item(raw\_text) -> NormalizedExpense`

\---

## 8\) Arquitectura lógica

```text
\[ Usuario / Rol ]
       |
       v
\[ Dash Pages UI ]
       |
       v
\[ Callbacks ]
       |
       v
\[ Services ]
   |      |       |
   |      |       +--> \[Integrations: Gemini / SharePoint / SAP / AAD / Mail]
   |      |
   |      +----------> \[Repositories]
   |                         |
   |                         v
   +--------------------> \[PostgreSQL / SQLite]
```

\---

## 9\) Convenciones de implementación

1. `pages/` define layout por página.
2. `callbacks/` solo orquesta inputs/outputs.
3. `services/` concentra casos de uso.
4. `domain/` define reglas y estados.
5. `repositories/` encapsula SQLAlchemy.
6. `schemas/` define contratos de entrada/salida.
7. `integrations/` aísla proveedores externos.
8. Los IDs de componentes Dash deben centralizarse cuando crezcan.
9. No usar variables globales mutables para compartir estado.
10. Las cargas pesadas deben estar preparadas para background jobs.

\---

## 10\) Plan de construcción para Codex

# Módulo 0 — Bootstrap del proyecto

### Objetivo

Crear la base del repositorio y dejar la app corriendo con navegación mínima.

### Entregables

* `pyproject.toml`
* `requirements.txt`
* `app.py`, `run.py`
* `pages/home.py`
* `config/settings.py`
* `database/session.py`
* `README.md`
* `tests/e2e/test\_smoke\_dash.py`

### Tareas

1. Inicializar proyecto Python.
2. Configurar Dash con Bootstrap.
3. Activar Dash Pages.
4. Crear navbar/sidebar base.
5. Configurar settings por variables de entorno.
6. Agregar logging.
7. Agregar test smoke que verifique que la app levanta.

### Criterios de aceptación

* La app abre localmente.
* Existe menú lateral.
* Existe página Home.
* `pytest` corre sin errores.

### Prompt para Codex

```text
Implementa el Módulo 0 del proyecto "Portal de Viáticos de Benchmarking en IA" usando Python Dash con arquitectura por capas.
Requisitos:
- Usar Dash Pages.
- Crear estructura de carpetas indicada en la especificación.
- Configurar app.py y run.py.
- Agregar configuración por .env.
- Agregar prueba smoke con pytest/dash testing.
- No implementes todavía lógica de negocio.
- Entrega código listo para ejecutar.
```

\---

# Módulo 1 — Dominio y modelo de datos

### Objetivo

Definir entidades, enums, reglas básicas y tablas SQLAlchemy.

### Entregables

* `domain/enums.py`
* `domain/entities.py`
* `domain/rules.py`
* `domain/workflows.py`
* `database/models.py`
* `tests/unit/test\_rules.py`
* `tests/unit/test\_workflows.py`

### Tareas

1. Definir enum de estados del trámite.
2. Definir roles del proceso.
3. Modelar solicitud, aprobación, pago, documento, legalización.
4. Implementar reglas de enrutamiento.
5. Crear máquina de estados básica.
6. Crear tests unitarios para reglas y transiciones.

### Criterios de aceptación

* Las reglas de negocio no dependen de Dash.
* Los tests validan rutas condicionales.
* Las transiciones inválidas fallan con excepción clara.

### Prompt para Codex

```text
Implementa el Módulo 1.
Necesito el dominio y el modelo de datos para una app de viáticos.
Incluye:
- enums de estado y rol
- reglas de enrutamiento condicional
- workflow / state machine
- modelos SQLAlchemy
- pruebas unitarias para reglas y transiciones
No implementes UI todavía.
```

\---

# Módulo 2 — Repositorios y persistencia

### Objetivo

Crear la capa de acceso a datos desacoplada del dominio.

### Entregables

* `repositories/\*.py`
* `database/seed.py`
* `tests/integration/test\_repositories.py`

### Tareas

1. Crear repositories CRUD.
2. Agregar queries para bandejas por rol.
3. Agregar consulta de timeline / auditoría.
4. Crear seed con datos mock.
5. Crear pruebas de integración con SQLite temporal.

### Criterios de aceptación

* Repositories no conocen Dash.
* Pruebas pasan contra base temporal.
* Existe método para obtener solicitudes por estado y rol.

### Prompt para Codex

```text
Implementa el Módulo 2 creando repositories desacoplados usando SQLAlchemy.
Incluye seed local y pruebas de integración con SQLite in-memory o temporal.
Necesito queries para:
- crear solicitud
- consultar solicitud por id
- listar solicitudes por estado
- listar bandeja por rol
- guardar eventos de auditoría
```

\---

# Módulo 3 — Servicios de solicitud y aprobación

### Objetivo

Implementar los casos de uso centrales del proceso.

### Entregables

* `services/solicitud\_service.py`
* `services/aprobacion\_service.py`
* `services/auditoria\_service.py`
* `schemas/solicitud\_schema.py`
* `schemas/aprobacion\_schema.py`
* `tests/unit/test\_solicitud\_service.py`
* `tests/unit/test\_aprobacion\_service.py`

### Tareas

1. Crear servicio para guardar borrador.
2. Crear servicio para radicar solicitud.
3. Validar campos obligatorios.
4. Calcular ruta de aprobaciones según reglas.
5. Crear servicio de aprobar/rechazar/devolver.
6. Registrar auditoría por evento.

### Criterios de aceptación

* Al radicar, se crean los pasos correctos.
* Cada aprobación cambia el estado.
* Toda acción deja huella en auditoría.

### Prompt para Codex

```text
Implementa el Módulo 3 con servicios de negocio.
Necesito:
- guardar borrador
- radicar solicitud
- calcular workflow de aprobaciones
- aprobar, rechazar o devolver
- registrar auditoría
Incluye pruebas unitarias y usa Pydantic para contratos.
```

\---

# Módulo 4 — UI de Solicitud (Dash)

### Objetivo

Crear la primera experiencia visible de usuario.

### Entregables

* `pages/solicitud.py`
* `components/forms.py`
* `callbacks/solicitud\_callbacks.py`
* `tests/e2e/test\_solicitud\_form.py`

### Tareas

1. Formulario de nueva solicitud.
2. Validaciones en cliente/servidor.
3. Campos dinámicos por tipo de viaje.
4. Botones Guardar borrador / Radicar.
5. Feedback de errores y éxito.

### Criterios de aceptación

* Un usuario puede crear borrador.
* Puede radicar si cumple reglas.
* La UI responde sin mezclar demasiada lógica en callbacks.

### Prompt para Codex

```text
Implementa el Módulo 4 creando la página de Solicitud en Dash.
Requisitos:
- formulario empresarial limpio
- campos dinámicos
- callbacks mínimos que deleguen a services
- mensajes de error y éxito
- prueba e2e básica del formulario
```

\---

# Módulo 5 — UI de Aprobaciones y timeline

### Objetivo

Mostrar la trazabilidad del flujo y la bandeja por rol.

### Entregables

* `pages/aprobaciones.py`
* `components/tables.py`
* `components/timeline.py`
* `callbacks/aprobaciones\_callbacks.py`
* `tests/e2e/test\_aprobaciones\_flow.py`

### Tareas

1. Tabla de bandeja por rol.
2. Vista detalle de solicitud.
3. Timeline visual del proceso.
4. Botones aprobar/rechazar/devolver.
5. Vista de auditoría.

### Criterios de aceptación

* Se ve claramente el estado actual.
* Cada acción actualiza el timeline.
* Se puede rastrear responsable y fecha.

### Prompt para Codex

```text
Implementa el Módulo 5.
Construye en Dash:
- bandeja de aprobaciones por rol
- detalle de solicitud
- timeline del workflow
- acciones aprobar/rechazar/devolver
Integra con los services ya creados y agrega pruebas e2e.
```

\---

# Módulo 6 — Integración Gemini y apoyo documental

### Objetivo

Incorporar Gemini de manera controlada y testeable.

### Entregables

* `integrations/gemini\_client.py`
* `services/documentos\_service.py`
* `schemas/document\_ai\_schema.py`
* `tests/unit/test\_gemini\_client.py`
* `tests/unit/test\_documentos\_service.py`

### Tareas

1. Crear cliente Gemini con SDK oficial.
2. Agregar modo mock.
3. Implementar extracción estructurada de carta de invitación.
4. Implementar clasificación de documento adjunto.
5. Implementar resumen de comentarios de aprobación.
6. Validar salida con Pydantic.

### Criterios de aceptación

* Nada rompe si Gemini está desactivado.
* Las respuestas se validan contra esquema.
* Los tests mockean la integración externa.

### Prompt para Codex

```text
Implementa el Módulo 6 con integración a Gemini API.
Requisitos:
- usar Google GenAI SDK
- leer GEMINI\_API\_KEY desde variables de entorno
- exponer métodos tipados y validados con Pydantic
- soportar modo mock para tests
- incluir pruebas unitarias sin hacer llamadas reales externas
```

\---

# Módulo 7 — Generación documental

### Objetivo

Automatizar documentos principales del trámite.

### Entregables

* `services/documentos\_service.py`
* `templates/`
* `tests/integration/test\_document\_generation.py`

### Tareas

1. Generar resolución de comisión.
2. Generar carta/acuse/checklist.
3. Nombrar y versionar archivos.
4. Simular almacenamiento en SharePoint.
5. Relacionar documentos con la solicitud.

### Criterios de aceptación

* Los documentos se generan desde datos estructurados.
* Se registran en la base.
* Los tests validan contenido mínimo y nombres.

### Prompt para Codex

```text
Implementa el Módulo 7 de generación documental.
Necesito plantillas y servicio para crear:
- resolución de comisión
- carta base
- checklist
- metadata del documento
No conectes todavía SharePoint real; usa un adapter mock/local.
```

\---

# Módulo 8 — Pagos y notificación estructurada

### Objetivo

Eliminar el correo manual y preparar orden de pago auditable.

### Entregables

* `pages/pagos.py`
* `services/pagos\_service.py`
* `schemas/pago\_schema.py`
* `callbacks/pagos\_callbacks.py`
* `tests/unit/test\_pagos\_service.py`

### Tareas

1. Validar si una solicitud puede pasar a pago.
2. Construir orden de pago.
3. Generar notificación estructurada.
4. Registrar conciliación aprobado vs girado.
5. Mostrar cola de pagos.

### Criterios de aceptación

* No se notifica pago sin workflow completo.
* La orden de pago queda registrada.
* Existe estado de pago notificado / confirmado.

### Prompt para Codex

```text
Implementa el Módulo 8.
Construye la lógica de pagos y la página de cola de pagos:
- generar orden de pago
- notificar pago
- registrar valor aprobado, notificado y girado
- agregar tests unitarios y UI básica en Dash
```

\---

# Módulo 9 — Legalización posterior

### Objetivo

Controlar el cierre financiero del viaje.

### Entregables

* `pages/legalizacion.py`
* `services/legalizacion\_service.py`
* `schemas/legalizacion\_schema.py`
* `callbacks/legalizacion\_callbacks.py`
* `tests/unit/test\_legalizacion\_service.py`

### Tareas

1. Cargar soportes.
2. Registrar gasto por ítem.
3. Convertir moneda.
4. Calcular diferencias contra anticipo.
5. Determinar saldo a favor o reintegro.
6. Permitir cierre si cumple reglas.

### Criterios de aceptación

* La legalización produce un resumen financiero claro.
* Se detectan diferencias e inconsistencias.
* Los tests cubren cálculos monetarios.

### Prompt para Codex

```text
Implementa el Módulo 9 de legalización.
Incluye:
- registro de gastos
- conversión de moneda
- conciliación anticipo vs soportado
- cierre de legalización
- pruebas unitarias de cálculo
```

\---

# Módulo 10 — Dashboard ejecutivo y SLA

### Objetivo

Mostrar valor de negocio y trazabilidad operativa.

### Entregables

* `pages/dashboard.py`
* `services/dashboard\_service.py`
* `callbacks/dashboard\_callbacks.py`

### KPIs

* solicitudes por estado
* tiempo promedio por etapa
* solicitudes vencidas por SLA
* monto aprobado por periodo
* pagos pendientes
* legalizaciones con inconsistencias

### Prompt para Codex

```text
Implementa el Módulo 10.
Construye un dashboard ejecutivo en Dash con KPIs del proceso y gráficos Plotly.
Usa datos del repository/service layer y no dupliques lógica en callbacks.
```

\---

# Módulo 11 — Seguridad, configuración y endurecimiento

### Objetivo

Dejar el proyecto listo para entorno empresarial.

### Entregables

* manejo robusto de config
* feature flags
* control de errores
* logging estructurado
* tests adicionales

### Tareas

1. Config centralizada por entorno.
2. Feature flag para Gemini.
3. Manejo de errores UI/servicio/integración.
4. Logs con correlation id.
5. Preparar adapters para Azure AD y SharePoint.

### Prompt para Codex

```text
Implementa el Módulo 11 enfocado en endurecimiento:
- settings tipados
- feature flags
- logging estructurado
- manejo de errores
- placeholders de integración corporativa
```

\---

## 11\) Estrategia de pruebas

### 11.1 Unit tests (obligatorios)

Cubrir:

* reglas de negocio
* state machine
* servicios
* integración Gemini mockeada
* cálculos de legalización
* validación de notificación de pago

### 11.2 Integration tests

Cubrir:

* repositories con base temporal
* generación de documentos
* flujo solicitud -> aprobación -> pago

### 11.3 E2E / smoke Dash

Cubrir:

* carga de la app
* navegación mínima
* creación de solicitud
* aprobación básica

### Reglas para pruebas

1. No llamar APIs reales en unit tests.
2. Mockear Gemini y SharePoint.
3. Usar fixtures reutilizables.
4. Asegurar que cada bug crítico tenga test de regresión.

\---

## 12\) Contratos Pydantic sugeridos

### `InvitationData`

```python
class InvitationData(BaseModel):
    organization\_name: str
    destination\_city: str
    destination\_country: str
    start\_date: date
    end\_date: date
    contact\_name: str | None = None
```

### `DocumentClassification`

```python
class DocumentClassification(BaseModel):
    document\_type: str
    confidence: float
    notes: str | None = None
```

### `NormalizedExpense`

```python
class NormalizedExpense(BaseModel):
    category: str
    vendor: str | None = None
    amount: float
    currency: str
    expense\_date: date | None = None
```

\---

## 13\) Variables de entorno

```env
APP\_ENV=local
DEBUG=true
SECRET\_KEY=change-me
DATABASE\_URL=sqlite:///./viaticos.db

GEMINI\_API\_KEY=
ENABLE\_GEMINI=true
GEMINI\_MODEL=gemini-3-flash-preview

SHAREPOINT\_MODE=mock
SAP\_MODE=mock
AUTH\_MODE=mock
```

\---

## 14\) Definition of Done

Un módulo se considera terminado si:

1. compila;
2. tiene tests;
3. pasa lint y formato;
4. no rompe módulos previos;
5. actualiza README o docs;
6. deja lista la siguiente fase.

\---

## 15\) Instrucción general para Codex

```text
Actúa como ingeniero de software senior especializado en Python Dash.
Implementa este proyecto módulo por módulo siguiendo estrictamente esta arquitectura:
- pages para UI
- callbacks livianos
- services para casos de uso
- repositories para persistencia
- domain para reglas
- integrations para proveedores externos
- schemas con Pydantic
- tests unitarios desde el inicio

Reglas:
- no mezclar lógica de negocio compleja en callbacks
- no usar variables globales mutables
- usar tipado
- escribir código limpio y comentado
- agregar pruebas unitarias en cada módulo
- usar mocks para Gemini y otros externos
- mantener compatibilidad con una futura integración corporativa

Empieza por el Módulo 0 y no avances al siguiente hasta dejar el actual completo.
```

\---

## 16\) Prioridad funcional recomendada

Orden real de construcción:

1. bootstrap
2. dominio
3. persistencia
4. solicitud
5. aprobaciones
6. Gemini
7. documentos
8. pagos
9. legalización
10. dashboard
11. endurecimiento

\---

## 17\) Nota de implementación

La primera versión debe ser **demo funcional empresarial**, no producto final.
Por tanto:

* usar datos mock para catálogos;
* diseñar adapters para integraciones;
* dejar contratos claros para luego conectar Azure AD, SharePoint, SAP y Power Automate.

\---

## 18\) Resultado esperado

Al finalizar, el proyecto debe permitir demostrar:

* trazabilidad completa;
* aprobaciones auditables;
* documentación automatizada;
* notificación estructurada a pagos;
* legalización controlada;
* apoyo documental con Gemini;
* analítica ejecutiva del proceso.

