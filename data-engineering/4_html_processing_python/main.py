from pathlib import Path
from src.collector import collect_html_files
from src.processor import HtmlImageProcessor
from src.replacer import HtmlReplacer
from src.results import ProcessingResults

input_dirs = ["input"]

def main():
    """
    Este script orquesta el flujo completo de procesamiento de archivos HTML para incrustar imágenes externas como data URI en base64.
    El proceso automatiza los siguientes pasos:

    1. Recolecta todos los archivos HTML desde las rutas de entrada especificadas, incluyendo subdirectorios.
    2. Para cada archivo HTML encontrado:
       - Extrae todas las rutas de imágenes referenciadas en etiquetas <img>.
       - Intenta convertir cada imagen a formato base64 (data URI), registrando los éxitos y los fallos.
       - Reemplaza en el HTML original las rutas de las imágenes por sus equivalentes en base64.
       - Guarda el HTML modificado en un directorio de salida, generando archivos autocontenidos y portables.
    3. Al finalizar, muestra un resumen estructurado de todas las imágenes procesadas exitosamente y de aquellas que fallaron, agrupadas por archivo HTML.

    Este flujo integra los módulos collector, processor, replacer y results.
    """
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    results = ProcessingResults()
    html_files = collect_html_files(input_dirs)
    print(f"Archivos HTML encontrados: {len(html_files)}")

    for html_path in html_files:
        print(f"\nProcesando: {html_path}")
        try:
            processor = HtmlImageProcessor(html_path)
            replacements = {}
            for src in processor.image_sources:
                try:
                    replacements[src] = processor.image_to_data_uri(
                        (html_path.parent / src).resolve() if not Path(src).is_absolute() else Path(src)
                    )
                    results.add_success(str(html_path), src)
                except Exception as e:
                    results.add_fail(str(html_path), src, e)

            replacer = HtmlReplacer(html_path, processor.html_text, replacements, output_dir)
            out_file = replacer.replace_and_write()
            print(f"Archivo generado: {out_file}")

        except Exception as e:
            print(f"Error procesando {html_path}: {e}")

    print("\nResumen de resultados:")
    print(results.as_dict())

if __name__ == "__main__":

    main()
