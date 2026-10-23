#!/usr/bin/env python3
"""Figures of the database.

    python3 scripts/plot_obsdata.py <repository root>

figures/overview_map.png       the lakes, coloured by the length of their temperature record
figures/data_coverage.png      days with temperature data per lake and year
figures/lakes/<site>.png       per lake: all daily values (time x depth), observation days per year by
                               source, near-surface and deepest values by day of year, hypsometry
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titlesize": 8.5, "axes.titleweight": "bold", "figure.dpi": 100})
SRC_COL = {"ISIMIP4 delivery": "#eb6834", "ISIMIP4 delivery (daily mean of sub-daily)": "#f4a27a",
           "ISIMIP3 daily": "#2a78d6", "ISIMIP3 sub-daily (daily mean)": "#9ec5f4"}


def lake_figure(root, m, out):
    f = root / "LocalLakes" / m.lake_folder
    d = pd.read_csv(f / f"{m.lake_site}_watertemp_daily.csv", dtype={"TIMESTAMP": str, "QC": str}, low_memory=False)
    d["t"] = pd.to_datetime(d.TIMESTAMP, format="%Y%m%d")
    d["QC"] = d.QC.fillna("")
    h = pd.read_csv(f / f"{m.lake_site}_hypsometry.csv")
    fig = plt.figure(figsize=(11, 7.6), constrained_layout=True)
    gs = fig.add_gridspec(2, 3, height_ratios=[1.15, 1])
    ax = fig.add_subplot(gs[0, :])
    vmin, vmax = np.percentile(d.WATERTEMP, [1, 99])
    big = len(d) > 200000
    q = d.sample(200000, random_state=1).sort_values("t") if big else d
    sc = ax.scatter(q.t, q.DEPTH, c=q.WATERTEMP, cmap="RdYlBu_r", vmin=vmin, vmax=vmax, s=3 if len(q) > 20000 else 8,
                    marker="s", lw=0, rasterized=True)
    fl = d[d.QC != ""]
    if len(fl):
        ax.scatter(fl.t, fl.DEPTH, s=14, facecolors="none", edgecolors="k", lw=0.5, label=f"QC flag ({len(fl)} values)")
        ax.legend(loc="lower left", fontsize=7, frameon=True)
    ax.set_ylim(max(d.DEPTH.max(), h.DEPTH.max()) * 1.03, 0)
    ax.axhline(h.DEPTH.max(), color="#8a8f98", lw=0.8, ls="--")
    ax.text(d.t.min(), h.DEPTH.max(), " deepest hypsometry level", va="bottom", fontsize=7, color="#5f6570")
    ax.set_ylabel("depth below surface (m)")
    ax.set_title(f"Daily water temperature: {len(d):,} values on {d.t.nunique():,} days, {m.temp_first} to {m.temp_last}"
                 + (" (200,000 shown)" if big else ""))
    fig.colorbar(sc, ax=ax, label="°C", pad=0.01)
    ax = fig.add_subplot(gs[1, 0])
    c = d.groupby([d.t.dt.year, "SOURCE"]).t.nunique().unstack(fill_value=0)
    bottom = np.zeros(len(c))
    for s in c.columns:
        ax.bar(c.index, c[s], bottom=bottom, color=SRC_COL.get(s, "#8a8f98"), width=0.9, label=s)
        bottom += c[s].values
    ax.set_title("Days with data per year, by source"); ax.set_ylabel("days"); ax.legend(fontsize=6.5, frameon=False)
    ax = fig.add_subplot(gs[1, 1])
    top = d[d.DEPTH <= d.DEPTH.min() + 1]
    deep = d[d.DEPTH >= d.DEPTH.max() - max(1.0, 0.1 * d.DEPTH.max())]
    for x, col, lab in ((top, "#eb6834", f"near surface ({top.DEPTH.min():g}-{top.DEPTH.max():g} m)"),
                        (deep, "#2a78d6", f"deepest ({deep.DEPTH.min():g}-{deep.DEPTH.max():g} m)")):
        ax.scatter(x.t.dt.dayofyear, x.WATERTEMP, s=3, alpha=0.4, color=col, label=lab, rasterized=True)
    ax.set_xticks([1, 91, 182, 274], ["Jan", "Apr", "Jul", "Oct"]); ax.set_ylabel("°C")
    ax.set_title("Seasonal cycle (all years)"); ax.legend(fontsize=6.5, markerscale=3, frameon=False)
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(h.BATHYMETRY_AREA / 1e6, h.DEPTH, "o-", color="#3b3f46", ms=2.5, lw=1)
    ax.set_ylim(h.DEPTH.max() * 1.03, min(0, h.DEPTH.min())); ax.set_xlim(left=0)
    ax.set_xlabel("area (km²)"); ax.set_ylabel("depth (m)")
    ax.set_title(f"Hypsometry: {len(h)} levels ({m.hypsometry_source})")
    title = f"{m['name']} ({m.lake_site}, {m.site_id}), {m.country}, {m.lat:.2f}°, {m.lon:.2f}°"
    fig.suptitle(title, fontsize=11, fontweight="bold")
    fig.savefig(out / f"{m.lake_site}.png"); plt.close(fig)


def overview(root, meta, out):
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    years = (pd.to_datetime(meta.temp_last) - pd.to_datetime(meta.temp_first)).dt.days / 365.25
    fig = plt.figure(figsize=(11, 5.6), constrained_layout=True)
    ax = fig.add_subplot(projection=ccrs.Robinson()); ax.set_global()
    ax.add_feature(cfeature.LAND, color="#eceef1"); ax.coastlines(lw=0.4, color="#8a8f98")
    s = ax.scatter(meta.lon, meta.lat, c=meta.temp_days, cmap="viridis", norm=matplotlib.colors.LogNorm(vmin=5, vmax=15000),
                   s=14 + 3 * np.sqrt(meta.max_depth_m.fillna(10)), edgecolors="k", lw=0.4, transform=ccrs.PlateCarree(), zorder=3)
    fig.colorbar(s, ax=ax, shrink=0.7, label="days with water-temperature data")
    ax.set_title(f"{len(meta)} ISIMIP4 local lakes (dot size grows with depth)")
    fig.savefig(out / "overview_map.png"); plt.close(fig)
    rows = []
    for _, m in meta.iterrows():
        d = pd.read_csv(root / "LocalLakes" / m.lake_folder / f"{m.lake_site}_watertemp_daily.csv", usecols=["TIMESTAMP"], dtype=str)
        y = pd.to_datetime(d.TIMESTAMP.drop_duplicates(), format="%Y%m%d").dt.year.value_counts()
        rows.append(y.rename(m.lake_folder))
    c = pd.concat(rows, axis=1).fillna(0).T
    c = c.loc[meta.sort_values("temp_first").lake_folder].reindex(columns=range(int(c.columns.min()), int(c.columns.max()) + 1),
                                                                  fill_value=0)   # every year, so the axis is linear
    fig, ax = plt.subplots(figsize=(11, 0.16 * len(c) + 1.2), constrained_layout=True)
    im = ax.imshow(np.where(c.values > 0, c.values, np.nan), aspect="auto", cmap="viridis",
                   norm=matplotlib.colors.LogNorm(vmin=1, vmax=366), interpolation="none",
                   extent=[c.columns.min() - 0.5, c.columns.max() + 0.5, len(c) - 0.5, -0.5])
    ax.set_yticks(range(len(c)), c.index, fontsize=6.5); ax.set_xlabel("year")
    ax.set_title("Days with water-temperature data per year")
    fig.colorbar(im, ax=ax, label="days", pad=0.01)
    fig.savefig(out / "data_coverage.png"); plt.close(fig)


def main(root):
    root = Path(root)
    meta = pd.read_csv(root / "metadata" / "lakes.csv")
    meta = meta[meta.included == True].copy()  # noqa: E712
    out = root / "figures"; (out / "lakes").mkdir(parents=True, exist_ok=True)
    overview(root, meta, out)
    for _, m in meta.iterrows():
        lake_figure(root, m, out / "lakes")
        print(m.lake_folder, flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
