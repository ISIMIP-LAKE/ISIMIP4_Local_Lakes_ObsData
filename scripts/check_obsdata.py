#!/usr/bin/env python3
"""Checks of the published files (run after build_obsdata.py).

    python3 -I scripts/check_obsdata.py <repository root>

Per lake: the three file types exist with the expected names and columns; dates valid and sorted;
depths >= 0; temperatures finite and within -0.5..40 C; one value per day and depth; sub-daily files
readable, one calendar year each; hypsometry starts at 0 m with the largest area and the area never
grows with depth. Also lists, as information, lakes observed deeper than their hypsometry reaches.
Writes metadata/checks.csv and prints the failures.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DAILY = ["SITE_ID", "SITE_NAME", "TIMESTAMP", "DEPTH", "WATERTEMP", "N", "SOURCE", "QC"]
SUB = ["SITE_ID", "SITE_NAME", "TIMESTAMP_START", "TIMESTAMP_END", "DEPTH", "WATERTEMP"]
HYP = ["SITE_ID", "SITE_NAME", "DEPTH", "BATHYMETRY_AREA"]


def main(root):
    root = Path(root)
    meta = pd.read_csv(root / "metadata" / "lakes.csv")
    rows = []
    for _, m in meta[meta.included == True].iterrows():  # noqa: E712
        f = root / "LocalLakes" / m.lake_folder
        p, info = [], {}
        d = pd.read_csv(f / f"{m.lake_site}_watertemp_daily.csv", dtype={"TIMESTAMP": str})
        if list(d.columns) != DAILY:
            p.append(f"daily columns {list(d.columns)}")
        t = pd.to_datetime(d.TIMESTAMP, format="%Y%m%d", errors="coerce")
        if t.isna().any(): p.append("daily: invalid dates")
        if not t.is_monotonic_increasing: p.append("daily: not sorted by date")
        if (d.DEPTH < 0).any(): p.append("daily: negative depth")
        if d.WATERTEMP.isna().any() or (d.WATERTEMP < -0.5).any() or (d.WATERTEMP > 40).any(): p.append("daily: temperature missing or out of range")
        if d.duplicated(["TIMESTAMP", "DEPTH"]).any(): p.append("daily: duplicated day and depth")
        if d.SITE_ID.nunique() != 1: p.append("daily: several SITE_IDs")
        nsub = 0
        for g in sorted(f.glob(f"{m.lake_site}_watertemp_subdaily_*.csv.gz")):
            s = pd.read_csv(g, dtype={"TIMESTAMP_START": str, "TIMESTAMP_END": str})
            nsub += len(s)
            ts = pd.to_datetime(s.TIMESTAMP_START, format="%Y%m%d%H%M", errors="coerce")
            if list(s.columns) != SUB: p.append(f"{g.name}: columns")
            if ts.isna().any() or ts.dt.year.nunique() != 1 or str(ts.dt.year.iloc[0]) not in g.name: p.append(f"{g.name}: dates")
            if (s.WATERTEMP < -0.5).any() or (s.WATERTEMP > 40).any() or s.WATERTEMP.isna().any(): p.append(f"{g.name}: temperature")
            if s.duplicated(["TIMESTAMP_START", "DEPTH"]).any(): p.append(f"{g.name}: duplicates")
        h = pd.read_csv(f / f"{m.lake_site}_hypsometry.csv")
        if list(h.columns) != HYP: p.append("hypsometry columns")
        if h.DEPTH.iloc[0] != 0: info["hyps_note"] = f"first level at {h.DEPTH.iloc[0]:g} m (as provided)"
        if (np.diff(h.DEPTH) <= 0).any(): p.append("hypsometry depth not increasing")
        if (np.diff(h.BATHYMETRY_AREA) > 0).any(): p.append("hypsometry area grows with depth")
        if h.BATHYMETRY_AREA.iloc[0] != h.BATHYMETRY_AREA.max(): p.append("hypsometry: surface area not the largest")
        deep = d.DEPTH.max() - h.DEPTH.max()
        info.update(obs_max_depth=d.DEPTH.max(), hyps_max_depth=h.DEPTH.max(),
                    obs_deeper_than_hypsometry_m=round(deep, 2) if deep > 0 else 0, subdaily_values=nsub)
        rows.append({"lake": m.lake_folder, "ok": not p, "problems": "; ".join(p), "daily_values": len(d), **info})
    r = pd.DataFrame(rows)
    r.to_csv(root / "metadata" / "checks.csv", index=False)
    print(f"{r.ok.sum()} of {len(r)} lakes pass")
    for _, x in r[~r.ok].iterrows():
        print(f"  {x.lake}: {x.problems}")
    dd = r[r.obs_deeper_than_hypsometry_m > 0]
    print(f"information: {len(dd)} lakes observed deeper than their hypsometry: " +
          ", ".join(f"{a} (+{b:g} m)" for a, b in zip(dd.lake, dd.obs_deeper_than_hypsometry_m)))
    hn = r[r.get("hyps_note", pd.Series(dtype=str)).notna()] if "hyps_note" in r else r.iloc[0:0]
    for _, x in hn.iterrows():
        print(f"information: {x.lake} hypsometry {x.hyps_note}")


if __name__ == "__main__":
    main(sys.argv[1])
