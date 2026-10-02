# Arte Empleo

Radar paralelo para detectar oportunidades de arte, pintura, docencia creativa y proyectos culturales en Madrid y, cuando tenga sentido, remoto/España.

Este proyecto vive separado de la búsqueda principal de Product/UX para no mezclar historiales ni criterios.

## Qué busca

Cuatro tipos de oportunidad:

1. **Empleo** — profesora de arte/pintura, educadora o mediadora cultural, museos, exposiciones, visual/creative design, visitor experience.
2. **Proyectos / freelance** — muralismo, ilustración, retrato, artwork, editorial, escenografía, decoración e intervenciones artísticas.
3. **Eventos / encargos** — live painting, retratos en bodas y eventos, activaciones de marca, workshops y colaboraciones puntuales.
4. **Convocatorias** — residencias, exposiciones, concursos, becas, arte público y open calls.

## Perfil objetivo

El filtro está pensado para un perfil híbrido con formación en Product Design e Interior Design, experiencia profesional en UX/UI y diseño visual/editorial, Adobe Creative Suite, pintura/dibujo y experiencia preparando o impartiendo actividades creativas.

No presupone experiencia profesional como muralista, wedding painter o artista de eventos si no está acreditada. Esas oportunidades se conservan como posibles encargos cuando el portfolio artístico pueda ser suficiente.

## Archivos

- `profile_arte.md` — perfil profesional relevante para este radar.
- `sources_arte.csv` — fuentes oficiales que el bot revisa.
- `keywords_arte.json` — palabras de inclusión, exclusión y categorías.
- `reglas_encaje_arte.md` — cómo valorar una oportunidad.
- `check_art_opportunities.py` — scraper conservador con cobertura auditable.
- `opportunities_seen.csv` — histórico ligero de URLs ya vistas.
- `all_open_art_opportunities.csv` — snapshot actual.
- `nuevas_oportunidades.csv` — novedades de la ejecución.
- `coverage_report_arte.csv` — una fila por fuente revisada.
- `daily_art_report.md` — digest legible.
- `PROMPT_SISTEMA_ARTE.md` — especificación completa del sistema.

## Ejecución

```bash
pip install -r arte-empleo/requirements.txt
python arte-empleo/check_art_opportunities.py
```

GitHub Actions lo ejecuta mediante `.github/workflows/daily-art-search.yml`.

## Principio importante

No se interpreta una web sin resultados como "no hay oportunidades" si el listado no se ha podido leer correctamente. En ese caso la fuente queda como `unresolved_listing_not_parsed` o `error`.

La automatización de GitHub cubre la **watchlist fija**. Las fuentes abiertas (LinkedIn, Indeed, InfoJobs, búsquedas web, Instagram, agencias de eventos, wedding planners, etc.) requieren una capa adicional de descubrimiento; están definidas en el prompt maestro para revisarlas cuando se ejecute una búsqueda abierta.
