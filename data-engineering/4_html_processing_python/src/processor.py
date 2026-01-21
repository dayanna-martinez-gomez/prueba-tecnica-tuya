from pathlib import Path
import base64
from html.parser import HTMLParser
from typing import List, Dict, Tuple

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Ajusta según tu estructura
os.chdir(BASE_DIR)

class ImageSourceExtractor(HTMLParser):
    """Extrae los src de todas las etiquetas <img> en un HTML."""
    def __init__(self):
        super().__init__()
        self.sources: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        if tag.lower() == "img":
            attrs_dict = {k.lower(): v for k, v in attrs}
            src = attrs_dict.get("src")
            if src:
                self.sources.append(src)

class HtmlImageProcessor:
    """Procesa un archivo HTML para extraer y convertir imágenes a base64."""
    def __init__(self, html_path: Path):
        self.html_path = html_path
        self.html_text = html_path.read_text(encoding="utf-8")
        self.image_sources = self._extract_image_sources()

    def _extract_image_sources(self) -> List[str]:
        parser = ImageSourceExtractor()
        parser.feed(self.html_text)
        return parser.sources

    @staticmethod
    def extension_to_mime_type(extension: str) -> str:
        ext = extension.lower()
        if ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        if ext == ".png":
            return "image/png"
        if ext == ".gif":
            return "image/gif"
        if ext == ".webp":
            return "image/webp"
        return "application/octet-stream"

    @staticmethod
    def image_to_data_uri(img_path: Path) -> str:
        mime = HtmlImageProcessor.extension_to_mime_type(img_path.suffix)
        data = img_path.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"

    def build_replacements(self) -> Dict[str, str]:
        replacements: Dict[str, str] = {}
        for src in self.image_sources:
            img_path = Path(src)
            if not img_path.is_absolute():
                img_path = (self.html_path.parent / img_path).resolve()
            replacements[src] = self.image_to_data_uri(img_path)
        return replacements

