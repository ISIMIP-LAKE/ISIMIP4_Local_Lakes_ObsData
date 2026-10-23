#!/usr/bin/env python3
"""Tables for the documentation, generated from metadata/ (run after build_obsdata.py and check_obsdata.py).

    python3 scripts/make_docs.py <repository root>

docs/LAKES.md        one row per lake: identifiers, location, depth, record, sources, figure link
docs/CORRECTIONS_BY_LAKE.md   every correction applied, per lake, with counts (from metadata/corrections.csv)
"""
import sys
from pathlib import Path

import pandas as pd


def fmt(x, nd=1):
    return "" if pd.isna(x) else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def main(root):
    root = Path(root)
    m = pd.read_csv(root / "metadata" / "lakes.csv")
    chk = pd.read_csv(root / "metadata" / "checks.csv").set_index("lake")
    inc = m[m.included == True].sort_values("lake_folder")  # noqa: E712
    L = ["# Lakes", "", f"{len(inc)} lakes. Folder `LocalLakes/<Folder>/`, files `<site>_...`. Depth: maximum depth "
         "from the coordination sheet; record: first and last day with water temperature; days: days with at least one "
         "value. Sources: `I3` = ISIMIP3 database (daily file `d`, sub-daily files `s`), `I4` = ISIMIP4 delivery.", "",
         "| Folder | Site (protocol) | SITE_ID | Name | Country | Type | Lat | Lon | Max depth (m) | Record | Days | Depths | Sub-daily years | Hypsometry levels | Temperature sources | Figure |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    abbrev = {"ISIMIP3 daily": "I3 d", "ISIMIP3 sub-daily (daily mean)": "I3 s", "ISIMIP4 delivery": "I4",
              "ISIMIP4 delivery (daily mean of sub-daily)": "I4 s"}
    for _, r in inc.iterrows():
        src = ", ".join(abbrev.get(s.strip(), s.strip()) for s in str(r.temp_sources).split(";"))
        L.append(f"| {r.lake_folder} | `{r.lake_site}` | {r.site_id} | {r['name']} | {r.country} | {r.type} | {r.lat:.2f} | "
                 f"{r.lon:.2f} | {fmt(r.max_depth_m)} | {r.temp_first} – {r.temp_last} | {int(r.temp_days):,} | "
                 f"{int(r.temp_depths):,} | {int(r.subdaily_years)} | {int(r.hypsometry_levels)} | {src} | "
                 f"[png](../figures/lakes/{r.lake_site}.png) |")
    out = m[m.included != True]  # noqa: E712
    if len(out):
        L += ["", "Not included:", ""] + [f"- {r.lake_folder} (`{r.lake_site}`): {r.note}" for _, r in out.iterrows()]
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "LAKES.md").write_text("\n".join(L) + "\n")

    P = ["# Data providers", "", "Institutes and references as given in the ISIMIP4 local-lakes coordination sheet "
         "(contact e-mail addresses are not published here; ask the ISIMIP lake sector coordination). Please cite the "
         "references when you use a lake's data.", "", "| Lake | Institute | Reference |", "|---|---|---|"]
    for _, r in inc.iterrows():
        P.append(f"| {r['name']} | {fmt(r.institute).replace('|', '/')} | {fmt(r.reference).replace('|', '/')} |")
    (root / "docs" / "PROVIDERS.md").write_text("\n".join(P) + "\n")

    c = pd.read_csv(root / "metadata" / "corrections.csv")
    C = ["# Corrections by lake", "", "Generated from `metadata/corrections.csv` (one row per source file and rule). "
         "Rules: see [CORRECTIONS.md](CORRECTIONS.md). `n` = number of values (rows) concerned.", ""]
    for lake in sorted(c.lake.unique()):
        x = c[c.lake == lake]
        C += [f"## {lake}", "", "| File | Rule | n | Detail |", "|---|---|---|---|"]
        for _, r in x.iterrows():
            C.append(f"| {r.file} | {r.rule} | {int(r.n_values):,} | {fmt(r.detail).replace('|', '/')} |")
        if lake in chk.index and chk.loc[lake, "obs_deeper_than_hypsometry_m"] > 0:
            C.append(f"| (check) | observations reach {chk.loc[lake, 'obs_max_depth']:g} m, hypsometry {chk.loc[lake, 'hyps_max_depth']:g} m | | not corrected; see ISSUES.md |")
        C.append("")
    (root / "docs" / "CORRECTIONS_BY_LAKE.md").write_text("\n".join(C) + "\n")
    print("docs/LAKES.md, docs/PROVIDERS.md, docs/CORRECTIONS_BY_LAKE.md written")


if __name__ == "__main__":
    main(sys.argv[1])
