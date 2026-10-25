# Certified bounds for OEIS A365621(8)

**14 <= a(8) <= 17. The exact value remains unknown.**

This repository publishes coordinates and independently executable certificates. The official OEIS entry checked on 2026-10-25 still listed the upper bound18; the 17-shape witness improves that recorded upper bound. This is not a claim of global priority. An OEIS update has not yet been submitted.

## Reproduce with Python standard library only

```sh
python -B verify_release.py --inputs inputs --output my_check.json --rebuild --cuts dual_cuts_k14.json
```

Use a new output path; the verifier refuses to overwrite existing receipts. No SAT, LP, numpy or third-party package is needed. `--rebuild` generates2725 translation-only fixed octominoes, takes their D4 quotient to369 free shapes and independently checks all67896 vertex pairs, reconstructing6544 graph edges. It then verifies the coordinates, every explicit one-cell move and all369 integer dual inequalities. `VERIFICATION.json` records an actual local execution, not an assumed pass.

## Mathematical object

Vertices are free octominoes, modulo integer translations, rotations and reflections. Distinct vertices are adjacent if representatives overlap in exactly seven cells. The detached intermediate is allowed to be disconnected. No sliding path or bound on move distance is imposed. This matches [A365621](https://oeis.org/A365621) and [A098891](https://oeis.org/A098891). It is not a cell-adjacency graph.

## Certificates

- `upper17_coordinates.csv`, `UPPER17_CONFIGURATIONS.md`, and `inputs/UPPER17.json` contain all17 shapes. IDs are zero-based positions in `inputs/graph_n8.json`, not an asserted OEIS-wide ordering.
- `inputs/independent_highs17.json` contains an explicit remove/add witness for every non-selected target. Selected shapes cover themselves.
- `lower14_weights.csv` and `inputs/LOWER14_RATIONAL.json` contain nonnegative integer target weights. Their sum is1351314766, with denominator100000000. Every closed-neighborhood sum is at most99999999. For any dominating setS, the total target weight is at most the sum of the selected closed-neighborhood weights, hence |S| >= ceil(13.51314766)=14. Only integer arithmetic is needed.
- `dual_cuts_k14.json` contains certified necessary conditions for the <=14 decision. These are not an UNSAT proof.
- `FRACTIONAL_LP_BARRIER.json` describes a fractional cover of cost13.513576, not an integer dominating set. It explains why ordinary nonnegative vertex-weight duals alone cannot certify15.

## Provenance and limits

Implementation, derivations and documentation were AI-assisted and validated using distinct implementations. This is not external human peer review. No n8 UNSAT certificate or proof of exact value17 is claimed. A human OEIS contributor must understand the programs and comply with the [OEIS policy on AI-assisted submissions](https://oeis.org/wiki/Use_of_AI_for_OEIS_Submissions_is_Forbidden), including writing their own comment. Do not attribute authorship to an AI tool.

`RELEASE_FILES.csv` lists SHA256 hashes of distributed files, excluding itself. No blanket license grant is made by this evidence publication. GitHub account ownership is not a claim that these results have undergone human expert review.
