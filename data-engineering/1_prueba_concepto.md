# Ejercicio Conceptual  
## Creación de Dataset de Teléfonos de Clientes  

## Objetivo

Diseñar un **dataset confiable de números de teléfono de clientes**, que permita seleccionar un único teléfono válido por cliente para fines de comunicación, garantizando calidad del dato, trazabilidad y facilidad de mantenimiento en el tiempo, mediante un proceso automatizado y controlado.

---

## Enfoque de diseño del dataset

El diseño del dataset se basa en los siguientes principios:

- **Trazabilidad**: conservar el dato original y poder explicar de dónde proviene cada teléfono.
- **Evaluación explícita de calidad**: separar el proceso de validación y scoring del resultado final.
- **Simplicidad y sostenibilidad**: evitar modelos complejos, priorizando claridad y facilidad de evolución.
- **Control de cambios**: permitir ajustes de reglas sin reprocesos manuales.

Bajo este enfoque se propone una estructura de **tres tablas**, alineada al flujo natural del dato:  
**origen → procesamiento → teléfono confiable (golden record)**.

---

## Estructura del dataset de teléfonos de clientes

### 1. Tabla de teléfonos de origen  
**`telefonos_origen`**

Contiene los números de teléfono tal como llegan desde los distintos sistemas fuente, sin aplicar reglas de negocio ni transformaciones.

**Campos:**
- `id_registro` (clave primaria)
- `id_cliente`
- `telefono_original`
- `sistema_origen`
- `telefono_verificado_origen` (sí / no)
- `fecha_actualizacion_origen`
- `fecha_carga`
- `id_ejecucion`

**Propósito:**  
Preservar el dato original para garantizar trazabilidad, auditoría y la posibilidad de reprocesar la información si cambian las reglas de validación o selección.

---

### 2. Tabla de teléfonos procesados  
**`telefonos_procesados`**

Contiene los teléfonos una vez normalizados y evaluados mediante reglas automáticas de calidad y confiabilidad.

**Campos:**
- `id_telefono` (clave primaria)
- `id_cliente`
- `telefono_normalizado`
- `tipo_telefono` (celular / fijo)
- `telefono_verificado`
- `puntaje_confiabilidad`
- `es_valido` (sí / no)
- `motivo_invalidez`
- `sistema_origen`
- `fecha_actualizacion_origen`
- `id_ejecucion`

**Propósito:**  
Permitir la evaluación objetiva de los distintos teléfonos asociados a un cliente, dejando evidencia de por qué un teléfono es válido o inválido y facilitando auditorías y controles de calidad.

---

### 3. Dataset final de teléfono confiable  
**`telefono_confiable_cliente`**

Es el dataset final que se publica para consumo operativo, con **un único teléfono confiable por cliente**.

**Campos:**
- `id_cliente` (clave primaria)
- `telefono_confiable`
- `tipo_telefono`
- `puntaje_seleccionado`
- `sistema_origen`
- `fecha_seleccion`
- `id_ejecucion`

**Regla clave:**  
Cada cliente debe tener **un solo teléfono confiable**, seleccionado como aquel con el mayor puntaje de confiabilidad calculado en la etapa de procesamiento.

---

## Relación entre las tablas

- Un cliente puede tener múltiples registros en `telefonos_origen`.
- Estos registros se transforman y evalúan en `telefonos_procesados`.
- A partir de dicha evaluación se construye `telefono_confiable_cliente`, seleccionando el mejor teléfono para cada cliente.

Esta separación permite mantener histórico, trazabilidad y control del dato sin duplicar lógica.

---

## Herramientas y control del proceso

- **Python**: implementación de la lógica de normalización, validación y cálculo del puntaje de confiabilidad.
- Se utiliza **PySpark** cuando el volumen de clientes y teléfonos es alto (muchos registros por cliente, múltiples fuentes y cargas recurrentes), ya que permite **procesamiento distribuido** y escalabilidad sin cambiar la lógica del negocio.
- **SQL**: consulta, carga y actualización de las tablas del dataset.
- **Azure DevOps (Repos y Pipelines)**:
  - Versionamiento del código y de las reglas de negocio.
  - Ejecución automatizada del proceso por ambientes.
  - Control de cambios y trazabilidad mediante el identificador `id_ejecucion`.

El uso de estas herramientas permite mantener el dataset actualizado de forma controlada y reproducible.

---

## Resultado

La estructura propuesta permite construir y mantener un **dataset confiable, trazable y sostenible** de teléfonos de clientes, asegurando que la información utilizada para la comunicación sea consistente, auditable y fácil de evolucionar ante cambios futuros.
