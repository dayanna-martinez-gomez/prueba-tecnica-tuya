from pathlib import Path
from typing import Dict

class HtmlReplacer:
    """
    Esta clase encapsula el proceso de reemplazo de rutas de imágenes en archivos HTML por sus equivalentes en base64 (data URI)
    y la escritura del resultado en un nuevo archivo. Permite transformar un HTML con imágenes externas en un HTML autocontenido,
    facilitando su portabilidad y distribución sin dependencias de archivos adicionales.
    """
    def __init__(self, html_path: Path, html_text: str, replacements: Dict[str, str], output_dir: Path):
        self.html_path = html_path
        self.html_text = html_text
        self.replacements = replacements
        self.output_dir = output_dir

    def replace_and_write(self) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        new_html = self.html_text
        for src, data_uri in self.replacements.items():
            new_html = new_html.replace(f'src="{src}"', f'src="{data_uri}"')
        out_path = self.output_dir / f"{self.html_path.stem}__inlined{self.html_path.suffix}"
        out_path.write_text(new_html, encoding="utf-8")
