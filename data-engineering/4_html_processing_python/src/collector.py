from pathlib import Path
from typing import List

def collect_html_files(inputs: List[str]) -> List[Path]:
    """
    Recibe una lista de rutas (archivos HTML o directorios)
    y devuelve todos los archivos HTML encontrados.
    Si la ruta es un directorio, recorre también los subdirectorios.
    """
    html_files: List[Path] = []
    for item in inputs:
        path = Path(item)
        # Caso 1: es un archivo HTML
        if path.is_file() and path.suffix.lower() == ".html":
            html_files.append(path)
        # Caso 2: es un directorio
        elif path.is_dir():
            for html in path.rglob("*.html"):
                html_files.append(html)
        # Otros casos (no existe o no es html) se ignoran
    return html_files

