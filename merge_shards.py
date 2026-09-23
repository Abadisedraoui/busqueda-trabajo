#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

import check_all_companies as m

BASE = Path(__file__).resolve().parent
SHARDS = BASE / "shards"
COVERAGE_HEADERS = ["row","empresa","input_url","platform_hint","resolved_url","detected_platform","resolution_source","strategy","status","all_jobs_seen","design_jobs_found","warning","error","seconds","checked_at"]
JOB_HEADERS = ["empresa","titulo","url","plataforma","ubicacion","descripcion","external_id"]
SEEN_HEADERS = ["empresa","titulo","url","fecha_visto","signature","content_fingerprint"]


def read_csv(path: Path):
    if not path.exists(): return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def job_from(r):
    return m.Job(r.get("empresa", ""), r.get("titulo", ""), r.get("url", ""), r.get("plataforma", ""), r.get("ubicacion", ""), r.get("descripcion", ""), r.get("external_id", ""))


def dedupe(rows):
    out=[]; sigs=set(); fps=set(); urls=set()
    for r in rows:
        j=job_from(r); fp=j.content_fingerprint
        if j.signature in sigs or j.canonical_url in urls or (fp and fp in fps):
            continue
        sigs.add(j.signature); urls.add(j.canonical_url)
        if fp: fps.add(fp)
        out.append(j)
    return out


def main():
    dirs=sorted([p for p in SHARDS.iterdir() if p.is_dir()]) if SHARDS.exists() else []
    if not dirs: raise SystemExit("No shard artifacts found")

    coverage=[]; open_rows=[]; new_rows=[]; merged_cache={}
    for d in dirs:
        coverage += read_csv(d/"coverage_report.csv")
        open_rows += read_csv(d/"all_open_design_jobs.csv")
        new_rows += read_csv(d/"nuevas_ofertas.csv")
        cf=d/"resolution_cache.json"
        if cf.exists():
            try:
                data=json.loads(cf.read_text(encoding="utf-8"))
                if isinstance(data, dict): merged_cache.update(data)
            except Exception: pass

    coverage.sort(key=lambda r: int(r.get("row") or 0))
    open_jobs=dedupe(open_rows)
    candidate_new=dedupe(new_rows)

    seen_rows=read_csv(BASE/"ofertas_vistas.csv")
    seen_urls={m.canonicalize_url(r.get("url", "")) for r in seen_rows if r.get("url")}
    seen_sigs={r.get("signature", "") for r in seen_rows if r.get("signature")}
    seen_fps={r.get("content_fingerprint", "") for r in seen_rows if r.get("content_fingerprint")}
    truly_new=[]
    today=datetime.now().date().isoformat()
    for j in candidate_new:
        fp=j.content_fingerprint
        if j.canonical_url in seen_urls or j.signature in seen_sigs or (fp and fp in seen_fps):
            continue
        truly_new.append(j)
        seen_rows.append({"empresa":j.company,"titulo":j.title,"url":j.url,"fecha_visto":today,"signature":j.signature,"content_fingerprint":fp})
        seen_urls.add(j.canonical_url); seen_sigs.add(j.signature)
        if fp: seen_fps.add(fp)

    def jr(j):
        return {"empresa":j.company,"titulo":j.title,"url":j.url,"plataforma":j.platform,"ubicacion":j.location,"descripcion":j.description,"external_id":j.external_id}

    m.write_csv(BASE/"coverage_report.csv", coverage, COVERAGE_HEADERS)
    m.write_csv(BASE/"all_open_design_jobs.csv", [jr(j) for j in open_jobs], JOB_HEADERS)
    m.write_csv(BASE/"nuevas_ofertas.csv", [jr(j) for j in truly_new], JOB_HEADERS)
    m.write_csv(BASE/"ofertas_vistas.csv", seen_rows, SEEN_HEADERS)
    (BASE/"resolution_cache.json").write_text(json.dumps(merged_cache, ensure_ascii=False, indent=2), encoding="utf-8")
    (BASE/"daily_search_report.md").write_text(m.render_report(coverage, truly_new, open_jobs), encoding="utf-8")
    (BASE/"dashboard.html").write_text(m.render_dashboard(coverage, truly_new, open_jobs), encoding="utf-8")
    print(f"Merged {len(dirs)} shards; {len(coverage)} coverage rows; {len(truly_new)} new jobs")


if __name__ == "__main__":
    main()
