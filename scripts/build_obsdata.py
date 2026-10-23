#!/usr/bin/env python3
"""Build the ISIMIP4 local-lake observation database (water temperature and hypsometry).

    python3 -I scripts/build_obsdata.py --isimip3 <ISIMIP_Local_Lakes clone> --isimip4 <ISIMIP4 delivery LocalLakes>
            --sheet <sheet csv dir> --protocol <lake_site.yaml> --out <repository root> [--include Lake,...]

Inputs
  --isimip3   clone of https://github.com/icra/ISIMIP_Local_Lakes (ISIMIP3 database, public)
  --isimip4   the ISIMIP4 local-lake delivery (LocalLakes/<Lake>/..., collected by the ISIMIP lake sector)
  --sheet     the ISIMIP4 local-lakes coordination sheet, exported as CSV (metadata_hydrothermal.csv,
              metadata_hydrothermal_corrected.csv, metadata_waterquality.csv)
  --protocol  isimip-protocol-4 definitions/lake_site.yaml (lake-site identifiers, titles, coordinates)

Outputs (under --out)
  LocalLakes/<Lake>/<site>_watertemp_daily.csv            one value per day and depth
  LocalLakes/<Lake>/<site>_watertemp_subdaily_<yyyy>.csv.gz  cleaned sub-daily records, one file per year
  LocalLakes/<Lake>/<site>_hypsometry.csv                 depth below the surface vs area
  metadata/lakes.csv, metadata/source_files.csv, metadata/corrections.csv

Every value removed or changed is counted in metadata/corrections.csv with the rule that did it;
the rules are documented in docs/CORRECTIONS.md. Nothing is interpolated or gap-filled.
"""
import argparse
import gzip
import hashlib
import io
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

TMIN, TMAX = -0.5, 40.0            # liquid lake water; below -0.5 C = logger frozen into the ice
SENTINELS = [-9999.0, -999.0, -99.0]
# Lakes whose ISIMIP4 delivery may not be redistributed (water-quality sheet: "no (only accessible to
# the ISIMIP3 lake sector modellers)"): their ISIMIP4 files are not used; the public ISIMIP3 files are.
ISIMIP4_RESTRICTED = {"Bosumtwi"}
# Lake-specific value ranges, checked by hand (docs/CORRECTIONS.md)
LAKE_RANGE = {"Bosumtwi": (24.0, 33.0, "temperature = depth entries (depth typed in the temperature column)")}
# ISIMIP3 files filed under another lake (folder, file pattern) -> lake they belong to, with the evidence
REASSIGN = [
    ("Zurich", "*Temp*.csv", "LowerLakeZurich",
     "the 'Zurich' folder holds Lower Lake Zurich data (CH-ZUR rows = the ISIMIP4 Lower Lake Zurich file, 1981-2022)"),
    ("Rappbodep", "*subdaily*.csv", "Rappbode",
     "profiles reach 48-79 m but the pre-dam is ~17 m deep; the 44 days of 2015 that are also in the Rappbode reservoir "
     "daily file are identical to it (max difference < 1e-8 C): main-reservoir data filed under the pre-dam"),
]


class Log:
    def __init__(self):
        self.rows = []

    def add(self, lake, file, rule, n, detail=""):
        if n:
            self.rows.append({"lake": lake, "file": file, "rule": rule, "n_values": int(n), "detail": detail})


LOG = Log()
SOURCES = []


def sha256(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def norm(c):
    return re.sub(r"[^A-Z0-9]+", "_", str(c).strip().upper()).strip("_")


def read_table(f):
    """CSV with tolerant header handling; returns a frame of strings with normalised column names."""
    text = Path(f).read_text(encoding="utf-8-sig", errors="replace")
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) <= 1:
        return pd.DataFrame(), "empty file (header only)"
    head = [norm(c) for c in next(iter(pd.read_csv(io.StringIO(lines[0]), header=None, dtype=str).values))]
    nf = len(lines[1].split(","))
    note = ""
    if nf == 5 and head == ["SITE_ID", "SITE_NAME", "TIMESTAMP", "WTEMP"]:
        head = ["SITE_ID", "SITE_NAME", "TIMESTAMP", "DEPTH", "WTEMP"]      # Zurich_Temp.csv: DEPTH missing in header
        note = "header lacked the DEPTH column (5 data columns, 4 names); columns re-assigned"
    d = pd.read_csv(io.StringIO("\n".join(lines[1:])), header=None, dtype=str, keep_default_na=False)
    d = d.iloc[:, :len(head)]
    d.columns = head[:d.shape[1]]
    d = d.loc[:, [c for c in d.columns if c]]
    return d, note


def parse_time(s, lake, fname, ref=None):
    """yyyymmdd, yyyymmddHHMM, ISO dates; 6-digit yymmdd only when it falls inside the file's own span."""
    s = s.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    t = pd.to_datetime(s.where(s.str.fullmatch(r"\d{8}")), format="%Y%m%d", errors="coerce")
    t = t.fillna(pd.to_datetime(s.where(s.str.fullmatch(r"\d{12}")), format="%Y%m%d%H%M", errors="coerce"))
    iso = s.where(s.str.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}([ T].*)?"))
    t = t.fillna(pd.to_datetime(iso, errors="coerce", format="mixed"))
    six = s.str.fullmatch(r"\d{6}") & t.isna()
    if six.any():
        cand = pd.to_datetime("20" + s.where(six), format="%Y%m%d", errors="coerce")
        lo, hi = t.min(), t.max()
        ok = cand.notna() & (cand >= lo - pd.Timedelta(days=366)) & (cand <= hi + pd.Timedelta(days=366))
        t = t.where(~(six & ok), cand)
        LOG.add(lake, fname, "date written as yymmdd (6 digits), read as 20yy-mm-dd", int((six & ok).sum()),
                ", ".join(sorted(set(s[six & ok]))[:5]))
    return t


def clean_temp(d, lake, fname, subdaily):
    tcol = "TIMESTAMP_START" if subdaily else "TIMESTAMP"
    vcol = next(c for c in ("WTEMP", "WATERTEMP", "TEMP") if c in d.columns)
    t = parse_time(d[tcol], lake, fname)
    t_end = parse_time(d["TIMESTAMP_END"], lake, fname) if subdaily and "TIMESTAMP_END" in d else None
    z = pd.to_numeric(d["DEPTH"], errors="coerce")
    v = pd.to_numeric(d[vcol].replace({"NA": "", "NaN": "", "nan": "", "NULL": ""}), errors="coerce")
    o = pd.DataFrame({"t": t, "z": z, "v": v})
    if t_end is not None:
        o["t_end"] = t_end
    n0 = len(o)
    bad_t = o.t.isna()
    LOG.add(lake, fname, "missing or unreadable date removed", bad_t.sum())
    o = o[~bad_t]
    LOG.add(lake, fname, "missing depth removed", o.z.isna().sum()); o = o[o.z.notna()]
    if len(o) and (o.z <= 0).all() and (o.z < 0).any():
        LOG.add(lake, fname, "depths given as negative numbers (height); sign flipped to depth below surface", (o.z < 0).sum())
        o = o.assign(z=-o.z)
    neg = o.z < 0
    LOG.add(lake, fname, "negative depth in a file of positive depths removed", neg.sum()); o = o[~neg]
    LOG.add(lake, fname, "missing temperature removed (empty, NA, NaN)", o.v.isna().sum()); o = o[o.v.notna()]
    sen = o.v.isin(SENTINELS)
    LOG.add(lake, fname, "missing-value code removed (-9999, -999, -99)", sen.sum()); o = o[~sen]
    if lake in LAKE_RANGE:
        lo, hi, why = LAKE_RANGE[lake]
        bad = (o.v < lo) | (o.v > hi)
        LOG.add(lake, fname, f"lake-specific range {lo}-{hi} C: {why}", bad.sum(),
                "; ".join(f"{r.t.date()} {r.z:g} m: {r.v:g}" for r in o[bad].head(12).itertuples()))
        o = o[~bad]
    low, high = o.v < TMIN, o.v > TMAX
    LOG.add(lake, fname, f"temperature below {TMIN} C removed (logger frozen in ice / not liquid water)", low.sum(),
            f"min {o.v[low].min():.2f} C" if low.any() else "")
    LOG.add(lake, fname, f"temperature above {TMAX} C removed", high.sum())
    o = o[~low & ~high]
    o = o.assign(z=o.z.round(3))
    key = ["t", "z"]
    dup = o.duplicated(key, keep=False)
    if dup.any():
        LOG.add(lake, fname, "several values at the same time and depth: averaged", dup.sum(),
                f"{o[dup].groupby(key).ngroups} groups")
        agg = {"v": "mean"} | ({"t_end": "max"} if "t_end" in o else {})
        o = o.groupby(key, as_index=False).agg(agg)
    return o, n0


def daily_from(o, fname, source):
    d = o.assign(day=o.t.dt.normalize()).groupby(["day", "z"]).v.agg(["mean", "count"]).reset_index()
    return d.rename(columns={"mean": "v", "count": "n"}).assign(source=source, file=fname)


def density(T):
    """Fresh water density (kg m-3), UNESCO/Chen & Millero (1977) at zero salinity."""
    return (999.842594 + 6.793952e-2 * T - 9.095290e-3 * T ** 2 + 1.001685e-4 * T ** 3
            - 1.120083e-6 * T ** 4 + 6.536332e-9 * T ** 5)


NO_STABILITY_CHECK = {"Kivu": "temperature rises with depth, stabilised by salinity (meromictic)"}
UNSTABLE_KGM3, TOP_EXCLUDED_M = 0.1, 1.0
OUTLIER_C, OUTLIER_MAD, OUTLIER_MIN_N = 5.0, 6.0, 10


def qc_flags(dd, lake):
    """Flags only (no value is removed): 'unstable' = lighter than water above it on the same day by more
    than 0.1 kg m-3, the reference being the water from 1 m down to the value (the top metre is excluded:
    night-time surface cooling); 'outlier' = more than 5 C and 6 robust SD (1.4826 MAD) from the lake's median
    for that calendar month and depth band (1 m bands to 20 m, 5 m below), groups with >= 10 values."""
    f = pd.Series("", index=dd.index)
    if lake not in NO_STABILITY_CHECK:
        x = dd[dd.z >= TOP_EXCLUDED_M].sort_values(["day", "z"])
        rho = density(x.v)
        above = rho.groupby(x.day).cummax().groupby(x.day).shift(1)
        bad = rho < above - UNSTABLE_KGM3
        f.loc[bad[bad].index] = "unstable"
    band = np.where(dd.z < 20, np.floor(dd.z), 20 + 5 * np.floor((dd.z - 20) / 5))
    g = dd.assign(m=dd.day.dt.month, b=band).groupby(["m", "b"]).v
    med, mad, n = g.transform("median"), g.transform(lambda s: (s - s.median()).abs().median()), g.transform("size")
    out = ((dd.v - med).abs() > np.maximum(OUTLIER_C, OUTLIER_MAD * 1.4826 * mad)) & (n >= OUTLIER_MIN_N)
    f[out] = np.where(f[out] == "", "outlier", f[out] + ";outlier")
    return f


def site_code(lake, frames):
    ids = [f["SITE_ID"].str.strip().replace("", np.nan).dropna() for f in frames if "SITE_ID" in f]
    ids = pd.concat(ids) if ids else pd.Series(dtype=str)
    return ids.mode().iloc[0] if len(ids) else ""


def hypsometry(f, lake):
    d, _ = read_table(f)
    h = pd.DataFrame({"z": pd.to_numeric(d["DEPTH"], errors="coerce"),
                      "a": pd.to_numeric(d["BATHYMETRY_AREA"], errors="coerce")})
    LOG.add(lake, f.name, "hypsometry row with missing depth or area removed", h.isna().any(axis=1).sum())
    h = h.dropna()
    if (h.z < 0).any():
        LOG.add(lake, f.name, "hypsometry depths negative; sign flipped", (h.z < 0).sum()); h = h.assign(z=h.z.abs())
    h = h.sort_values("z")
    if h.z.duplicated().any():
        LOG.add(lake, f.name, "hypsometry: repeated depth, kept the larger area", h.z.duplicated().sum())
        h = h.groupby("z", as_index=False).a.max()
    if len(h) > 2 and (h.a.diff().dropna() > 0).all():
        LOG.add(lake, f.name, "hypsometry depth axis inverted (area grew with depth at every level); "
                "re-expressed as depth below the surface", len(h),
                f"source surface area {h.a.iloc[0]:g} m2 at depth {h.z.iloc[0]:g}; after fix {h.a.iloc[-1]:g} m2 at 0 m")
        h = pd.DataFrame({"z": (h.z.max() - h.z).round(4), "a": h.a}).sort_values("z")
    return h, d


def protocol_sites(yml):
    return {s["specifier"]: s for s in yaml.safe_load(Path(yml).read_text())}


def ascii_key(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower())


def main(a):
    i3, i4, out = Path(a.isimip3), Path(a.isimip4), Path(a.out)
    sites = pd.read_csv(Path(__file__).resolve().parent / "lake_sites.csv")
    proto = protocol_sites(a.protocol)
    sheet = pd.read_csv(Path(a.sheet) / "metadata_hydrothermal.csv")
    sheet = sheet[sheet["Lake Short Name"].notna()].assign(key=lambda x: x["Lake Short Name"].map(ascii_key))
    corr = pd.read_csv(Path(a.sheet) / "metadata_hydrothermal_corrected.csv").assign(key=lambda x: x["Lake.Short.Name"].map(ascii_key))
    pubcol = "Data can go public (yes required for inclusion in ISIMIP4)"
    include = set(a.include.split(",")) if a.include else set()
    i3_commit = a.isimip3_commit
    meta_rows = []
    (out / "LocalLakes").mkdir(parents=True, exist_ok=True)
    for _, s in sites.iterrows():
        lake, site = s.lake, s.lake_site
        sh = sheet[sheet.key == ascii_key(lake)]
        if not len(sh):
            sh = sheet[sheet.key.str.startswith(ascii_key(lake)[:8])]
        sh = sh.iloc[0]
        public = str(sh[pubcol]).strip().lower() == "yes"
        if not public and lake not in include:
            print(f"{lake}: WITHHELD (sheet '{pubcol}' = {sh[pubcol]!r})")
            meta_rows.append({"lake_folder": lake, "lake_site": site, "included": False,
                              "note": f"withheld: data-sharing permission not given in the coordination sheet ({sh[pubcol]})"})
            continue
        folder = out / "LocalLakes" / lake
        folder.mkdir(parents=True, exist_ok=True)
        daily_parts, sub_parts, id_frames = [], [], []
        # ---- ISIMIP4 delivery (highest priority)
        d4 = i4 / lake
        if d4.exists() and lake not in ISIMIP4_RESTRICTED:
            for f in sorted(d4.glob("*watertemp*.csv")):
                d, note = read_table(f); id_frames.append(d)
                sub = "subdaily" in f.name
                o, n0 = clean_temp(d, lake, f.name, sub)
                SOURCES.append({"lake": lake, "source": "ISIMIP4 delivery", "file": f"{lake}/{f.name}", "sha256": sha256(f),
                                "rows": n0, "rows_used": len(o), "first": o.t.min().date(), "last": o.t.max().date()})
                if sub:
                    sub_parts.append(o.assign(prio=0))
                daily_parts.append(daily_from(o, f.name, "ISIMIP4 delivery" + (" (daily mean of sub-daily)" if sub else "")).assign(prio=0))
        # ---- ISIMIP3 public database
        moved_away = {f for fo, pat, to, _ in REASSIGN if fo == lake for f in (i3 / fo).glob(pat)}
        files3 = [(lake, f, "") for f in sorted((i3 / lake).glob("*.csv")) if f not in moved_away] if (i3 / lake).exists() else []
        files3 += [(fo, f, why) for fo, pat, to, why in REASSIGN if to == lake for f in sorted((i3 / fo).glob(pat))]
        for fo, why in {(fo, why) for fo, pat, to, why in REASSIGN if fo == lake}:
            LOG.add(lake, f"{fo}/(moved files)", "ISIMIP3 files of this folder moved to another lake: " + why, len(moved_away))
        for fo, f, why in files3:
            n = f.name.lower()
            if "temp" not in n:
                continue
            d, note = read_table(f)
            if d.empty:
                LOG.add(lake, f"{fo}/{f.name}", "empty source file (header only), skipped", 1)
                SOURCES.append({"lake": lake, "source": f"ISIMIP3 {i3_commit}", "file": f"{fo}/{f.name}", "sha256": sha256(f), "rows": 0, "rows_used": 0})
                continue
            if note:
                LOG.add(lake, f"{fo}/{f.name}", note, len(d))
            if fo != lake:
                LOG.add(lake, f"{fo}/{f.name}", f"file of ISIMIP3 folder '{fo}' assigned to {lake}: {why}", len(d))
            id_frames.append(d)
            sub = "subdaily" in n
            o, n0 = clean_temp(d, lake, f"{fo}/{f.name}", sub)
            SOURCES.append({"lake": lake, "source": f"ISIMIP3 {i3_commit}", "file": f"{fo}/{f.name}", "sha256": sha256(f),
                            "rows": n0, "rows_used": len(o), "first": o.t.min().date() if len(o) else None,
                            "last": o.t.max().date() if len(o) else None})
            if sub:
                sub_parts.append(o.assign(prio=2))
                daily_parts.append(daily_from(o, f.name, "ISIMIP3 sub-daily (daily mean)").assign(prio=2))
            else:
                daily_parts.append(daily_from(o, f.name, "ISIMIP3 daily").assign(prio=1))
        sid = site_code(lake, id_frames)
        name = lake
        # ---- daily: per day, the whole profile of the highest-priority source that has that day
        # (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean), so no profile mixes two instruments
        dd = pd.concat(daily_parts, ignore_index=True)
        best = dd.groupby("day").prio.transform("min")
        drop = dd.prio > best
        if drop.any():
            k = dd[drop].merge(dd[~drop][["day", "z", "v"]], on=["day", "z"], suffixes=("", "_kept"))
            diff = (k.v - k.v_kept).abs()
            LOG.add(lake, "(daily merge)", "day also in a higher-priority source: lower-priority values of that day not used "
                    "(ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean)", drop.sum(),
                    f"{dd[drop].day.nunique()} days; at common depths the sources differ by median {diff.median():.2f}, "
                    f"max {diff.max():.2f} C" if len(k) else f"{dd[drop].day.nunique()} days, no common depths")
        dd = dd[~drop].sort_values(["day", "z", "prio"])
        dup = dd.duplicated(["day", "z"], keep=False)
        if dup.any():          # same priority, several files with the same day and depth: average
            LOG.add(lake, "(daily merge)", "same day and depth in several files of the same source: averaged", dup.sum())
            dd = dd.groupby(["day", "z"], as_index=False).agg(v=("v", "mean"), n=("n", "sum"), source=("source", "first"),
                                                              file=("file", "first"), prio=("prio", "min"))
        dd = dd.reset_index(drop=True)
        dd["qc"] = qc_flags(dd, lake)
        for k in ("unstable", "outlier"):
            LOG.add(lake, "(daily, flag only)", f"QC flag '{k}' set (value kept)", dd.qc.str.contains(k).sum())
        daily = pd.DataFrame({"SITE_ID": sid, "SITE_NAME": name, "TIMESTAMP": dd.day.dt.strftime("%Y%m%d"),
                              "DEPTH": dd.z.map(lambda x: f"{x:g}"), "WATERTEMP": dd.v.round(4), "N": dd.n.astype(int),
                              "SOURCE": dd.source, "QC": dd.qc})
        daily.to_csv(folder / f"{site}_watertemp_daily.csv", index=False)
        # ---- sub-daily: cleaned records, one gzip file per year
        nsub_years = 0
        if sub_parts:
            ss = pd.concat(sub_parts, ignore_index=True).sort_values(["t", "z", "prio"]).drop_duplicates(["t", "z"], keep="first")
            for y, g in ss.groupby(ss.t.dt.year):
                te = g["t_end"] if "t_end" in g else pd.Series(pd.NaT, index=g.index)
                x = pd.DataFrame({"SITE_ID": sid, "SITE_NAME": name, "TIMESTAMP_START": g.t.dt.strftime("%Y%m%d%H%M"),
                                  "TIMESTAMP_END": te.dt.strftime("%Y%m%d%H%M").fillna(""), "DEPTH": g.z.map(lambda v: f"{v:g}"),
                                  "WATERTEMP": g.v.round(4)})
                with gzip.GzipFile(folder / f"{site}_watertemp_subdaily_{y}.csv.gz", "wb", mtime=0) as fh:
                    fh.write(x.to_csv(index=False).encode())
                nsub_years += 1
        # ---- hypsometry
        hfile = None
        if d4.exists() and lake not in ISIMIP4_RESTRICTED:
            hfile = next(iter(sorted(d4.glob("*hypsometry*.csv"))), None)
        hsrc = "ISIMIP4 delivery" if hfile else f"ISIMIP3 {i3_commit}"
        if hfile is None:
            hfile = next(iter(sorted(p for p in (i3 / lake).glob("*.csv") if re.search("hyps", p.name.lower()))), None)
        h, hd = hypsometry(hfile, lake)
        if hsrc.startswith("ISIMIP4"):
            h3f = next(iter(sorted(p for p in (i3 / lake).glob("*.csv") if re.search("hyps", p.name.lower()))), None) if (i3 / lake).exists() else None
            if h3f is not None:
                h3, _ = hypsometry(h3f, lake)
                same = len(h3) == len(h) and np.allclose(h3.values, h.values, rtol=1e-6)
                LOG.add(lake, hfile.name, "ISIMIP4 hypsometry used; ISIMIP3 file " + ("identical" if same else "differs"), 1,
                        "" if same else f"ISIMIP3 {len(h3)} levels to {h3.z.max():g} m, ISIMIP4 {len(h)} levels to {h.z.max():g} m")
        SOURCES.append({"lake": lake, "source": hsrc, "file": f"{hfile.parent.name}/{hfile.name}", "sha256": sha256(hfile),
                        "rows": len(hd), "rows_used": len(h)})
        pd.DataFrame({"SITE_ID": sid, "SITE_NAME": name, "DEPTH": h.z.map(lambda x: f"{x:g}"),
                      "BATHYMETRY_AREA": h.a.map(lambda x: f"{x:.10g}")}).to_csv(folder / f"{site}_hypsometry.csv", index=False)
        # ---- metadata
        p = proto[site]
        c = corr[corr.key == ascii_key(lake)]
        c = c.iloc[0] if len(c) else None
        num = lambda x: pd.to_numeric(str(x).replace(",", "."), errors="coerce")
        pick = lambda kc, ks: num(c[kc]) if c is not None and pd.notna(num(c[kc])) else num(sh[ks])
        lat, lon = p["lat"], p["lon"]
        coord_note = ""
        if lake == "Bosumtwi":
            lat, lon = 6.5, -1.41
            coord_note = "protocol lat 6.3, lon 1.25 (longitude sign wrong, ~300 km east of the lake); corrected to 6.5, -1.41"
        z = dd.z
        meta_rows.append({
            "lake_folder": lake, "lake_site": site, "included": True, "site_id": sid, "name": p["title"],
            "type": p.get("type", ""), "country": p.get("country", ""), "lat": lat, "lon": lon,
            "elevation_m": pick("elevation.m", "Elevation (m)"), "mean_depth_m": pick("mean.depth.m", "Mean depth (m)"),
            "max_depth_m": pick("max.depth.m", "Max depth (m)"), "area_km2": pick("lake.area.sqkm", "lake area (km²)"),
            "watershed_area_km2": num(sh["Watershed area (km²)"]), "trophic_state": sh["Trophic state"],
            "human_impacts": sh["Human impacts"], "secchi_m": pick("Average.Secchi.disk.depth.m", "Average Secchi disk depth [m]"),
            "light_extinction_m-1": pick("Light.extinction.coefficient.m", "Light extinction coefficient [m-1]"),
            "institute": sh["Institute"], "reference": sh["Reference (APA style)"],
            "temp_first": dd.day.min().date(), "temp_last": dd.day.max().date(), "temp_days": dd.day.nunique(),
            "temp_values_daily": len(dd), "temp_depths": z.nunique(), "temp_depth_min": z.min(), "temp_depth_max": z.max(),
            "subdaily_years": nsub_years, "hypsometry_levels": len(h), "hypsometry_depth_max": h.z.max(),
            "hypsometry_area_surface_m2": h.a.iloc[0], "hypsometry_source": hsrc,
            "temp_sources": "; ".join(sorted(set(dd.source))), "coord_note": coord_note,
            "data_sharing": "yes (coordination sheet)" if public else
                            "yes (confirmed by the ISIMIP lake sector coordination, 2026-10-23; not yet in the sheet)",
            "qc_unstable": int(dd.qc.str.contains("unstable").sum()), "qc_outlier": int(dd.qc.str.contains("outlier").sum()),
            "note": ""})
        print(f"{lake:20s} {site:20s} {dd.day.min().date()}..{dd.day.max().date()} days={dd.day.nunique():6d} "
              f"depths={z.nunique():4d} subdaily_years={nsub_years:3d} hyps={len(h):3d} ({hsrc})", flush=True)
    (out / "metadata").mkdir(exist_ok=True)
    pd.DataFrame(meta_rows).to_csv(out / "metadata" / "lakes.csv", index=False)
    pd.DataFrame(SOURCES).to_csv(out / "metadata" / "source_files.csv", index=False)
    pd.DataFrame(LOG.rows).to_csv(out / "metadata" / "corrections.csv", index=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k in ("isimip3", "isimip4", "sheet", "protocol", "out"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--isimip3-commit", default="1868644")
    ap.add_argument("--include", default="", help="lakes to include although the sheet has no 'yes' (after confirmation)")
    main(ap.parse_args())
