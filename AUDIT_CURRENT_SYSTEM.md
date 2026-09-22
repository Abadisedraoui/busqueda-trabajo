# Auditoría del sistema actual

Auditoría realizada sobre `watchlist_consolidado.xlsx` adjunto (306 filas de empresas).

## Distribución de `plataforma_ats`

| Valor | Filas |
|---|---:|
| no_se | 76 |
| greenhouse | 63 |
| verificar | 46 |
| ashby | 40 |
| otro | 34 |
| lever | 17 |
| teamtailor | 11 |
| workable | 5 |
| recruitee | 5 |
| workday | 4 |
| icims | 3 |
| breezyhr | 1 |
| agencia_excluir | 1 |
| **Total** | **306** |

## Problema del `check_boards.py` actual

El bucle solo acepta explícitamente:

- greenhouse
- lever
- ashby
- teamtailor
- recruitee
- smartrecruiters

Con la watchlist actual, **170 de 306 filas quedan descartadas antes de intentar ninguna petición** por tener otro valor de plataforma o no tener URL. Es decir, el script no está monitorizando realmente toda la watchlist.

Además, el sistema actual no genera un informe con una fila por empresa, así que un skip y una empresa correctamente comprobada pueden parecer lo mismo desde el digest.

## Qué cambia en v2

`check_all_companies.py` procesa cada fila y la registra en `coverage_report.csv`. Añade Workable, Workday, Personio, detección automática de ATS, descubrimiento de la página oficial de careers, extracción HTML/JSON-LD y fallback de navegador para portales JavaScript.
