# What was corrected, and how

The published files are built by `scripts/build_obsdata.py` from the original contributions, without
editing any file by hand. Every value that is removed, moved or changed is counted in
`metadata/corrections.csv` (per source file and rule); [CORRECTIONS_BY_LAKE.md](CORRECTIONS_BY_LAKE.md)
lists them per lake. **No value is interpolated, gap-filled or adjusted.** The only numbers that change are
averages where one time and depth had several values, and depths whose sign was reversed.

Sources: the ISIMIP3 database ([icra/ISIMIP_Local_Lakes](https://github.com/icra/ISIMIP_Local_Lakes),
commit `1868644`, 5 January 2023) and the ISIMIP4 delivery collected by the ISIMIP lake sector in 2026
(`metadata/source_files.csv` lists every file used, with its SHA-256 checksum).

## 1. Errors in the ISIMIP3 database that are fixed here

| Problem in ISIMIP3 | Lakes | Fix |
|---|---|---|
| File names did not follow one pattern (`taihu_…`, `washington_temp_daily.csv`, `FishLake_hypsometry.csv`, `LowerZurich_…` in folder `LowerLakeZurich`, `Murten_Temp.csv`, `Bryrup_wtemp_daily.csv`, `…_hypsography.csv`, `…_hypsograph.csv`) | 10 | one pattern: `<site>_watertemp_daily.csv`, `<site>_watertemp_subdaily_<yyyy>.csv.gz`, `<site>_hypsometry.csv`, `<site>` = ISIMIP4 protocol lake-site identifier |
| Column names differed (`SITE-ID`, `SITE-NAME`, `BATHYMETRY-AREA` in 7 hypsometry files; `WTEMP` in ISIMIP3 vs `WATERTEMP` in ISIMIP4; an extra `ELEVATION_M` column in Zlutice) | 9 | one set of columns per file type (README); Zlutice's water-level column is not carried over (see ISSUES.md) |
| 19 lakes had sub-daily files only, no daily file | 19 | daily file built from the sub-daily data (daily mean per depth) |
| Folder `Zurich`: header without the `DEPTH` column (4 names, 5 data columns), so every column was shifted; the data are the Lower Lake Zurich record 1981-2022 (the same rows as the ISIMIP4 Lower Lake Zurich file) | Lower Lake Zurich | columns re-assigned; assigned to Lower Lake Zurich; folder `Zurich` dropped (no separate lake) |
| Sub-daily files of the Rappbode **pre-dam** contain profiles to 48-79 m (the pre-dam is ~17 m deep); the 44 days of 2015 also in the Rappbode **reservoir** file are identical to it | Rappbode, Rappbode pre-dam | moved to the Rappbode reservoir (adds 39 days in 2016-2017) |
| Trout Lake hypsometry: 160,790,000 m² at the surface, ten times the lake (NTL-LTER 1,607.9 ha = 16,079,000 m²; sheet 15.65 km²); depths and shape agree with the lake (mean depth 15.1 m vs 14.6 m) | Trout Lake | all areas divided by 10 |
| Taihu hypsometry upside down: area 0 at depth 0, largest area at 13.31 m | Taihu | re-expressed as depth below the surface |
| Tarawera: 162 dates written with six digits (`160101`, `160102`) | Tarawera | read as 2016-01-01 and 2016-01-02 (inside the record, which otherwise resumes on 2016-01-21) |
| Bosumtwi: 67 rows without a date; 13 values where the depth was typed in the temperature column (17.035 °C at 17 m, 36.682 °C at 36 m, 68.828 °C at 68 m, ...) | Bosumtwi | removed (the lake is 26-33 °C at every depth) |
| 11 sub-daily files contain only a header (Erken 1990 and 1993-1997, Mt Bold 2009-2012, Trout Bog 2013) | 3 | skipped |
| Missing values written as `NaN`, `NA`, empty fields or `-9999` | 7 | removed (the files contain only measured values) |
| Loggers frozen into the ice: temperatures down to −22 °C | 14 | values below −0.5 °C removed (20,924 values; 99 % in seven lakes with under-ice loggers) |
| Several rows for the same time and depth | 17 | averaged (`N` in the daily files counts the values behind each daily value) |
| Coordinates of Bosumtwi in the protocol: 6.3, **+1.25** (east of Accra, ~300 km off) | Bosumtwi | 6.50, −1.41 in `metadata/lakes.csv` |

## 2. Rules applied to every file

1. **Dates**: `yyyymmdd`, `yyyymmddHHMM` and ISO dates are read; six-digit dates only when they fall inside
   the record (Tarawera). Rows without a readable date are removed.
2. **Depth**: metres below the water surface, positive downwards. A file with only negative depths
   (ISIMIP4 Erken, height above the surface) is converted; a single negative depth in a file of positive depths
   is removed (Sammamish, 1 row). Rows without depth are removed.
3. **Missing values**: empty, `NA`, `NaN`, `-9999`, `-999`, `-99` are removed.
4. **Physical range**: −0.5 to 40 °C (fresh water cannot be colder than about −0.1 °C; −0.5 allows for
   sensor accuracy). Bosumtwi additionally 24-33 °C (depth-as-temperature entries).
5. **Duplicates**: values with the same time and depth are averaged.
6. **Daily values from sub-daily records**: the mean of all values of the calendar day at each depth,
   whatever their number (`N`). The day is the one of `TIMESTAMP_START`, in the time of the source file.
7. **One source per day**: when a lake has several sources, each day takes the whole profile of the
   highest-priority source that has that day: **ISIMIP4 delivery > ISIMIP3 daily file > daily mean of
   ISIMIP3 sub-daily files**. A daily profile therefore never mixes two instruments (where manual profiles and
   buoy loggers measured the same day and depth they differ by a median of 0.2-0.5 °C in five lakes). The `SOURCE` column says which source each value
   comes from; the number of values not used per lake is in `metadata/corrections.csv`.
8. **Hypsometry**: sorted by depth; repeated depths keep the larger area; an axis on which the area grows
   with depth at every level is flipped (Taihu). When the ISIMIP4 delivery has a hypsometry it is used (it
   equals the ISIMIP3 file for Erken, Lower Lake Zurich, Sammamish, Vendyurskoe and Washington, and differs
   only by rounding for Feeagh).

## 3. Quality flags (values kept)

The `QC` column of the daily files marks values that look wrong but are not removed, because the same
pattern can also be real. Most lakes have none or a few; check them before using a value.

| Flag | Meaning | Values |
|---|---|---|
| `unstable` | lighter than the water above it on the same day by more than 0.1 kg m⁻³ (fresh-water density, Chen & Millero 1977); the top metre is not used as a reference (night-time surface cooling). Not applied to Lake Kivu, where salt keeps warmer deep water stable. Such an inversion cannot last a day: a sensor out of position (e.g. Trout Lake buoy, 11 August 2011: 22 °C at 18-30 m while the manual profile reads 6.6-6.9 °C), a faulty sensor (Lake Annie, 6 m) or, in Falling Creek and Sammamish, several casts per day at slightly different depths | 28,232 (1.3 %) |
| `outlier` | more than 5 °C and more than 6 robust standard deviations (1.4826 × median absolute deviation) from the lake's median for that calendar month and depth band (1 m bands to 20 m, 5 m below; bands with at least 10 values) | 1,731 (0.08 %) |

Both rules use the daily values only; the sub-daily files carry no flag.

## 4. What is not corrected

Observations deeper than the deepest hypsometry level, hypsometries that do not start at 0 m, metadata
that disagree with the data, and the time zones of the sub-daily records need information from the data
providers: see [ISSUES.md](ISSUES.md).
