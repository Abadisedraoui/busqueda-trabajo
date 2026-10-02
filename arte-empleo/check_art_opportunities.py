#!/usr/bin/env python3
import csv, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse, parse_qsl, urlencode

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources_arte.csv"
KEYWORDS = ROOT / "keywords_arte.json"
SEEN = ROOT / "opportunities_seen.csv"
ALL = ROOT / "all_open_art_opportunities.csv"
NEW = ROOT / "nuevas_oportunidades.csv"
COVERAGE = ROOT / "coverage_report_arte.csv"
REPORT = ROOT / "daily_art_report.md"

HEADERS = {"User-Agent":"Mozilla/5.0 (compatible; arte-empleo-bot/1.0)"}

def norm_url(url):
    try:
        p=urlparse(url)
        qs=[(k,v) for k,v in parse_qsl(p.query, keep_blank_values=True)
            if k.lower() not in {"utm_source","utm_medium","utm_campaign","utm_term","utm_content","fbclid","gclid"}]
        return urlunparse((p.scheme,p.netloc,p.path,p.params,urlencode(qs),p.fragment))
    except Exception:
        return url

def load_seen():
    if not SEEN.exists(): return set()
    with SEEN.open(encoding="utf-8", newline="") as f:
        return {norm_url(r["url"]) for r in csv.DictReader(f) if r.get("url")}

def classify(text, cfg):
    low=text.lower()
    for ex in cfg["exclude"]:
        if ex in low: return None, None
    for cat, terms in cfg["categories"].items():
        for t in terms:
            if t in low:
                sub=cat
                if cat=="freelance_project" and "mural" in low: sub="muralism"
                if cat=="events_commissions": sub="events_live_art"
                if cat=="open_call": sub="residency_grant"
                return cat, sub
    return None, None

def extract_links(base_url, html, cfg):
    soup=BeautifulSoup(html,"html.parser")
    out=[]
    for a in soup.find_all("a", href=True):
        title=" ".join(a.get_text(" ", strip=True).split())
        href=urljoin(base_url, a["href"])
        context=(title+" "+a.get("aria-label","")+" "+href)
        cat, sub=classify(context, cfg)
        if not cat: 
            continue
        out.append({
            "title": title or href,
            "url": norm_url(href),
            "category": cat,
            "subcategory": sub or cat
        })
    return out

def main():
    cfg=json.loads(KEYWORDS.read_text(encoding="utf-8"))
    seen=load_seen()
    now=datetime.now(timezone.utc).isoformat()
    opportunities=[]
    coverage=[]

    with SOURCES.open(encoding="utf-8", newline="") as f:
        sources=list(csv.DictReader(f))

    for src in sources:
        err=""
        status="checked_no_relevant"
        http_status=""
        links_scanned=0
        relevant=0
        try:
            r=requests.get(src["url"], headers=HEADERS, timeout=25, allow_redirects=True)
            http_status=str(r.status_code)
            if r.status_code in (401,403,429):
                status="blocked"
            elif r.status_code>=400:
                status="error"
                err=f"HTTP {r.status_code}"
            else:
                links=extract_links(r.url, r.text, cfg)
                links_scanned=len(BeautifulSoup(r.text,"html.parser").find_all("a"))
                seen_here=set()
                for item in links:
                    key=(item["title"].lower(), item["url"])
                    if key in seen_here: continue
                    seen_here.add(key)
                    item.update({
                        "source_name":src["source_name"],
                        "location":src.get("location",""),
                        "status":"open_or_listed",
                        "discovered_at":now
                    })
                    opportunities.append(item)
                relevant=len(links)
                if relevant:
                    status="checked_relevant_found"
                elif links_scanned < 2:
                    status="unresolved_listing_not_parsed"
        except Exception as e:
            status="error"
            err=str(e)[:300]

        coverage.append({
            "source_name":src["source_name"],"url":src["url"],"status":status,
            "http_status":http_status,"links_scanned":links_scanned,
            "relevant_found":relevant,"error":err,"checked_at":now
        })
        time.sleep(0.4)

    # dedupe global
    dedup={}
    for o in opportunities:
        dedup[(o["source_name"].lower(),o["title"].lower(),o["url"])]=o
    opportunities=list(dedup.values())

    fields=["source_name","title","url","category","subcategory","location","status","discovered_at"]
    with ALL.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(opportunities)

    new=[o for o in opportunities if norm_url(o["url"]) not in seen]
    with NEW.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(new)

    seen_exists=SEEN.exists() and SEEN.stat().st_size>0
    with SEEN.open("a",encoding="utf-8",newline="") as f:
        sw=csv.DictWriter(f,fieldnames=["source_name","title","url","category","first_seen"])
        if not seen_exists: sw.writeheader()
        for o in new:
            sw.writerow({"source_name":o["source_name"],"title":o["title"],"url":o["url"],
                         "category":o["category"],"first_seen":now[:10]})

    cfields=["source_name","url","status","http_status","links_scanned","relevant_found","error","checked_at"]
    with COVERAGE.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cfields); w.writeheader(); w.writerows(coverage)

    groups=[("employment","Empleo"),("freelance_project","Proyectos / freelance"),
            ("events_commissions","Eventos / encargos"),("open_call","Convocatorias / residencias")]
    lines=["# Daily art opportunity report","",f"Checked: {len(sources)} sources",f"New opportunities: {len(new)}",""]
    for key,label in groups:
        lines += [f"## {label}"]
        rows=[o for o in new if o["category"]==key]
        if not rows:
            lines += ["- Sin novedades detectadas.",""]
        else:
            for o in rows[:50]:
                lines.append(f"- [{o['title']}]({o['url']}) — {o['source_name']}")
            lines.append("")
    unresolved=[c for c in coverage if c["status"] not in {"checked_relevant_found","checked_no_relevant"}]
    lines += ["## Cobertura / problemas", f"- Fuentes con incidencia: {len(unresolved)}"]
    for c in unresolved[:30]:
        lines.append(f"- {c['source_name']}: {c['status']} {c['error']}".rstrip())
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
