# Checkpoint 1 — answer key

Don't read this until you've attempted `questions.md` and
`spot_the_bug.ipynb` yourself. These are model answers, not the only
acceptable phrasing — the point is whether your reasoning matches, not
the exact wording.

## Part 1 — `questions.md`

1. It's deliberate anonymisation by the police, not a bug — confirmed by
   grouping `Crime type` where `Crime ID` is null: **every single one** is
   "Anti-social behaviour". ASB reports don't get a trackable case ID or a
   formal outcome (`Last outcome category` is null for the same rows),
   presumably to protect reporters/victims in what are often
   neighbour-dispute-type incidents.

2. `.duplicated()` defaults to marking only the **second-and-later**
   occurrence of a repeated value as `True`; the first occurrence stays
   `False` (hidden). That's fine for *counting* how many duplicates exist,
   but if you want to actually see every row involved — both the original
   and the repeat, side by side — you need `keep=False`, which flags *all*
   copies of a repeated value as `True`, first occurrence included.

3. Multi-word area names like "Kensington and Chelsea 003C" contain
   several spaces. `split(" ")[0]` would grab only the first token
   ("Kensington"), losing "and Chelsea". `rsplit(" ", n=1)` splits from
   the *right*, at most once, so it always peels off exactly the trailing
   LSOA sub-code token and leaves the rest of the name — however many
   words — intact.

4. `LSOA name` sometimes contains area names outside the real 33 London
   boroughs (e.g. neighbouring counties' LSOAs bleeding in at the edges of
   the force boundary, similar to West Mercia's Welsh-border pattern).
   Only 6,491 rows (0.53%) fell outside the real set. Filtering with
   `.isin(LONDON_BOROUGHS)` was the right fix rather than correcting each
   bad value individually because there's no meaningful "correction" to
   make — those rows genuinely belong to a different administrative area;
   they're not typos or misspellings of a London borough, so the honest
   move is excluding them from a *London borough* analysis, not relabeling
   them.

5. Raw count conflates two different things: how many crimes happen, and
   how many people are around for crimes to happen *to*. Westminster
   contains the West End, Oxford Street, and most of central London's
   tourist/retail footfall — huge numbers of non-resident people passing
   through — so its raw count is inflated by crime against/among visitors,
   not necessarily elevated risk to the ~200k people who actually live
   there. Per-capita rate (crimes ÷ resident population) is an attempt to
   fix this, but it only partly works: Westminster's *tiny* resident
   population relative to its footfall means even the per-capita number
   stays a genuine outlier (~465/1000/yr) — dividing by residents alone
   doesn't account for non-resident *visitors* still being the ones
   involved in many of the crimes.

6. Different reasons, not the same one. Westminster: huge non-resident
   footfall inflates the numerator (crime count) far more than the
   resident population in the denominator can absorb — a footfall
   distortion. City of London: the *opposite* mechanism — it's the
   business/financial district with an extremely small resident
   population (a few thousand), so even a modest crime count divided by
   that tiny denominator produces a mathematically huge per-capita rate —
   a small-denominator distortion. Both inflate the per-capita number, but
   one is driven by the numerator, the other by the denominator.

7. `IMD_score` is a composite that includes a "Crime" sub-domain
   (~9.3% weight) which is itself partly built from recorded police crime
   data — so correlating our crime counts against `IMD_score` risks partly
   comparing the data against a derivative of itself, inflating the
   apparent relationship. `Income_score` (proportion of the population
   experiencing income deprivation) doesn't include crime data at all, so
   checking that the relationship holds against `Income_score` too is a
   cleaner, more independent check that the deprivation link isn't just
   circular.

8. ONS population data, the MHCLG deprivation file, and the LAD boundary
   GeoJSON all use the official name `"Herefordshire, County of"`, while
   the crime data's `LSOA name` column uses the plain `"Herefordshire"`.
   Without the alias, `load_population()`, `load_deprivation()`, and
   `load_lad_boundaries()` would each fail to find a match for
   "Herefordshire" in their source files (since they filter by exact name
   membership in the requested `names` set) — Herefordshire would silently
   vanish from population, deprivation, and map data, while still being
   present in the crime counts, breaking every join involving it.

9. Independently-scaled maps (each stretched to its own min/max) would
   have made West Mercia's *least*-deprived-equivalent district look just
   as "red"/high on its own scale as London's *most* affected borough —
   visually implying the two forces have comparably wide internal
   variation, when West Mercia is actually uniformly lower than London
   across the board. A shared scale keeps the comparison honest: it shows
   West Mercia as consistently cooler-colored throughout, which is the
   true finding, rather than flattering West Mercia's map into looking
   just as "varied" as London's.

10. It suggests the two forces have structurally different crime
    profiles. London has extreme high-footfall/low-resident-population
    outliers (Westminster, City of London) that are driven by tourism and
    commerce, not resident deprivation — those have to be excluded before
    the deprivation signal, which does exist, can come through clearly
    (0.26 → 0.57). West Mercia has no borough/district anywhere near that
    scale of footfall distortion, so ordinary residents' deprivation
    tracks directly with their local crime rate from the start (IMD 0.69,
    Income 0.71) — a more "textbook" deprivation-crime relationship,
    undistorted by a city-centre effect. (Worcester is a smaller-scale
    echo of the same footfall pattern, but not large enough to need
    excluding the way Westminster/City of London did.)

## Part 2 — `spot_the_bug.ipynb`

**Bug 1 — repeated Crime IDs (cell after "Checking repeated Crime IDs"):**
`is_repeated = london["Crime ID"].duplicated()` is missing `keep=False`.
Default `.duplicated()` only flags second-and-later occurrences, so
`repeated` ends up with only *half* of each pair (roughly 6,899 rows,
matching the `.duplicated().sum()` count from `01_explore.ipynb`) instead
of both rows of every repeat (roughly double that). Fix:
`london["Crime ID"].duplicated(keep=False)`.

**Bug 2 — per-capita rate (cell after "Per-capita crime rate by
borough"):** `borough_counts` is built from `london` directly, without
filtering to `LONDON_BOROUGHS` first — so the printed line reads
`"325 boroughs found"`, flatly contradicting the markdown's claim of "the
33 real London boroughs" right above it. The stray ~292 bogus "boroughs"
(LSOA names from outside Greater London) get `NaN` population after the
merge. Fix: filter before grouping —
`london[london["Borough"].isin(LONDON_BOROUGHS)].groupby("Borough")...`.

**Bug 3 — deprivation correlation (cell after "Correlation with
deprivation"):** the `print()` claims Westminster and City of London are
excluded, but `merged` is never actually filtered — both are still in
there. The printed correlation comes out close to the *raw* ~0.26 figure,
not the ~0.57 figure the project established after excluding them. Fix:
add
`merged = merged[~merged["Borough"].isin(["Westminster", "City of London"])]`
before computing `.corr()`.

**Bug 4 — top-10 chart (cell after "Chart — top 10 boroughs..."):**
selecting the top 10 is correct (`sort_values(ascending=False).head(10)`
does grab the 10 highest rates), but that leaves them in *descending*
order in the DataFrame — borough #1 (highest rate) first, #10 (lowest of
the top 10) last. `barh` draws rows bottom-to-top in DataFrame order, so
the chart comes out **upside down** relative to its own title: the lowest
of the top 10 appears at the top, the actual highest appears at the
bottom. Fix: re-sort ascending before plotting, e.g.
`top10 = top10.sort_values("Rate_per_1000", ascending=True)` right before
the `plt.barh(...)` call.
