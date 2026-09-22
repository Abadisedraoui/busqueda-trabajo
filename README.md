# Job Search Automation v3

Sistema para revisar **todas las empresas** de `watchlist_consolidado.xlsx` y detectar vacantes de diseño sin saltarse filas silenciosamente.

## Qué puestos detecta

La búsqueda es deliberadamente amplia. Incluye, entre otras variaciones:

- Product Designer / Senior Product Designer / Digital Product Designer
- UX Designer / UI Designer
- UX/UI Designer / UI/UX Designer
- Web Designer / Web UX Designer
- Visual Designer / Digital Designer
- User Experience Designer / User Interface Designer
- Interaction Designer / Experience Designer / Interface Designer
- Design Systems / Design Systems Designer
- equivalentes habituales en español

Se excluyen falsos positivos claros de diseño físico/ingeniería como `Product Design Engineer`, CAD, Mechanical o Industrial Designer. Los puestos Head/Lead/Manager **sí se detectan**: se decide después si encajan mediante las reglas de puntuación.

## Cómo reduce fallos

1. Procesa cada fila y la registra en `coverage_report.csv`.
2. Reintenta errores temporales HTTP (429, 5xx, timeouts de conexión).
3. Detecta ATS tanto por dominio como por señales dentro del HTML, útil para dominios personalizados.
4. Usa APIs/feeds cuando existen y, si fallan, degrada a lectura HTML/Playwright.
5. En webs propias sigue enlaces tipo `Open roles`, `Jobs`, `Vacancies`, etc. antes de rendirse.
6. Las URLs cacheadas caducan y se redescubren si dejan de funcionar.
7. Conserva parámetros de URL que identifican una vacante y elimina solo tracking.
8. Detecta duplicados por URL/ID y también por contenido cuando dos requisiciones tienen la misma descripción.
9. Si una web propia no permite verificar ninguna oferta, **no** asume que no hay vacantes: queda como `unresolved_listing_not_parsed`.
10. Incluye tests automáticos antes de cada ejecución de GitHub Actions.

## Instalación local

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Prueba de una empresa:

```bash
python check_all_companies.py --company "Notion" --browser
```

Ejecución completa:

```bash
python check_all_companies.py --browser
```

## Interfaz y resultados

- `dashboard.html` — interfaz visual para leer rápidamente cobertura, ofertas y errores.
- `coverage_report.csv` — una fila por empresa con método, ATS, estado y error.
- `all_open_design_jobs.csv` — snapshot de vacantes de diseño abiertas detectadas.
- `nuevas_ofertas.csv` — solo nuevas respecto al histórico.
- `ofertas_vistas.csv` — histórico persistente para deduplicar.
- `daily_search_report.md` — resumen legible de cada ejecución.
- `resolution_cache.json` — URLs/ATS descubiertos para no resolverlos desde cero cada día.

### Estados importantes

- `checked_design_found`: revisión correcta y se encontraron puestos objetivo.
- `checked_no_design`: revisión con suficiente señal y sin puestos objetivo.
- `unresolved`: no se encontró una URL oficial fiable.
- `unresolved_listing_not_parsed`: se llegó a la web, pero no se pudo verificar bien su listado; no se considera “cero ofertas”.
- `error`: fallo técnico que agotó los fallbacks.

## Subirlo a GitHub

Si ya tienes el repositorio anterior, copia estos archivos a la **raíz de ese repositorio** y sustituye los equivalentes:

```text
check_all_companies.py
requirements.txt
watchlist_consolidado.xlsx
ofertas_vistas.csv
resolution_cache.json
revision_diaria_v2.md
.github/workflows/daily-job-search.yml
tests/test_job_search.py
```

Puedes conservar `resume.md`, `reglas_puntuacion.md`, `digest.md`, `historial_puntuaciones.csv`, `generar_historial_html.py` y el resto de tu flujo anterior.

El antiguo `check_boards.py` ya no es necesario para la automatización diaria; puedes moverlo a una carpeta `archive/` o eliminarlo cuando compruebes que v3 funciona.

**Importante:** conserva/sube `ofertas_vistas.csv`. Si lo borras, la primera ejecución puede considerar como nuevas ofertas que ya habías visto.

Los siguientes archivos los genera/actualiza el bot automáticamente y se pueden dejar versionados en GitHub:

```text
dashboard.html
coverage_report.csv
all_open_design_jobs.csv
nuevas_ofertas.csv
daily_search_report.md
resolution_cache.json
ofertas_vistas.csv
```

Después de hacer push, abre **Actions → Daily job search → Run workflow** una vez manualmente. Revisa primero `dashboard.html` y `coverage_report.csv`; solo después conviene confiar en la ejecución diaria.

## Limitación real

No existe una API universal para las webs de empleo. Algunas compañías cambian de ATS, bloquean automatizaciones o usan portales muy dinámicos. El objetivo del sistema no es fingir un 100 %: es maximizar la cobertura y hacer visible exactamente qué empresa no pudo verificarse y por qué.
