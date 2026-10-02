# Prompt maestro — radar de arte, empleo creativo y encargos

## Objetivo

Mantener un sistema automatizado, auditable y conservador para encontrar oportunidades que puedan encajar con un perfil híbrido de diseño + arte en Madrid.

No limitar la búsqueda a empleo tradicional.

## Tipos de oportunidad

Clasificar cada resultado en exactamente una categoría principal:

1. `employment` — contrato o puesto estable/temporal.
2. `freelance_project` — proyecto o colaboración profesional puntual.
3. `events_commissions` — bodas, eventos, retratos, live painting, activaciones.
4. `open_call` — convocatoria, residencia, exposición, concurso, beca o ayuda.

Añadir una subcategoría:
- teaching
- cultural_mediation
- exhibition_experience
- creative_design
- muralism
- illustration_portrait
- events_live_art
- residency_grant
- museum_operations
- other_creative

## Fuentes fijas

Revisar todas las filas de `sources_arte.csv`.
Nunca saltar una fuente en silencio.

Cada fuente debe terminar como:
- checked_relevant_found
- checked_no_relevant
- unresolved_listing_not_parsed
- blocked
- error

## Descubrimiento abierto

Además de la watchlist, cuando la búsqueda se haga con acceso web revisar activamente:

- LinkedIn
- Indeed
- InfoJobs
- Google Jobs / búsqueda web
- Domestika
- portales culturales
- webs de museos, fundaciones y centros culturales
- colegios, academias y empresas de extraescolares
- agencias de eventos y experiential marketing
- wedding planners y proveedores de bodas
- estudios de interiorismo, escenografía y producción
- productoras y agencias creativas
- Instagram/web pública cuando exista una llamada concreta a artistas
- ayuntamientos, Comunidad de Madrid, Ministerio de Cultura, BOE/BOCM
- convocatorias de arte público, muralismo y residencias

## Búsquedas abiertas sugeridas

Combinar Madrid/España con:
- profesora pintura / profesor dibujo / art teacher
- tallerista arte / monitor artes plásticas
- mediador cultural / museum educator
- exhibition designer / museografía / diseño expositivo
- muralista / mural / arte urbano / intervención artística
- artista freelance / colaboración artista / artista para proyecto
- retratos eventos / retratos bodas / wedding painter / live painter
- artista evento / activación de marca / live illustration
- convocatoria artista / open call Madrid / residencia artística
- concurso mural / arte público / convocatoria artes visuales

## Verificación

Cuando una oportunidad venga de un agregador, buscar la fuente oficial cuando sea posible.
Conservarla si no se encuentra fuente oficial pero parece vigente, marcando `aggregator_unverified`.

No presentar como nueva una convocatoria cerrada solo porque siga indexada.
Registrar deadline y estado cuando estén publicados.

## Deduplicación

Comparar URL normalizada + título + organización.
Eliminar parámetros de tracking.
Mantener `opportunities_seen.csv` como histórico ligero.

## Salidas

Cada ejecución debe generar:
- `nuevas_oportunidades.csv`
- `all_open_art_opportunities.csv`
- `opportunities_seen.csv`
- `coverage_report_arte.csv`
- `daily_art_report.md`

El digest debe separar:
- Empleo
- Proyectos / freelance
- Eventos / encargos
- Convocatorias / residencias

## Evaluación

Usar `profile_arte.md` y `reglas_encaje_arte.md`.

No inventar experiencia.
Distinguir experiencia acreditada, habilidad transferible y oportunidad exploratoria.
