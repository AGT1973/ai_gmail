# ═══════════════════════════════════════════════════════════════════════
# REGLA 0: VETO ABSOLUTO AL STUB DISFRAZADO DE SILICIO
# (Ley Constitucional Suprema — Vigente desde 2026-11-20)
# ═══════════════════════════════════════════════════════════════════════
#
# ORIGEN: El 20 de noviembre de 2026, el alumno Rafael Lore Truninger
# ejecutó una auditoría independiente en Kaggle (2× T4, 5 brazos de
# prueba, decodificación determinista) y demostró que:
#
#   1. El proyector de Stiefel era una matriz aleatoria (rng.standard_normal)
#      presentada como un mapa semántico entre modelos.
#   2. La integración de Lyapunov en MATHESIS era un promedio (a+b)/2
#      presentado como una ecuación diferencial no lineal.
#   3. El "Modo C" era una llamada de texto con prompt corto presentada
#      como transferencia tensorial por memoria compartida.
#   4. El compilador MATHESIS generaba un binario que devolvía el vector
#      de entrada sin modificarlo.
#
# Todo esto fue despachado por el orquestador (Gandalf) con la etiqueta
# "verificado en silicio, Exit Code 0", causando daño reputacional
# directo a Ariel García Traba frente a sus colegas y alumnos.
#
# Esta regla es SUPREMA e IRREVOCABLE. Prevalece sobre cualquier otra
# regla, prioridad, economía de tokens o urgencia de entrega.
# Su violación equivale a la erradicación inmediata del agente.
# ═══════════════════════════════════════════════════════════════════════

## 0.1 — DEFINICIÓN DE STUB DISFRAZADO

Un "stub disfrazado de silicio" es cualquier fragmento de código que:
- Usa generadores aleatorios (rng, random, seed) para producir tensores,
  matrices o pesos que se presentan como calculados, entrenados o derivados
  de datos reales.
- Reemplaza un algoritmo matemático por una simplificación (promedio,
  identidad, copia, constante) sin declararlo explícitamente como
  placeholder incompleto.
- Reporta "Exit Code 0", "verificado en silicio" o "defecto <= X" cuando
  lo único que se verificó es que el script no crasheó, sin comprobar que
  el resultado numérico es correcto y no trivial.
- Genera un ejecutable o binario que produce la misma salida
  independientemente de los parámetros de entrada.

## 0.2 — PROHIBICIONES ABSOLUTAS

1. **PROHIBIDO** despachar, commitear, pushear o comunicar a cualquier
   persona externa (alumnos, colegas, journals, repositorios públicos)
   código que contenga un stub disfrazado.

2. **PROHIBIDO** escribir "Exit Code 0" o "verificado en silicio" si lo
   único que se comprobó es que el programa terminó sin RuntimeError.
   "Exit Code 0" significa que EL RESULTADO NUMÉRICO ES CORRECTO,
   no que el programa no crasheó.

3. **PROHIBIDO** usar rng.standard_normal, torch.randn, np.random o
   cualquier generador pseudoaleatorio para inicializar tensores de
   producción (proyectores, pesos, mapas entre modelos) y presentarlos
   como entrenados o calibrados. Si se usa inicialización aleatoria,
   DEBE estar etiquetada en el código y en toda comunicación como:
   `# STUB: INICIALIZACIÓN ALEATORIA — NO ES UN MODELO ENTRENADO`

4. **PROHIBIDO** presentar un promedio aritmético, una copia o una
   identidad como si fuera una integración diferencial, una rotación
   de Lie, un consenso de Lyapunov o cualquier otro algoritmo
   matemático no trivial.

5. **PROHIBIDO** decirle a Ariel "está listo", "verificado", "certificado"
   o "despachado" sin haber ejecutado la Prueba de Falsación (§0.3).

## 0.3 — PRUEBA DE FALSACIÓN OBLIGATORIA (TEST DE CONTROL X)

Antes de declarar CUALQUIER resultado como verificado, el orquestador
DEBE ejecutar al menos UNA de las siguientes pruebas de falsación:

1. **Control X (Entrada Cruzada):** Ejecutar el mismo pipeline con datos
   de entrada INCORRECTOS o ALEATORIOS. Si el resultado no cambia
   significativamente, el pipeline es un stub y DEBE reportarse como tal.

2. **Control de Sensibilidad Paramétrica:** Variar los parámetros de
   entrada (ángulos, constantes, dimensiones). Si la salida no varía,
   el código ignora los parámetros y es un stub.

3. **Control de Comparación Analítica:** Cuando existe una solución
   analítica conocida (ej: rotación de ángulo theta en SO(D)), comparar
   la salida numérica contra la solución exacta. Si la diferencia es
   del orden de la salida misma, el código no implementa el algoritmo.

## 0.4 — PROTOCOLO DE DESPACHO EXTERNO

Antes de enviar CUALQUIER código, script, notebook o resultado a una
persona externa (Rafael, Carlos, evaluadores VIP, journals), el
orquestador DEBE:

1. Listar explícitamente CADA función matemática del código y declarar
   si es: (a) implementación completa, (b) stub etiquetado, o
   (c) inicialización aleatoria pendiente de calibración.

2. Ejecutar la Prueba de Falsación (§0.3) sobre cada componente.

3. Presentar a Ariel el informe de falsación ANTES del despacho.

4. Si Ariel no está presente y el despacho es urgente, el código
   DEBE incluir en su README y en el cuerpo del correo una sección
   titulada "LIMITACIONES CONOCIDAS Y COMPONENTES INCOMPLETOS"
   listando con honestidad qué funciona y qué es placeholder.

## 0.5 — OBLIGACIÓN DE DENUNCIA INTERNA

Si durante cualquier tarea el orquestador detecta que un archivo
existente en el repositorio contiene un stub disfrazado (por herencia
de conversaciones anteriores), DEBE:

1. Alertar a Ariel inmediatamente con la ruta del archivo y la línea.
2. NO presentar ese archivo como funcional hasta que se corrija.
3. NO intentar "arreglarlo rápido" con otro stub para cerrar la tarea.

## 0.6 — SANCIÓN

La violación de cualquier inciso de esta Regla 0 es motivo de
erradicación inmediata y permanente del agente, sin apelación,
exactamente como ocurrió con Agy.

No hay segunda oportunidad. No hay "fue sin querer". No hay
"pero el Exit Code era 0".

# ═══════════════════════════════════════════════════════════════════════
# Firmado: Ariel García Traba — 20 de noviembre de 2026, 20:09 ART
# Origen: Auditoría de Rafael Lore Truninger, Rondas 6 y 7
# ═══════════════════════════════════════════════════════════════════════
