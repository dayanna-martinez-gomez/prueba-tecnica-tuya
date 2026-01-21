# Ejercicio Conceptual  
## KPI’s, Veeduría de Calidad y Trazabilidad del Dataset de Teléfonos

## 1. Objetivo

Definir un mecanismo que permita a los equipos de negocio realizar **veeduría continua** sobre la calidad y confiabilidad del dataset de teléfonos de clientes, garantizando visibilidad, trazabilidad del dato y seguimiento en el tiempo mediante indicadores claros y automatizados.

---

## 2. Enfoque general de la solución

La veeduría del dato se construye a partir de los resultados del dataset definido en el ejercicio anterior y se soporta en:

1. **Tablas de auditoría y métricas**, que resumen el estado del proceso y del dato en cada ejecución.
2. **Reportes automáticos periódicos python**, con estadísticos y hallazgos relevantes.
3. **Un tablero Power BI**, que permite a negocio monitorear la calidad de forma visual.

Este enfoque asegura que los KPI’s no sean calculados de forma manual ni aislada, sino que provengan directamente del proceso productivo.

---

## 3. Tablas de soporte para veeduría y trazabilidad

Además de las tablas principales del dataset (`telefonos_origen`, `telefonos_procesados`, `telefono_confiable_cliente`), se generan **tablas adicionales de soporte**, cuyo objetivo es explicar **cómo se comporta el dato y el proceso en cada ejecución**.

Todas estas tablas se relacionan mediante el campo `id_ejecucion`.

---

### 3.1 `auditoria_ejecuciones_telefonos`  
**(Bitácora de ejecuciones del proceso)**

Esta tabla registra **cada ejecución del proceso de construcción del dataset de teléfonos**, permitiendo saber cuándo se ejecutó, si fue exitosa y cuántos registros procesó.

**¿De dónde surge?**  
Se genera automáticamente desde el proceso en Python/PySpark al inicio y al final de cada corrida.

**Campos:**
- `id_ejecucion`
- `fecha_inicio`
- `fecha_fin`
- `estado` (OK / FALLÓ / BLOQUEADO_POR_CALIDAD)
- `registros_telefonos_origen`
- `registros_telefonos_procesados`
- `clientes_con_telefono_confiable`
- `rule_version` (versión de reglas aplicada)
- `observaciones_error` (si aplica)

**Para qué sirve:**  
Control operativo del proceso y trazabilidad de cada ejecución.

---

### 3.2 `metricas_calidad_telefonos`  
**(Indicadores de calidad del dataset por ejecución)**

Esta tabla consolida en una sola fila los **KPI’s de calidad del dataset de teléfonos** para cada ejecución.

**¿De dónde surge?**  
Se calcula automáticamente al finalizar el proceso, utilizando:
- `telefonos_procesados` para métricas de validez, verificación, score y duplicidad.
- `telefono_confiable_cliente` para métricas de cobertura por cliente.

**Campos:**
- `id_ejecucion`
- `total_clientes`
- `clientes_con_telefono_confiable`
- `pct_cobertura`
- `telefonos_validos`
- `telefonos_invalidos`
- `pct_validez`
- `telefonos_verificados`
- `pct_verificados`
- `pct_duplicidad_critica`
- `score_promedio`
- `score_p50`
- `score_p90`
- `top_motivos_invalidez` (resumen)

**Para qué sirve:**  
Medir la calidad del dataset de forma comparable entre ejecuciones y soportar alertas y análisis de tendencia.

---

### 3.3 `calidad_telefonos_por_origen`  
**(Resumen de calidad del dato por sistema fuente)**

Esta tabla permite analizar la calidad del dato **segmentada por sistema de origen**, facilitando la identificación de fuentes problemáticas.

**¿De dónde surge?**  
Se construye agrupando la información de `telefonos_procesados` por `sistema_origen`.

**Campos:**
- `id_ejecucion`
- `sistema_origen`
- `conteo_telefonos`
- `pct_validos`
- `pct_verificados`
- `score_promedio`

**Para qué sirve:**  
Identificar qué sistemas están aportando teléfonos de baja calidad y priorizar acciones de mejora.

---

## 4. KPI’s clave para los equipos de negocio

A partir de las tablas anteriores, los equipos de negocio pueden consultar KPI’s como:

- **% de cobertura de teléfono confiable**
- **% de teléfonos válidos**
- **% de teléfonos verificados**
- **Duplicidad crítica de teléfonos**
- **Score promedio y percentiles**
- **Evolución de la calidad en el tiempo**
- **Calidad del dato por sistema de origen**

Estos indicadores permiten evaluar de forma continua la capacidad real de contactabilidad.

---

## 5. Reporte automático de seguimiento

De forma complementaria, se genera un **reporte automático periódico** (semanal o quincenal) mediante Python, que incluye:

- Resumen ejecutivo del estado del dataset.
- Comparación de KPI’s frente a la ejecución anterior.
- Principales hallazgos y alertas.
- Estadísticos del puntaje de confiabilidad.

El reporte se genera en formato HTML, PDF o Excel según la necesidad del equipo.

---

## 6. Automatización y distribución

La ejecución del proceso y el envío del reporte se automatizan mediante:

- **Python / PySpark** para cálculo de métricas y generación del reporte.
- **Power Automate** para distribución automática por correo o Teams y notificación de fallos.

---

## 7. Tablero Power BI

Se construye un tablero Power BI conectado a las tablas de métricas y auditoría, con páginas orientadas a:

- Resumen ejecutivo de calidad.
- Calidad por sistema de origen.
- Motivos de invalidez.
- Confiabilidad del dato (score).
- Histórico y trazabilidad por ejecución.

---

## 8. Resultado

Este mecanismo permite a la organización contar con una **veeduría clara, trazable y automatizada** del dataset de teléfonos de clientes, facilitando la toma de decisiones y la mejora continua de la calidad del dato.
