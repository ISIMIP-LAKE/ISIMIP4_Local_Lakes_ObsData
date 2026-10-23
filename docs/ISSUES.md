# Open issues (not corrected; information from the data providers needed)

Found while building this database (`scripts/check_obsdata.py`, `metadata/checks.csv`, comparison of
`metadata/lakes.csv` with the files). The data are published as received for these points; please
take them into account, and tell the ISIMIP lake sector coordination if you can resolve one.

## Hypsometry does not match the lake

| Lake | Hypsometry | Coordination sheet | Likely explanation |
|---|---|---|---|
| Trout Lake | surface area **160.8 km²**, deepest level 33 m | 15.65 km², 35.7 m | areas about **10 times too large** (decimal shift) |
| Windermere | 6.7 km², 42 m | 14.8 km², 64 m | hypsometry of the **South Basin**; the sheet gives the whole lake (North Basin 64 m) |
| Allequash Lake | 0.58 km², 7 m | 1.64 km², 8 m | hypsometry of one basin only? |
| Langtjern | 0.06 km², 9 m | 0.23 km², 12 m | hypsometry of part of the lake? |
| Taihu | 2,330 km², **13.3 m** (after flipping the inverted axis) | 2,445 km², 4.8 m (mean 2.1 m) | depth axis wrong (13.3 m is far deeper than the lake); observations at the surface only |
| Mt Bold | starts at 0.92 m (3.22 km²) | | depths below the full-supply level? |
| Hulun | starts at 0.02 m | | minor |

## Coordination-sheet metadata that disagree with the data

| Lake | Sheet | Data / literature |
|---|---|---|
| Falling Creek Reservoir | area 119 km² | hypsometry 0.12 km² (the reservoir is ~0.12 km²): sheet value 1000 times too large |
| Lake Rotorua | area 425 km² | hypsometry 79.3 km² (the lake is ~80 km²) |
| Lake Stechlin | area 2.23 km² | hypsometry 4.23 km² (the lake is ~4.3 km²) |
| Ekoln, Alqueva, Kilpisjärvi, Kuivajärvi, Wingra | maximum depth 28-68 % greater than the deepest hypsometry level | hypsometry or sheet to be checked |
| Lake Bosumtwi | protocol coordinates 6.3, +1.25 | the lake is at 6.50, −1.41 (`metadata/lakes.csv` has the correct values) |

## Observations deeper than the hypsometry

Sau (+5.5 m below the deepest hypsometry level), Kuivajärvi (+2.0), Trout (+2.0), Hassel (+1.9),
Fish (+1.8), Falling Creek (+1.7), Monona (+1.7), Allequash (+1.0), Sparkling (+1.0), Bryrup (+1.0),
Laramie (+0.6), Delavan (+0.5), Crystal Bog (+0.5), Mendota (+0.2). In reservoirs (Sau) the level varies;
in the others the hypsometry may not reach the deepest point.

## Data values

- **Bosumtwi** (ISIMIP3 file): 13 values where the depth was entered as the temperature and 67 rows without a
  date were removed. If the provider has the correct values, they can be added.
- **Chao**: 8 days with `NaN` at the surface were removed.
- **Trout Lake buoy, 11 August 2011** and similar days: sensors out of position; flagged `unstable`, not removed.
- **Lake Annie**: single days with one sensor out of line (e.g. 6 m); flagged.
- **Falling Creek, Sammamish**: several profiles per day at slightly different depths; the daily mean per exact
  depth mixes casts, so these lakes have the most `unstable` flags (7 % and 6 %).
- **Zlutice**: the ISIMIP3 files carry the water-level elevation (`ELEVATION_M`) in every row; it is not part of
  this format and was not carried over.

## Time and naming

- **Time zone** of the sub-daily records is not documented (local time or UTC); daily means use the calendar
  day of `TIMESTAMP_START` as given.
- **SITE_ID** differs between the two rounds for some lakes (Erken `SE-Erk` / `SE-Erken`, Arendsee
  `DE-Arendsee` / `DE-Are`, Bosumtwi `GH-Bosumtwi` / `GH-Bos`); the code most used in the source files is kept.
- **Villasjön** is spelled "Vallasjön" in one delivery e-mail; the data files and this database use Villasjön.

## Data not included

- **Bosumtwi** ISIMIP4 delivery (monthly temperature and hypsometry): marked as restricted to ISIMIP3 lake
  sector modellers; only the public ISIMIP3 data of Bosumtwi are included.
- **Arendsee, Scharmützelsee**: the ISIMIP4 delivery has oxygen files only (no new temperature); their ISIMIP3
  temperature data are included.
