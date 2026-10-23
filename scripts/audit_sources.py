#!/usr/bin/env python3
"""Audit of the source files (ISIMIP3 public repository and ISIMIP4 delivery) before harmonisation.

    python3 -I scripts/audit_sources.py <ISIMIP3 LocalLakes dir> <ISIMIP4 LocalLakes dir> <out dir>

Reads every temperature and hypsometry file as text (no cleaning) and reports per file: header,
rows, timestamp formats, unparseable dates, missing-value codes, depth sign/range, temperature
range, values equal to the depth, duplicated (time, depth) rows; for lakes with both daily and
sub-daily files, how the daily file compares with the daily mean of the sub-daily files.
Writes <out>/audit_files.csv and <out>/audit_daily_vs_subdaily.csv.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SENTINELS = [-9999, -999, -99, 9999, 999]


def norm_cols(cols):
    return [re.sub(r"[^A-Z0-9]+", "_", str(c).strip().upper()).strip("_") for c in cols]


def ts_kind(s):
    s = s.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    kinds = np.select([s.str.fullmatch(r"\d{8}"), s.str.fullmatch(r"\d{12}"), s.str.fullmatch(r"\d{6}"),
                       s.str.fullmatch(r"\d{4}-\d{2}-\d{2}.*"), s.str.upper().isin(["NA", "NAN", ""])],
                      ["yyyymmdd", "yyyymmddHHMM", "6digits", "iso", "missing"], "other")
    return pd.Series(kinds).value_counts().to_dict()


def parse_time(s):
    s = s.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    out = pd.to_datetime(s.where(s.str.fullmatch(r"\d{8}")), format="%Y%m%d", errors="coerce")
    out = out.fillna(pd.to_datetime(s.where(s.str.fullmatch(r"\d{12}")), format="%Y%m%d%H%M", errors="coerce"))
    iso = s.where(s.str.fullmatch(r"\d{4}-\d{2}-\d{2}.*"))
    out = out.fillna(pd.to_datetime(iso, errors="coerce", format="mixed"))
    return out


def audit_temp(f, lake, source):
    d = pd.read_csv(f, dtype=str, keep_default_na=False)
    raw_cols = list(d.columns)
    d.columns = norm_cols(d.columns)
    tcol = "TIMESTAMP" if "TIMESTAMP" in d else ("TIMESTAMP_START" if "TIMESTAMP_START" in d else d.columns[2])
    vcol = next((c for c in d.columns if c in ("WTEMP", "WATERTEMP", "TEMP", "WATER_TEMP")), d.columns[-1])
    t = parse_time(d[tcol])
    z = pd.to_numeric(d.get("DEPTH", pd.Series(dtype=str)), errors="coerce")
    v = pd.to_numeric(d[vcol].replace({"NA": "", "NaN": "", "nan": ""}), errors="coerce")
    sent = v.isin(SENTINELS)
    vv = v.where(~sent)
    r = {"lake": lake, "source": source, "file": f.name, "rows": len(d), "columns": "|".join(raw_cols),
         "time_col": tcol, "value_col": vcol, "ts_kinds": ts_kind(d[tcol]), "time_unparsed": int(t.isna().sum()),
         "first": t.min(), "last": t.max(), "value_missing": int(v.isna().sum()), "value_sentinel": int(sent.sum()),
         "value_min": vv.min(), "value_max": vv.max(), "value_lt_m1": int((vv < -1).sum()), "value_gt_40": int((vv > 40).sum()),
         "value_eq_depth": int((((vv - z).abs() < 0.06) & (z >= 1)).sum()),
         "depth_missing": int(z.isna().sum()), "depth_negative": int((z < 0).sum()), "depth_min": z.min(), "depth_max": z.max(),
         "depths_n": int(z.nunique()), "site_ids": "|".join(sorted(set(d.iloc[:, 0])) [:5])}
    key = pd.DataFrame({"t": t, "z": z.abs().round(2)})
    r["dup_time_depth"] = int(key.duplicated().sum())
    return r, pd.DataFrame({"t": t, "z": z.abs(), "v": vv})


def audit_hypso(f, lake, source):
    d = pd.read_csv(f, dtype=str, keep_default_na=False)
    raw = list(d.columns); d.columns = norm_cols(d.columns)
    z = pd.to_numeric(d.get("DEPTH"), errors="coerce"); a = pd.to_numeric(d.get("BATHYMETRY_AREA"), errors="coerce")
    o = pd.DataFrame({"z": z.abs(), "a": a}).dropna().sort_values("z")
    return {"lake": lake, "source": source, "file": f.name, "rows": len(d), "columns": "|".join(raw),
            "depth_negative": int((z < 0).sum()), "depth_min": z.min(), "depth_max": z.max(),
            "area_top": o.a.iloc[0] if len(o) else np.nan, "area_bottom": o.a.iloc[-1] if len(o) else np.nan,
            "area_increases_with_depth": int((o.a.diff() > 0).sum()), "dup_depth": int(o.z.duplicated().sum()),
            "missing": int(z.isna().sum() + a.isna().sum()), "site_ids": "|".join(sorted(set(d.iloc[:, 0]))[:3])}


def main(i3, i4, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    rows, hyp, cmp = [], [], []
    for src, root in (("ISIMIP3", Path(i3)), ("ISIMIP4", Path(i4))):
        for lake_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            daily, sub = [], []
            for f in sorted(lake_dir.glob("*.csv")):
                n = f.name.lower()
                if re.search(r"hyps", n):
                    hyp.append(audit_hypso(f, lake_dir.name, src)); continue
                if not re.search(r"temp", n):
                    continue
                r, data = audit_temp(f, lake_dir.name, src)
                r["kind"] = "subdaily" if "subdaily" in n or r["time_col"] == "TIMESTAMP_START" else ("monthly" if "monthly" in n else "daily")
                rows.append(r)
                (sub if r["kind"] == "subdaily" else daily).append(data)
            if daily and sub:
                dd = pd.concat(daily).dropna(); ss = pd.concat(sub).dropna()
                ss = ss.assign(t=ss.t.dt.normalize()).groupby(["t", "z"]).v.mean().rename("sub")
                j = dd.assign(z=dd.z.round(2)).groupby(["t", "z"]).v.mean().rename("daily").to_frame().join(
                    ss.reset_index().assign(z=lambda x: x.z.round(2)).set_index(["t", "z"]), how="inner")
                cmp.append({"lake": lake_dir.name, "source": src, "overlap_values": len(j),
                            "max_abs_diff": float((j.daily - j["sub"]).abs().max()) if len(j) else np.nan,
                            "mean_abs_diff": float((j.daily - j["sub"]).abs().mean()) if len(j) else np.nan,
                            "daily_days": dd.t.nunique(), "subdaily_days": ss.index.get_level_values(0).nunique()})
    pd.DataFrame(rows).to_csv(out / "audit_files.csv", index=False)
    pd.DataFrame(hyp).to_csv(out / "audit_hypsometry.csv", index=False)
    pd.DataFrame(cmp).to_csv(out / "audit_daily_vs_subdaily.csv", index=False)
    print(f"{len(rows)} temperature files, {len(hyp)} hypsometry files, {len(cmp)} lakes with daily+subdaily")


if __name__ == "__main__":
    main(*sys.argv[1:4])
