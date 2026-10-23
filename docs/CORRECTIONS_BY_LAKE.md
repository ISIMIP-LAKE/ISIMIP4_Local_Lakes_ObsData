# Corrections by lake

Generated from `metadata/corrections.csv` (one row per source file and rule). Rules: see [CORRECTIONS.md](CORRECTIONS.md). `n` = number of values (rows) concerned.

## Allequash

| File | Rule | n | Detail |
|---|---|---|---|
| Allequash/Allequash_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1 | min -1.00 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 2 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 1 |  |
| (check) | observations reach 8 m, hypsometry 7 m | | not corrected; see ISSUES.md |

## Alqueva

| File | Rule | n | Detail |
|---|---|---|---|
| Alqueva/Alqueva_temp_subdaily_2017.csv | missing-value code removed (-9999, -999, -99) | 1,250 |  |
| Alqueva/Alqueva_temp_subdaily_2018.csv | missing-value code removed (-9999, -999, -99) | 6,656 |  |
| Alqueva/Alqueva_temp_subdaily_2019.csv | missing-value code removed (-9999, -999, -99) | 1,651 |  |
| Alqueva/Alqueva_temp_subdaily_2020.csv | missing-value code removed (-9999, -999, -99) | 13,115 |  |
| Alqueva/Alqueva_temp_subdaily_2021.csv | missing-value code removed (-9999, -999, -99) | 369 |  |
| Alqueva/Alqueva_temp_subdaily_2022.csv | missing-value code removed (-9999, -999, -99) | 4,719 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 9 |  |

## Annie

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | same day and depth in several files of the same source: averaged | 266 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 1,574 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 59 |  |

## Arendsee

| File | Rule | n | Detail |
|---|---|---|---|
| Arendsee/Arendsee_wtemp_subdaily_2014.csv | missing temperature removed (empty, NA, NaN) | 1,072 |  |
| Arendsee/Arendsee_wtemp_subdaily_2016.csv | missing temperature removed (empty, NA, NaN) | 1,564 |  |
| Arendsee/Arendsee_wtemp_subdaily_2017.csv | missing temperature removed (empty, NA, NaN) | 20,230 |  |
| Arendsee/Arendsee_wtemp_subdaily_2018.csv | missing temperature removed (empty, NA, NaN) | 16,557 |  |
| Arendsee/Arendsee_wtemp_subdaily_2019.csv | missing temperature removed (empty, NA, NaN) | 21,124 |  |
| Arendsee/Arendsee_wtemp_subdaily_2020.csv | missing temperature removed (empty, NA, NaN) | 4,412 |  |
| Arendsee/Arendsee_wtemp_subdaily_2021.csv | missing temperature removed (empty, NA, NaN) | 7,430 |  |
| Arendsee/Arendsee_wtemp_subdaily_2022.csv | missing temperature removed (empty, NA, NaN) | 3,794 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 1 |  |

## Argyle

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 19 |  |

## BigMuskellunge

| File | Rule | n | Detail |
|---|---|---|---|
| BigMuskellunge/BigMuskellunge_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 2 | min -1.00 C |

## Bosumtwi

| File | Rule | n | Detail |
|---|---|---|---|
| Bosumtwi/Bosumtwi_temp_daily.csv | missing or unreadable date removed | 67 |  |
| Bosumtwi/Bosumtwi_temp_daily.csv | missing temperature removed (empty, NA, NaN) | 2 |  |
| Bosumtwi/Bosumtwi_temp_daily.csv | lake-specific range 24.0-33.0 C: temperature = depth entries (depth typed in the temperature column) | 13 | 2018-09-21 17 m: 17.035; 2019-03-23 9 m: 9.045; 2019-09-10 7 m: 7.11; 2019-09-10 15 m: 15.033; 2020-01-24 36 m: 36.682; 2020-01-24 68 m: 68.828; 2020-01-24 69 m: 69.025; 2020-01-24 70 m: 69.255; 2020-04-18 0 m: 0.202; 2020-05-16 14 m: 14.008; 2020-07-18 0 m: 0.242; 2020-07-18 22 m: 22.092 |
| Bosumtwi/Bosumtwi_temp_daily.csv | several values at the same time and depth: averaged | 142 | 71 groups |

## Bryrup

| File | Rule | n | Detail |
|---|---|---|---|
| Bryrup/Bryrup_wtemp_daily.csv | several values at the same time and depth: averaged | 42 | 21 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 15 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 4 |  |
| (check) | observations reach 10 m, hypsometry 9 m | | not corrected; see ISSUES.md |

## BurleyGriffin

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 5 |  |

## Chao

| File | Rule | n | Detail |
|---|---|---|---|
| Chao/Chao_temp_daily.csv | missing temperature removed (empty, NA, NaN) | 8 |  |

## Crystal

| File | Rule | n | Detail |
|---|---|---|---|
| Crystal/Crystal_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1 | min -1.30 C |

## CrystalBog

| File | Rule | n | Detail |
|---|---|---|---|
| CrystalBog/CrystalBog_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1 | min -1.50 C |
| CrystalBog/CrystalBog_temp_subdaily_2010.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 35 | min -0.87 C |
| CrystalBog/CrystalBog_temp_subdaily_2011.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1,662 | min -5.78 C |
| CrystalBog/CrystalBog_temp_subdaily_2012.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 14 | min -5.93 C |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 1,133 | 115 days; at common depths the sources differ by median 0.45, max 4.20 C |
| (daily merge) | same day and depth in several files of the same source: averaged | 20 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 216 |  |
| (check) | observations reach 2.5 m, hypsometry 2 m | | not corrected; see ISSUES.md |

## Dickie

| File | Rule | n | Detail |
|---|---|---|---|
| Dickie/Dickie_temp_daily.csv | several values at the same time and depth: averaged | 4 | 2 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 2 |  |

## Eagle

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 1 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 10 |  |

## Ekoln

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | same day and depth in several files of the same source: averaged | 202 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 413 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 55 |  |

## Erken

| File | Rule | n | Detail |
|---|---|---|---|
| erken_watertemp_daily.csv | missing depth removed | 634 |  |
| erken_watertemp_daily.csv | depths given as negative numbers (height); sign flipped to depth below surface | 267,222 |  |
| erken_watertemp_daily.csv | several values at the same time and depth: averaged | 8,886 | 4443 groups |
| Erken/Erken_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 2 | min -0.99 C |
| Erken/Erken_temp_daily.csv | several values at the same time and depth: averaged | 9,111 | 4553 groups |
| Erken/Erken_temp_subdaily_1990.csv | empty source file (header only), skipped | 1 |  |
| Erken/Erken_temp_subdaily_1993.csv | empty source file (header only), skipped | 1 |  |
| Erken/Erken_temp_subdaily_1994.csv | empty source file (header only), skipped | 1 |  |
| Erken/Erken_temp_subdaily_1995.csv | empty source file (header only), skipped | 1 |  |
| Erken/Erken_temp_subdaily_1996.csv | empty source file (header only), skipped | 1 |  |
| Erken/Erken_temp_subdaily_1997.csv | empty source file (header only), skipped | 1 |  |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 212,768 | 8853 days; at common depths the sources differ by median 0.00, max 4.05 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 6 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 19 |  |
| erken_hypsometry.csv | ISIMIP4 hypsometry used; ISIMIP3 file identical | 1 |  |

## EsthwaiteWater

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | same day and depth in several files of the same source: averaged | 48 |  |

## FallingCreek

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 4,443 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 328 |  |
| (check) | observations reach 10.989 m, hypsometry 9.3 m | | not corrected; see ISSUES.md |

## Feeagh

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 59,085 | 4534 days; at common depths the sources differ by median 0.00, max 0.86 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 8 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 1 |  |
| feeagh_hypsometry.csv | ISIMIP4 hypsometry used; ISIMIP3 file differs | 1 | ISIMIP3 48 levels to 46.8 m, ISIMIP4 48 levels to 46.8112 m |

## Fish

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 6 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 1 |  |
| (check) | observations reach 20.8 m, hypsometry 19 m | | not corrected; see ISSUES.md |

## Grossglienickersee

| File | Rule | n | Detail |
|---|---|---|---|
| grossglienickersee_watertemp_subdaily.csv | missing temperature removed (empty, NA, NaN) | 16,223 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 1 |  |

## Harp

| File | Rule | n | Detail |
|---|---|---|---|
| harp_watertemp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 10 | min -0.99 C |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 30,925 | 753 days; at common depths the sources differ by median 0.00, max 5.35 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 2 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 9 |  |

## Hassel

| File | Rule | n | Detail |
|---|---|---|---|
| Hassel/Hassel_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1 | min -7.30 C |
| Hassel/Hassel_temp_daily.csv | several values at the same time and depth: averaged | 200 | 95 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 3 |  |
| (check) | observations reach 15.933 m, hypsometry 14 m | | not corrected; see ISSUES.md |

## Hulun

| File | Rule | n | Detail |
|---|---|---|---|
| Hulun/Hulun_temp_daily.csv | missing temperature removed (empty, NA, NaN) | 34 |  |

## InreHarrsjon

| File | Rule | n | Detail |
|---|---|---|---|
| inreharrsjon_watertemp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1,909 | min -11.76 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 69 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 18 |  |

## Kinneret

| File | Rule | n | Detail |
|---|---|---|---|
| Kinneret/Kinneret_temp_daily.csv | several values at the same time and depth: averaged | 2 | 1 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 3 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 2 |  |

## Klicava

| File | Rule | n | Detail |
|---|---|---|---|
| Klicava/Klicava_temp_daily.csv | several values at the same time and depth: averaged | 16 | 8 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 1 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 24 |  |

## Kuivajarvi

| File | Rule | n | Detail |
|---|---|---|---|
| Kuivajarvi/Kuivajarvi_temp_subdaily_2017.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 790 | min -3.02 C |
| (daily merge) | same day and depth in several files of the same source: averaged | 128 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 38 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 2 |  |
| (check) | observations reach 12 m, hypsometry 10 m | | not corrected; see ISSUES.md |

## Langtjern

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 1 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 6 |  |

## LowerLakeZurich

| File | Rule | n | Detail |
|---|---|---|---|
| lower-zurich_watertemp_daily.csv | missing temperature removed (empty, NA, NaN) | 1 |  |
| Zurich/Zurich_Temp.csv | header lacked the DEPTH column (5 data columns, 4 names); columns re-assigned | 22,365 |  |
| Zurich/Zurich_Temp.csv | file of ISIMIP3 folder 'Zurich' assigned to LowerLakeZurich: the 'Zurich' folder holds Lower Lake Zurich data (CH-ZUR rows = the ISIMIP4 Lower Lake Zurich file, 1981-2022) | 22,365 |  |
| Zurich/Zurich_Temp.csv | missing temperature removed (empty, NA, NaN) | 1 |  |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 29,291 | 497 days; at common depths the sources differ by median 0.00, max 2.70 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 3 |  |
| lower-zurich_hypsometry.csv | ISIMIP4 hypsometry used; ISIMIP3 file identical | 1 |  |

## MellerstaHarrsjon

| File | Rule | n | Detail |
|---|---|---|---|
| mellerstaharrsjon_watertemp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 2,594 | min -20.16 C |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 210 |  |

## Mendota

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 3 |  |
| (check) | observations reach 25.2 m, hypsometry 25 m | | not corrected; see ISSUES.md |

## Monona

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 4 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 1 |  |
| (check) | observations reach 23 m, hypsometry 21.336 m | | not corrected; see ISSUES.md |

## Mozhaysk

| File | Rule | n | Detail |
|---|---|---|---|
| Mozhaysk/Mozhaysk_temp_daily.csv | missing depth removed | 1 |  |
| Mozhaysk/Mozhaysk_temp_daily.csv | several values at the same time and depth: averaged | 322 | 161 groups |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 735 | 105 days; at common depths the sources differ by median 0.24, max 6.80 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 17 |  |

## MtBold

| File | Rule | n | Detail |
|---|---|---|---|
| MtBold/MtBold_temp_subdaily_2009.csv | empty source file (header only), skipped | 1 |  |
| MtBold/MtBold_temp_subdaily_2010.csv | empty source file (header only), skipped | 1 |  |
| MtBold/MtBold_temp_subdaily_2011.csv | empty source file (header only), skipped | 1 |  |
| MtBold/MtBold_temp_subdaily_2012.csv | empty source file (header only), skipped | 1 |  |
| (daily merge) | same day and depth in several files of the same source: averaged | 216 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 104 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 423 |  |

## Neuchatel

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 1 |  |

## NohipaloMustjarv

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | same day and depth in several files of the same source: averaged | 16 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 4 |  |

## NohipaloValgejarv

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | same day and depth in several files of the same source: averaged | 32 |  |

## Rappbode

| File | Rule | n | Detail |
|---|---|---|---|
| Rappbodep/Rappbodep_temp_subdaily_2015.csv | file of ISIMIP3 folder 'Rappbodep' assigned to Rappbode: profiles reach 48-79 m but the pre-dam is ~17 m deep; the 44 days of 2015 that are also in the Rappbode reservoir daily file are identical to it (max difference < 1e-8 C): main-reservoir data filed under the pre-dam | 10,174 |  |
| Rappbodep/Rappbodep_temp_subdaily_2016.csv | file of ISIMIP3 folder 'Rappbodep' assigned to Rappbode: profiles reach 48-79 m but the pre-dam is ~17 m deep; the 44 days of 2015 that are also in the Rappbode reservoir daily file are identical to it (max difference < 1e-8 C): main-reservoir data filed under the pre-dam | 24,261 |  |
| Rappbodep/Rappbodep_temp_subdaily_2017.csv | file of ISIMIP3 folder 'Rappbodep' assigned to Rappbode: profiles reach 48-79 m but the pre-dam is ~17 m deep; the 44 days of 2015 that are also in the Rappbode reservoir daily file are identical to it (max difference < 1e-8 C): main-reservoir data filed under the pre-dam | 4,271 |  |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 9,802 | 46 days; at common depths the sources differ by median 0.00, max 0.15 C |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 16 |  |

## Rappbodep

| File | Rule | n | Detail |
|---|---|---|---|
| Rappbodep/(moved files) | ISIMIP3 files of this folder moved to another lake: profiles reach 48-79 m but the pre-dam is ~17 m deep; the 44 days of 2015 that are also in the Rappbode reservoir daily file are identical to it (max difference < 1e-8 C): main-reservoir data filed under the pre-dam | 3 |  |
| Rappbodep/Rappbodep_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 3 | min -9.60 C |
| Rappbodep/Rappbodep_temp_daily.csv | several values at the same time and depth: averaged | 46 | 13 groups |

## Rimov

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | same day and depth in several files of the same source: averaged | 126 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 2,269 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 1 |  |

## Rotorua

| File | Rule | n | Detail |
|---|---|---|---|
| Rotorua/Rotorua_temp_daily.csv | several values at the same time and depth: averaged | 9,328 | 4664 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 5 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 10 |  |

## Sammamish

| File | Rule | n | Detail |
|---|---|---|---|
| Sammamish/Sammamish_temp_subdaily_2000.csv | several values at the same time and depth: averaged | 8 | 4 groups |
| Sammamish/Sammamish_temp_subdaily_2002.csv | several values at the same time and depth: averaged | 8 | 4 groups |
| Sammamish/Sammamish_temp_subdaily_2003.csv | several values at the same time and depth: averaged | 4 | 2 groups |
| Sammamish/Sammamish_temp_subdaily_2005.csv | several values at the same time and depth: averaged | 2 | 1 groups |
| Sammamish/Sammamish_temp_subdaily_2006.csv | several values at the same time and depth: averaged | 199,060 | 49745 groups |
| Sammamish/Sammamish_temp_subdaily_2007.csv | several values at the same time and depth: averaged | 229,627 | 57387 groups |
| Sammamish/Sammamish_temp_subdaily_2008.csv | negative depth in a file of positive depths removed | 1 |  |
| Sammamish/Sammamish_temp_subdaily_2008.csv | several values at the same time and depth: averaged | 2,911 | 1442 groups |
| Sammamish/Sammamish_temp_subdaily_2009.csv | several values at the same time and depth: averaged | 1,413 | 706 groups |
| Sammamish/Sammamish_temp_subdaily_2010.csv | several values at the same time and depth: averaged | 1,323 | 661 groups |
| Sammamish/Sammamish_temp_subdaily_2011.csv | several values at the same time and depth: averaged | 1,374 | 687 groups |
| Sammamish/Sammamish_temp_subdaily_2012.csv | several values at the same time and depth: averaged | 1,222 | 610 groups |
| Sammamish/Sammamish_temp_subdaily_2013.csv | several values at the same time and depth: averaged | 910 | 455 groups |
| Sammamish/Sammamish_temp_subdaily_2014.csv | several values at the same time and depth: averaged | 1,162 | 581 groups |
| Sammamish/Sammamish_temp_subdaily_2015.csv | several values at the same time and depth: averaged | 44 | 22 groups |
| Sammamish/Sammamish_temp_subdaily_2016.csv | several values at the same time and depth: averaged | 558 | 279 groups |
| Sammamish/Sammamish_temp_subdaily_2017.csv | several values at the same time and depth: averaged | 357 | 178 groups |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 27,561 | 395 days; at common depths the sources differ by median 0.00, max 3.44 C |
| (daily merge) | same day and depth in several files of the same source: averaged | 48 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 17,892 |  |
| sammamish_hypsometry.csv | ISIMIP4 hypsometry used; ISIMIP3 file identical | 1 |  |

## Sau

| File | Rule | n | Detail |
|---|---|---|---|
| Sau/Sau_temp_daily.csv | several values at the same time and depth: averaged | 110 | 55 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 68 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 10 |  |
| (check) | observations reach 65 m, hypsometry 59.54 m | | not corrected; see ISSUES.md |

## Scharmutzel

| File | Rule | n | Detail |
|---|---|---|---|
| Scharmutzel/Scharmutzel_wtemp_subdaily_2019.csv | missing temperature removed (empty, NA, NaN) | 1,477 |  |
| Scharmutzel/Scharmutzel_wtemp_subdaily_2020.csv | missing temperature removed (empty, NA, NaN) | 7,666 |  |
| Scharmutzel/Scharmutzel_wtemp_subdaily_2021.csv | missing temperature removed (empty, NA, NaN) | 74 |  |

## Sparkling

| File | Rule | n | Detail |
|---|---|---|---|
| Sparkling/Sparkling_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1 | min -0.70 C |
| Sparkling/Sparkling_temp_subdaily_1999.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 278 | min -4.66 C |
| Sparkling/Sparkling_temp_subdaily_2000.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 496 | min -3.89 C |
| Sparkling/Sparkling_temp_subdaily_2002.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 221 | min -1.94 C |
| Sparkling/Sparkling_temp_subdaily_2003.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1,544 | min -3.09 C |
| Sparkling/Sparkling_temp_subdaily_2005.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1,114 | min -3.87 C |
| Sparkling/Sparkling_temp_subdaily_2006.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 71 | min -1.89 C |
| Sparkling/Sparkling_temp_subdaily_2014.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1 | min -1.85 C |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 5,056 | 340 days; at common depths the sources differ by median 0.25, max 5.07 C |
| (daily merge) | same day and depth in several files of the same source: averaged | 228 |  |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 110 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 9 |  |
| (check) | observations reach 20 m, hypsometry 19 m | | not corrected; see ISSUES.md |

## Sunapee

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 14,139 | 1117 days; at common depths the sources differ by median 0.00, max 5.34 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 30 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 18 |  |

## Tahoe

| File | Rule | n | Detail |
|---|---|---|---|
| Tahoe/Tahoe_temp_daily.csv | several values at the same time and depth: averaged | 936 | 128 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 81 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 2 |  |

## Taihu

| File | Rule | n | Detail |
|---|---|---|---|
| taihu_hypsometry.csv | hypsometry depth axis inverted (area grew with depth at every level); re-expressed as depth below the surface | 11 | source surface area 0 m2 at depth 0; after fix 2.32961e+09 m2 at 0 m |

## Tarawera

| File | Rule | n | Detail |
|---|---|---|---|
| Tarawera/Tarawera_temp_daily.csv | date written as yymmdd (6 digits), read as 20yy-mm-dd | 162 | 160101, 160102 |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 26 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 53 |  |

## Toolik

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 6 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 1 |  |

## Trout

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 2,450 | 111 days; at common depths the sources differ by median 0.26, max 15.20 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 770 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 376 |  |
| Trout_hypsometry.csv | hypsometry: areas ten times too large (decimal shift: 160,790,000 m2 at the surface vs 16,079,000 m2 = 1,607.9 ha, NTL-LTER); all areas divided by 10 | 34 |  |
| (check) | observations reach 35 m, hypsometry 33 m | | not corrected; see ISSUES.md |

## TroutBog

| File | Rule | n | Detail |
|---|---|---|---|
| TroutBog/TroutBog_temp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 2 | min -1.10 C |
| TroutBog/TroutBog_temp_subdaily_2004.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 446 | min -3.20 C |
| TroutBog/TroutBog_temp_subdaily_2005.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 2,342 | min -5.65 C |
| TroutBog/TroutBog_temp_subdaily_2006.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 795 | min -1.55 C |
| TroutBog/TroutBog_temp_subdaily_2007.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 100 | min -2.58 C |
| TroutBog/TroutBog_temp_subdaily_2010.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 456 | min -2.72 C |
| TroutBog/TroutBog_temp_subdaily_2011.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 2,199 | min -6.12 C |
| TroutBog/TroutBog_temp_subdaily_2012.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 1,009 | min -2.35 C |
| TroutBog/TroutBog_temp_subdaily_2013.csv | empty source file (header only), skipped | 1 |  |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 1,426 | 144 days; at common depths the sources differ by median 0.50, max 4.05 C |
| (daily merge) | same day and depth in several files of the same source: averaged | 76 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 3 |  |

## TwoSisters

| File | Rule | n | Detail |
|---|---|---|---|
| TwoSisters/TwoSisters_temp_daily.csv | several values at the same time and depth: averaged | 2 | 1 groups |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 2 |  |

## Vendyurskoe

| File | Rule | n | Detail |
|---|---|---|---|
| vendyurskoe_watertemp_daily.csv | several values at the same time and depth: averaged | 2 | 1 groups |
| Vendyurskoe/Vendyurskoe_temp_daily.csv | several values at the same time and depth: averaged | 2 | 1 groups |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 25,721 | 2621 days; at common depths the sources differ by median 0.00, max 0.00 C |
| vendyurskoe_hypsometry.csv | ISIMIP4 hypsometry used; ISIMIP3 file identical | 1 |  |

## Villasjon

| File | Rule | n | Detail |
|---|---|---|---|
| villasjon_watertemp_daily.csv | temperature below -0.5 C removed (logger frozen in ice / not liquid water) | 2,824 | min -22.10 C |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 51 |  |

## Vortsjarv

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | same day and depth in several files of the same source: averaged | 16 |  |

## Washington

| File | Rule | n | Detail |
|---|---|---|---|
| Washington/washington_temp_daily.csv | several values at the same time and depth: averaged | 182 | 91 groups |
| (daily merge) | day also in a higher-priority source: lower-priority values of that day not used (ISIMIP4 > ISIMIP3 daily > ISIMIP3 sub-daily mean) | 12,620 | 475 days; at common depths the sources differ by median 0.00, max 2.80 C |
| (daily, flag only) | QC flag 'unstable' set (value kept) | 1 |  |
| (daily, flag only) | QC flag 'outlier' set (value kept) | 3 |  |
| washington_hypsometry.csv | ISIMIP4 hypsometry used; ISIMIP3 file identical | 1 |  |

## Windermere

| File | Rule | n | Detail |
|---|---|---|---|
| (daily merge) | same day and depth in several files of the same source: averaged | 48 |  |

## Wingra

| File | Rule | n | Detail |
|---|---|---|---|
| (daily, flag only) | QC flag 'unstable' set (value kept) | 3 |  |

## Zlutice

| File | Rule | n | Detail |
|---|---|---|---|
| Zlutice/Zlutice_temp_daily.csv | several values at the same time and depth: averaged | 6 | 3 groups |

