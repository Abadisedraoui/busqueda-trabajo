# Revisión diaria v3

1. Ejecutar `python check_all_companies.py --browser`.
2. Abrir primero `dashboard.html` y comprobar la cobertura real.
3. Revisar `coverage_report.csv`: ningún `unresolved*` o `error` debe interpretarse como “sin vacantes”.
4. Leer `nuevas_ofertas.csv` y verificar el enlace oficial de cada oferta.
5. Puntuar las ofertas nuevas con el CV y `reglas_puntuacion.md`.
6. Actualizar `digest.md`, `historial_puntuaciones.csv` e `historial.html` como en el flujo anterior.
7. Si un error/unresolved se repite, corregir la URL/ATS de esa empresa en la watchlist o añadir un adaptador específico.
8. No borrar `ofertas_vistas.csv`: es la memoria de deduplicación.
