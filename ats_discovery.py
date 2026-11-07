"""Barrido ATS-first independiente de la watchlist. No modifica ofertas_vistas.csv."""
from __future__ import annotations
import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from check_all_companies import (
    Job, build_session, fetch_greenhouse, fetch_lever, fetch_ashby,
    is_design_title, load_seen, canonicalize_url, norm,
)

ROOT = Path(__file__).resolve().parent
SEEDS = ROOT / "ats_discovery_sources.csv"
OUTPUT = ROOT / "ats_discovery_all.csv"
CANDIDATES = ROOT / "ats_discovery_candidates.csv"
COVERAGE = ROOT / "ats_discovery_coverage.csv"
SUPPORTED = {"greenhouse": fetch_greenhouse, "lever": fetch_lever, "ashby": fetch_ashby}

def read_sources(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def classify(job, seen_urls, seen_signatures, seen_fingerprints):
    if (job.canonical_url in seen_urls or job.signature in seen_signatures
            or (job.content_fingerprint and job.content_fingerprint in seen_fingerprints)):
        return "repetida_csv"
    return "posible_nueva_tracker_pendiente"

def write_csv(path, rows, headers):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sources", type=Path, default=SEEDS)
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args()
    sources = read_sources(args.sources)
    if args.limit:
        sources = sources[:args.limit]
    session = build_session()
    seen_urls, seen_signatures, seen_fingerprints = load_seen()
    found, coverage, unique = [], [], set()
    for index, source in enumerate(sources, 1):
        company, ats, url = (source.get(k) or "").strip() for k in ("empresa", "ats", "url")
        print(f"[{index}/{len(sources)}] {company} ({ats})", flush=True)
        entry = {"empresa": company, "ats": ats, "url": url, "estado": "", "ofertas_totales": 0, "ofertas_diseno": 0, "error": ""}
        try:
            if ats not in SUPPORTED:
                raise ValueError(f"ATS no soportado: {ats}")
            jobs = SUPPORTED[ats](session, company, url)
            entry["ofertas_totales"] = len(jobs)
            for job in jobs:
                if not job.url or not is_design_title(job.title):
                    continue
                entry["ofertas_diseno"] += 1
                key = (norm(job.company), job.canonical_url)
                if key in unique:
                    continue
                unique.add(key)
                found.append({
                    "empresa": job.company, "titulo": job.title, "ubicacion": job.location,
                    "url": job.url, "ats": ats, "estado": classify(job, seen_urls, seen_signatures, seen_fingerprints),
                    "descripcion": job.description, "fecha_revision": datetime.now().isoformat(timespec="seconds"),
                })
            entry["estado"] = "comprobado"
        except Exception as exc:
            entry["estado"] = "error"
            entry["error"] = f"{type(exc).__name__}: {exc}"
        coverage.append(entry)
    fields = ["empresa", "titulo", "ubicacion", "url", "ats", "estado", "descripcion", "fecha_revision"]
    write_csv(OUTPUT, found, fields)
    write_csv(CANDIDATES, [x for x in found if x["estado"] != "repetida_csv"], fields)
    write_csv(COVERAGE, coverage, ["empresa", "ats", "url", "estado", "ofertas_totales", "ofertas_diseno", "error"])
    print(json.dumps({"fuentes": len(sources), "verificadas": sum(x["estado"] == "comprobado" for x in coverage),
        "ofertas_diseno": len(found), "posibles_nuevas": sum(x["estado"] != "repetida_csv" for x in found),
        "errores": sum(x["estado"] == "error" for x in coverage)}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
