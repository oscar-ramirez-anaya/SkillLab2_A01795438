import io
import os
import subprocess

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "SkillLab2_A01795438.pdf")
TITULOS = ["1. Resumen ejecutivo", "2. Contexto, datos y método", "3. Parte A.", "4. Parte B.",
           "5. Interpretación 1.", "6. Interpretación 2.", "7. Conclusiones", "8. Declaración de uso de IA", "9. Referencias"]


def render(html, pdf):
    ruta = os.path.join(AQUI, "_tmp.html")
    open(ruta, "w", encoding="utf-8").write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", f"file://{ruta}"], check=True, capture_output=True)
    os.remove(ruta)


def paginas(pdf):
    textos = [p.extract_text() for p in PdfReader(pdf).pages]
    res = []
    for t in TITULOS:
        # se ignora la página del índice (2), donde todos los títulos aparecen
        hallada = next(i + 1 for i, x in enumerate(textos) if t in x and (i + 1 != 2 or t.startswith(("1.", "2."))))
        res.append(hallada)
    return res


plantilla = open(os.path.join(AQUI, "reporte_tpl.html"), encoding="utf-8").read()
tmp = os.path.join(AQUI, "_tmp.pdf")
html = plantilla
for _ in range(2):
    render(html, tmp)
    nums = paginas(tmp)
    html = plantilla
    for i, n in enumerate(nums, 1):
        html = html.replace("{P%d}" % i, str(n))
render(html, tmp)
print("páginas por sección:", paginas(tmp))

lector = PdfReader(tmp)
total = len(lector.pages)
escritor = PdfWriter()
for i, pagina in enumerate(lector.pages, 1):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.45, 0.45, 0.45)
    c.drawCentredString(letter[0] / 2, 22, f"Página {i} de {total}")
    if i > 1:
        c.drawString(45, 22, "Skill Lab 2 · A01795438")
    c.save()
    buf.seek(0)
    pagina.merge_page(PdfReader(buf).pages[0])
    escritor.add_page(pagina)
escritor.add_metadata({"/Title": "SkillLab2_A01795438", "/Author": "Oscar Alberto Ramírez Anaya",
                       "/Producer": "", "/Creator": ""})
with open(SALIDA, "wb") as f:
    escritor.write(f)
os.remove(tmp)
print("total", total)
