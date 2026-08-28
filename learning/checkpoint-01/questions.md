# Checkpoint 1 — explain-the-decision questions

Answer in your own words, no code needed. The point is to check you
understand *why* each decision was made, not just that the notebooks ran.
See `README.md` in this folder for how to use this — don't check
`answers.md` until you've genuinely attempted all ten.

1. `Crime ID` is missing for ~21% of London's rows. Why is that not a data
   loading bug, and how did we confirm it?

2. `.duplicated()` and `.duplicated(keep=False)` give different results.
   What's the difference, and why did it matter when we wanted to look at
   both rows of a repeated Crime ID?

3. `add_area_column` parses a borough/district name out of `"LSOA name"`
   using `rsplit(" ", n=1)` rather than `split(" ")[0]`. Why does that
   distinction matter for names like "Kensington and Chelsea 003C"?

4. We found 325 distinct "boroughs" in the raw London data instead of the
   real 33. What caused that, and why did we fix it by filtering with
   `.isin(LONDON_BOROUGHS)` rather than trying to correct each bad value
   individually?

5. Westminster has by far the highest raw crime *count* of any London
   borough. Why is that a misleading way to judge resident risk, and how
   does converting to a per-capita rate change (or not change) the
   picture?

6. Before correlating deprivation with per-capita crime rate, we excluded
   both Westminster and City of London. Explain the specific distortion
   each one causes — are they the same reason, or different?

7. `load_deprivation()` returns both `IMD_score` and `Income_score`. Why
   check the relationship against both, rather than relying on
   `IMD_score` alone?

8. `NAME_ALIASES` maps `"Herefordshire, County of"` to `"Herefordshire"`.
   What would break (and where — in which loader function(s)) if this
   alias didn't exist?

9. The London vs. West Mercia comparison notebook plots both forces'
   choropleth maps on a **shared** color scale, rather than letting each
   map scale independently to its own min/max. What would an
   independently-scaled pair of maps have visually implied that would
   have been misleading?

10. West Mercia's per-capita crime rate correlates strongly with
    deprivation immediately (no exclusions needed), while London's needed
    Westminster and City of London excluded first to get a comparably
    strong result. What does that difference suggest about how the two
    forces' crime patterns differ?
