import os
import sqlite3
import pandas as pd
import logging

"""
Este script automatiza el proceso de ingestión de datos desde un archivo Excel hacia una base de datos SQLite.
El flujo consiste en:
1. Cambiar el directorio de trabajo a la carpeta 'data' para asegurar rutas relativas consistentes.
2. Definir las rutas de entrada (Excel) y salida (base de datos) de forma clara y centralizada.
3. Implementar clases para manejar la conexión y operaciones con la base de datos (DB) y la lectura de hojas de Excel (Excel).
4. Para cada hoja encontrada en el archivo Excel, leer los datos y almacenarlos en la base de datos, creando o reemplazando las tablas según corresponda.
5. Registrar todas las operaciones relevantes mediante logging para trazabilidad y depuración.
6. Cerrar la conexión a la base de datos al finalizar el proceso.

Este enfoque garantiza portabilidad, robustez y facilidad de mantenimiento en el flujo de ingestión de datos tabulares.
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
EXCEL_PATH = "dataset.xlsx"
DB_PATH = "../db/dataset_sqlite.db"

class DB:
    """
    Clase para gestionar la conexión y operaciones con la base de datos SQLite.
    Permite insertar DataFrames como tablas y cerrar la conexión de forma segura.
    """
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        logging.info(f"Conectado a la base de datos: {path}")
    
    def insert(self, table, df):
        df.to_sql(table, self.conn, if_exists='replace', index=False)
        logging.info(f"Datos insertados en la tabla: {table}")
    
    def close(self):
        self.conn.close()
        logging.info("Conexión a la base de datos cerrada.")
    
    def create_index(self, table, column):
        index_name = f"idx_{table}_{column}"
        sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table}({column})"
        self.conn.execute(sql)
        logging.info(f"Índice creado: {index_name} en la tabla {table} ({column})")

class Excel:
    """
    Clase para gestionar la lectura de hojas y datos desde un archivo Excel.
    Permite listar las hojas disponibles y leer cada hoja como DataFrame.
    """
    def __init__(self, path):
        self.path = path
    
    def sheets(self):
        sheets = pd.ExcelFile(self.path).sheet_names
        logging.info(f"Hojas encontradas: {sheets}")
        return sheets
   
    def read(self, sheet):
        logging.info(f"Leyendo hoja: {sheet}")
        return pd.read_excel(self.path, sheet_name=sheet)

if __name__ == '__main__':
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = DB(DB_PATH)
    excel = Excel(EXCEL_PATH)
    for sheet in excel.sheets():
        df = excel.read(sheet)
        db.insert(sheet, df)
        # Crea un índice en la primera columna de cada tabla si existe
        if len(df.columns) > 0:
            db.create_index(sheet, df.columns[0])
    db.close()
