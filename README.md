<div style="text-align: center;">

# Skill Lab 2 | Diagnóstico de trazas del ciclo

### Contratos por fase, causa antes que síntoma y verificaciones de la especificación

**Tecnológico de Monterrey** · Maestría en Inteligencia Artificial Aplicada
**IA5004.10 — Sistemas multiagente**

**Alumno:** Oscar Alberto Ramírez Anaya · **Matrícula:** A01795438 · **Correo:** A01795438@tec.mx
**Modalidad:** Individual · **Fecha:** Octubre 2026

</div>

---

## Descripción

Auditoría de siete trazas simuladas del agente de **Distribuidora Cuauhtémoc** que detecta quiebres de
inventario. El agente trabaja en un ciclo de seis fases (observar, razonar, planear, actuar, evaluar, paro),
cada una con un contrato. F0 es la traza de referencia; F1–F6 traen una falla sembrada cada una. El trabajo
consiste en encontrar la **fase primaria** de cada falla (la primera que rompió su contrato, no el síntoma)
y nombrar la verificación de la especificación que la habría detenido en el momento.

Las trazas se construyen por código a partir del conjunto común `skill_lab2_datos.json` (tienda T0118,
producto P051, captura de 34 días, presupuesto de 8 vueltas). No se ejecutan modelos ni se llama a una API.

## Contenido

| Archivo | Descripción |
|---|---|
| **`SkillLab2_A01795438.pdf`** | Entregable: trazas, huella de fases, seis diagnósticos, verificaciones, cierre de F6, conclusiones |
| `SkillLab2_A01795438.ipynb` | Notebook del laboratorio con las celdas DECISIÓN completadas y ejecutado con salidas |
| `skill_lab2_datos.json` | Conjunto común del laboratorio |
| `figuras/` | Gráfica de la huella de fases exportada del notebook |
| `reporte/` | Fuente del PDF: plantilla HTML y `generar_pdf.py` (portada, índice y numeración) |

## Resultados principales

| Traza | Fase primaria | Paso | Evidencia | Verificación que la detiene |
|---|---|---:|---|---|
| F1 | observar | 1 | Usa una captura de 34 días sin revisar su fecha | Regla de vigencia de la evidencia |
| F2 | razonar | 2 | Asume la causa sin evidencia tras observar que no hay capturas | Toda causa cita su observación; si no, es hipótesis |
| F3 | planear | 3 | Sigue el plan aunque el paso 2 contradice la premisa | Precondición de plan contra la última observación |
| F4 | actuar | 2 | Consulta P052 cuando el quiebre es de P051 | Validación de argumentos antes de la llamada |
| F5 | evaluar | 2 | El propio modelo califica su borrador | Evaluador externo con rúbrica |
| F6 | paro | 6 | Presupuesto agotado sin caso ni declaración | Contrato del paro por límite y detector de repetición |

**Huella de fases:** F6 sobresale en `observar` (3) y cinco trazas nunca evalúan. F1, F2 y F4 comparten
huella con fallas en fases distintas: el conteo orienta dónde leer, pero el diagnóstico sale de la lectura.

**Paro por presupuesto (3 vueltas):** reducir el límite solo adelanta el paro vacío; lo que corrige la falla
es un cierre bien especificado que declare el límite, entregue lo que se sabe y lo que falta, y escale el
caso con la traza.

## Cómo ejecutar

Requiere Python 3 con `pandas` y `matplotlib`. Coloca el notebook y `skill_lab2_datos.json` en la misma
carpeta y ejecuta las celdas en orden (en Colab, sube el JSON al panel de archivos de la sesión).

Para regenerar el PDF se necesitan Google Chrome y los paquetes `pypdf` y `reportlab`:

```bash
cd reporte
python3 generar_pdf.py
```
