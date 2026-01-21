from typing import Dict, List, Any

class ProcessingResults:
    """
    Guarda las imágenes procesadas exitosamente y las que fallaron,
    en la estructura: { "success": {...}, "fail": {...} }
    """
    def __init__(self):
        self.success: Dict[str, List[str]] = {}
        self.fail: Dict[str, List[Dict[str, str]]] = {}

    def add_success(self, html_path: str, img_src: str) -> None:
        self.success.setdefault(html_path, []).append(img_src)

    def add_fail(self, html_path: str, img_src: str, error: Exception) -> None:
        self.fail.setdefault(html_path, []).append(
            {"src": img_src, "error": type(error).__name__}
        )

    def as_dict(self) -> Dict[str, Any]:
        return {"success": self.success, "fail": self.fail}