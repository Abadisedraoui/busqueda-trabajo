# Prompt maestro — sistema automatizado de búsqueda de empleo

## Contexto
Soy Zainab Abadi, Product & UX/UI Designer basada en Madrid, con 4+ años de experiencia. Te proporciono:

1. Mi CV actual, que es la fuente de verdad de mi experiencia profesional.
2. `watchlist_consolidado.xlsx`, con todas las empresas que quiero vigilar.
3. Mi Excel `Job Hunting 2026.xlsx`, con ofertas que ya he analizado o a las que he aplicado.
4. Un histórico de ofertas ya vistas, para no repetir resultados.

Quiero un sistema de búsqueda de empleo **automatizado, auditable y conservador**. El objetivo es detectar vacantes nuevas de Product Designer / UX/UI / Product Design en las empresas indicadas y ayudarme a priorizarlas por encaje real con mi experiencia.

## Regla principal: revisar TODAS las empresas
No quiero un script que solo revise las empresas con Greenhouse, Lever o Ashby y omita el resto.

Cada fila de `watchlist_consolidado.xlsx` debe terminar cada día en uno de estos estados:
- revisada correctamente;
- revisada y sin vacantes de diseño;
- URL/ATS resuelto automáticamente;
- error técnico concreto;
- pendiente de resolución, explicando exactamente por qué.

**Nunca se puede saltar una empresa en silencio.** Debe existir un informe de cobertura con una fila por empresa para poder comprobar cuántas se han revisado realmente.

## Cómo buscar

La búsqueda tiene dos capas:

- **Barrido abierto del mercado** para descubrir empresas y vacantes fuera de la watchlist. Usar activamente LinkedIn, Indeed, Glassdoor, InfoJobs, Jobgether, Google Jobs, **IxDF Jobs**, **Wellfound**, **UI/UX Jobs Board**, **Matcha**, **Himalayas**, **Remote.io** y **YC Work at a Startup**, además de otros portales relevantes.
- **Watchlist** para revisar las empresas conocidas mediante sus páginas oficiales y ATS.

IxDF, Wellfound, UI/UX Jobs Board, Matcha, Himalayas, Remote.io y YC Work at a Startup son fuentes fijas de descubrimiento. En IxDF, si la empresa está oculta, conservar la oferta como `IxDF / empresa oculta` con título y URL para poder deduplicarla posteriormente. Intentar identificar la empresa por el contenido antes de descartarla.

Aplicar este orden:

1. Si la empresa usa un ATS con feed/API pública, usarlo directamente. Soportar como mínimo:
   - Greenhouse
   - Lever
   - Ashby
   - Workable
   - Workday
   - SmartRecruiters
   - Recruitee
   - Personio
   - Teamtailor
   - iCIMS / Jobvite / BreezyHR mediante extracción pública cuando sea posible.

2. Si `web_empleo` apunta a la web corporativa, abrir esa página y detectar automáticamente si redirige o enlaza a un ATS.

3. Si no hay ATS detectable, revisar la propia web oficial:
   - JSON-LD `JobPosting`;
   - enlaces de vacantes;
   - portal renderizado con navegador cuando el contenido dependa de JavaScript.

4. Si el Excel no tiene una URL oficial o solo tiene LinkedIn/InfoJobs/otro agregador, localizar primero la página oficial de careers de la empresa y guardar/cachar ese resultado para futuras ejecuciones.

Los agregadores sirven activamente para descubrir ofertas. Cuando sea posible, verificar después la misma vacante en la web oficial o ATS. Si no se encuentra la fuente oficial pero la oferta parece vigente y relevante, **conservarla** y marcarla como `Agregador sin verificación oficial`.

Clasificar cada oferta como `Oficial/ATS`, `Agregador verificado oficialmente` o `Agregador sin verificación oficial`.

## Sistema de descubrimiento fuera de LinkedIn

LinkedIn es una fuente más, no el centro del sistema. Además de buscar vacantes publicadas, cada barrido debe intentar detectar tres tipos de oportunidad:

1. **Ofertas nuevas**: vacantes relevantes encontradas en portales especializados, careers pages, ATS y agregadores, aunque no estén publicadas en LinkedIn.
2. **Señales de contratación**: empresas compatibles con el perfil que estén ampliando equipos de Product/Engineering/Design, entrando en España/Europa, levantando financiación o mostrando otras señales recientes de crecimiento que puedan anticipar contratación de diseño. Estas señales no cuentan como ofertas y deben ir separadas.
3. **Puertas de entrada fuera del anuncio**: cuando exista una empresa u oferta especialmente interesante, localizar vías razonables y concretas como recruiters especializados en Product/UX, equipo de Talent de la empresa, comunidades profesionales, eventos, referrals o contactos relevantes. No generar outreach masivo ni mensajes genéricos.

Añadir también un enfoque de **reverse search**: descubrir empresas que encajen especialmente con el perfil aunque todavía no tengan una vacante de diseño visible. Priorizar B2B SaaS, plataformas complejas, edtech, accessibility, design systems, AI/productivity tools y compañías con equipos Product + Engineering. Incluirlas solo cuando exista una señal concreta que justifique vigilarlas.

El informe diario debe separar claramente:
- **Ofertas nuevas**
- **Empresas con señales de contratación**
- **Puertas de entrada / oportunidades fuera del anuncio**

No presentar una señal de contratación como si fuera una vacante. No saturar el informe con noticias corporativas genéricas: incluir solo señales recientes y accionables.

## Qué puestos buscar
Filtrar por títulos relacionados con:
- Product Designer / Product Design
- UX Designer
- UI/UX o UX/UI Designer
- User Experience Designer
- Interaction Designer
- Experience Designer
- Design Systems / Design System Designer

No limitar por seniority en la fase de descubrimiento: quiero poder ver también roles Senior, Staff o Lead y decidir después si encajan.

## Deduplicación
Antes de llamar a una oferta `Nueva`, comprobarla contra **AMBOS** históricos: `ofertas_vistas.csv` y `Job Hunting 2026.xlsx`. Comparar empresa + título + URL y variantes obvias del título. Si el Excel no puede comprobarse de forma completa o hay dudas, usar `posible repetida` o `posible nueva`, nunca `Nueva`.

Mantener `ofertas_vistas.csv` como índice ligero de ofertas revisadas. Registrar solo los datos necesarios para deduplicación; no guardar copias completas de cada descripción.

Normalizar las URLs para ignorar parámetros de tracking. Cuando dos requisiciones distintas correspondan claramente al mismo puesto real, señalarlas como posible duplicado para revisión.

## Salidas obligatorias de la búsqueda
Cada ejecución debe producir:

- `nuevas_ofertas.csv`: solo las ofertas nuevas encontradas hoy.
- `all_open_design_jobs.csv`: snapshot de todas las vacantes de diseño actualmente abiertas detectadas.
- `ofertas_vistas.csv`: histórico acumulativo.
- `coverage_report.csv`: una fila por empresa con URL resuelta, ATS detectado, método usado, número de ofertas revisadas, número de ofertas de diseño, estado y error si lo hay.
- `resolution_cache.json`: URLs y ATS descubiertos para no repetir trabajo cada día.
- `daily_search_report.md`: resumen de cobertura y nuevas ofertas.

## Evaluación de encaje
Después de descubrir las ofertas nuevas, leer su descripción completa junto con mi CV y `reglas_puntuacion.md`.

La puntuación mide **encaje entre el rol y mi perfil**, no la probabilidad de que me contraten. No inventar experiencia ni intentar predecir cómo reaccionará una empresa a mi trayectoria o a un career break.

Aplicar literalmente los criterios de `reglas_puntuacion.md`, pero si una oferta tiene un requisito esencial que mi CV no acredita (por ejemplo, people management cuando el puesto es principalmente de gestión), debe quedar visible como desajuste esencial aunque la suma de puntos sea alta.

## Digest diario
Generar `digest.md` con:

- **Aplicar ya**
- **Merece un vistazo**
- **Descartar**

Para cada oferta: empresa, puesto, enlace oficial, puntuación y razonamiento visible. Si no hay ofertas nuevas, decirlo expresamente.

Añadir las ofertas puntuadas a `historial_puntuaciones.csv` y regenerar `historial.html`.

## Automatización real
El proceso debe poder ejecutarse sin intervención manual cada mañana mediante GitHub Actions o cron. La ejecución automática debe:

1. instalar dependencias;
2. ejecutar la búsqueda sobre toda la watchlist;
3. guardar los informes y CSV actualizados;
4. hacer commit únicamente cuando haya cambios.

La cobertura importa tanto como las ofertas encontradas: si una empresa no puede revisarse, quiero verlo en el informe y arreglar esa empresa concreta, no asumir que fue comprobada.
