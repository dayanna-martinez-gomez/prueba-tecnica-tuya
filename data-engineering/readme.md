# Prueba Técnica – Ingeniería de Datos TUYA

Este repositorio contiene la solución desarrollada para la prueba técnica de Ingeniería de Datos de TUYA.  
La solución incluye ejercicios conceptuales y prácticos, organizados de forma independiente, siguiendo el orden y los requerimientos definidos en el enunciado.

Cada ejercicio fue abordado con un enfoque claro, priorizando la legibilidad, la correcta organización de los artefactos y el cumplimiento de los criterios solicitados.

---

## 📂 Estructura del repositorio

```text
prueba-tecnica-tuya/
├── 1_prueba_concepto.md
├── 2_prueba_concepto_KPIs.md
├── 3_output_rachas_sqlite/
│   ├── data/
│   │   └── dataset.xlsx
│   ├── db/
│   │   └── dataset_sqlite.db
│   ├── sql/
│   │   └── query_rachas.sql
│   └── ingest.py
├── 4_html_processing_python/
│   ├── input/
│   │   ├── html/
│   │   │   ├── ejemplo1.html
│   │   │   └── subdir/
│   │   │       └── ejemplo2.html
│   │   └── image/
│   │       ├── picture1.png
│   │       ├── picture2.jpg
│   │       └── picture3.jpg
│   ├── output/
│   │   ├── ejemplo1_inlined.html
│   │   └── ejemplo2_inlined.html
│   └── src/
│       ├── collector.py
│       ├── processor.py
│       ├── replacer.py
│       ├── results.py
│       └── main.py
└── readme.md

```

---

## 1️ Ejercicio Conceptual – Creación de Dataset de Teléfonos

**Archivo:** `1_prueba_concepto.md`

En este ejercicio se desarrolló una propuesta conceptual para la creación y mantenimiento de un dataset confiable de números de teléfono de clientes.

La solución se enfoca en:
- Definir un proceso controlado de ingestión de datos.
- Establecer validaciones básicas de calidad sobre los números de teléfono (formato, duplicidad y obligatoriedad).
- Garantizar la trazabilidad de los registros a lo largo del tiempo.
- Proponer el uso de pipelines automatizados (CI/CD) para el despliegue y mantenimiento del dataset.

El resultado es un diseño conceptual que busca asegurar la consistencia y confiabilidad del dato para su uso en procesos de comunicación con clientes.

---

## 2️ Ejercicio Conceptual – KPI’s y Calidad de Datos

**Archivo:** `2_prueba_concepto_KPIs.md`

Con base en el dataset conceptual de teléfonos, se planteó un mecanismo de seguimiento orientado a la calidad y trazabilidad del dato.

En este ejercicio se definieron:
- Indicadores de calidad de datos enfocados en teléfonos de clientes.
- Métricas para monitorear errores, duplicados y registros válidos.
- Un enfoque de veeduría que permite a los equipos de negocio evaluar el estado del dataset mediante KPIs.
- Separación entre la gestión técnica del dato y su consumo analítico.

La propuesta permite obtener información clara y medible sobre la calidad de los teléfonos almacenados.

---
## 3️ Ejercicio Práctico – Rachas de Saldo (SQLite)

**Carpeta:** `3_output_rachas_sqlite/`

En este ejercicio se implementa la carga y análisis de información histórica de saldos de clientes utilizando una base de datos SQLite.

### Componentes desarrollados
- **data/dataset.xlsx:** archivo fuente con la información utilizada para el ejercicio.
- **db/dataset_sqlite.db:** base de datos SQLite donde se almacenan los datos.
- **ingest.py:** script en Python encargado de cargar la información desde el archivo Excel hacia la base de datos.
- **sql/query_rachas.sql:** consulta SQL que resuelve los criterios solicitados en el enunciado.

### Dependencias
- Python 3.x
- `pandas`
- `openpyxl` (requerido para la lectura de archivos Excel `.xlsx`)

Las librerías `os`, `sqlite3` y `logging` hacen parte de la librería estándar de Python y no requieren instalación adicional.

### Ejecución

El ejercicio se ejecuta en dos pasos:

1. **Carga de datos**

   Ubicándose en la carpeta `3_output_rachas_sqlite`, ejecutar: python ingest.py

---

## 4️ Ejercicio Práctico – Procesamiento de Archivos HTML en Python

**Carpeta:** `4_html_processing_python/`

En este ejercicio se desarrolló una solución en Python para procesar archivos HTML y convertir las imágenes referenciadas mediante etiquetas `<img>` a formato Base64, generando nuevos archivos HTML sin modificar los originales.

### Funcionamiento general
- El sistema recibe archivos HTML o directorios que pueden contener archivos HTML, incluyendo subdirectorios.
- Para cada archivo HTML se identifican las imágenes asociadas.
- Las imágenes se convierten a Base64 utilizando únicamente librerías estándar de Python.
- Se generan nuevos archivos HTML con las imágenes embebidas.
- Se construye un objeto de resultados que registra los archivos procesados de forma exitosa y los que presentaron errores.

### Organización de carpetas
- **input/**: contiene archivos HTML e imágenes utilizados únicamente como ejemplos de entrada.
- **output/**: almacena los archivos HTML generados con las imágenes embebidas en Base64.
- **src/**: contiene el código fuente de la solución.

### Organización del código
El código fue estructurado separando responsabilidades:
- **collector.py:** localiza y recopila los archivos HTML a procesar.
- **processor.py:** coordina el procesamiento de cada archivo HTML.
- **replacer.py:** reemplaza las rutas de las imágenes por su versión codificada en Base64.
- **results.py:** gestiona el objeto de resultados con los procesos exitosos y fallidos.
- **main.py:** punto de entrada de la aplicación.

### Dependencias
Este ejercicio utiliza únicamente librerías estándar de Python, por lo que no requiere instalación de dependencias adicionales.

### Ejecución

Ubicándose en la carpeta `src`, ejecutar: python main.py




