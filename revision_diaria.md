# Revisión diaria de búsqueda de trabajo

Esto es el prompt que debe correr cada mañana. Sigue los pasos en orden.

## 1. Ejecutar el script de comprobación

Corre `python3 check_boards.py` en esta carpeta. Lee su salida por consola:
cuántas empresas se consultaron, cuántas ofertas nuevas encontró, y qué
empresas dieron error o no tienen slug extraíble. Si hay empresas con error
repetido varios días seguidos, avísame en el digest — puede que hayan
cambiado de ATS.

## 2. Buscar más allá del watchlist automatizado

Además de lo que devuelve el script, busca en la web puestos de "Product
Designer" o "UX/UI Designer" en empresas que encajen con mi perfil (SaaS
B2B, EdTech, accesibilidad, sistemas de diseño) que no estén ya en
`watchlist_consolidado.xlsx`.

Regla estricta de verificación: una oferta solo cuenta si puedes confirmar
que está publicada, en este momento, en la página oficial de empleo de la
propia empresa. Un enlace de LinkedIn, InfoJobs o un agregador no cuenta —
si el enlace es de un agregador, entra en la web oficial de la empresa y
confirma que el puesto sigue ahí. Una oferta que ya no está publicada no
cuenta, aunque el agregador la siga mostrando.

Si encuentras una empresa nueva que valga la pena vigilar a largo plazo
(encaja con mi perfil y tiene ritmo de contratación de diseño), añádela a
`watchlist_consolidado.xlsx` con su plataforma ATS si la identificas.

## 3. Puntuar cada oferta nueva

Para cada oferta en `nuevas_ofertas.csv` (y las que hayas encontrado en el
paso 2), léela junto con `resume.md` y `reglas_puntuacion.md`, y puntúala
siguiendo la regla al pie de la letra — no la suavices ni le des el
beneficio de la duda. Si la regla dice que algo descalifica, descalifica.

No inventes nada sobre mi experiencia que no esté en `resume.md`. No
intentes adivinar cómo va a reaccionar la empresa a mi hueco laboral —
eso no es algo que se pueda calcular, puntúa solo el encaje real con la
oferta.

## 4. Escribir el digest

Crea o sobrescribe `digest.md` con tres bloques:

- **Aplicar ya** — encaje alto, sin descalificadores
- **Merece un vistazo** — encaje razonable pero con algún pero
- **Descartar** — no cumple lo mínimo, con una frase de por qué

Para cada oferta: empresa, puesto, enlace, y el razonamiento de la
puntuación visible (no solo un número) para que pueda ver si la regla se
equivocó en algo.

Si no hay ninguna oferta nueva hoy, dilo igualmente en `digest.md` — un
día sin novedades también es información útil, no lo omitas.

## 5. Guardar

Si esta carpeta es un repositorio git, haz commit de
`nuevas_ofertas.csv`, `ofertas_vistas.csv` y `digest.md` con un mensaje
tipo "digest DD-MM-YYYY".
