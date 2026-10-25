# A367441(8) = 54: exact result and proof

**54 connected free heptominoes are necessary and sufficient to generate every free octomino by adding one cell.** Equivalence is under translation, rotation and reflection. The model has 108 selectable heptominoes, 369 target octominoes and 1,197 parent-target incidences.

Download the complete evidence and checksum from the [a367441-n8-v1.0.0 release](https://github.com/Jason-XiongLuHang/oeis-a365621-n8-bounds/releases/tag/a367441-n8-v1.0.0). This is a separate result from A365621(8) = 17; the older releases are retained.

## Construction and lower-bound certificate

`PARENTS54.csv` gives the 54 parents' coordinates; `B8_CONSTRUCTION.json` gives their indices and shapes. Its original status field predates independent certification: the later verification receipts in the archive certify the construction. The archive contains an add-one-cell geometric witness for each of the 369 targets.

A complete 20,399-node proof tree excludes covers of size at most 53. Its private-target deductions use a separately checked, complete 14,353-node proof excluding covers of size at most 52. Both frontiers are empty. The checker replays the dependency and rejects circular dependencies. Eight corrupted-certificate negative controls were rejected.

These are custom combinatorial proof trees checked by separate standard-library Python code, not DRAT/LRAT certificates or proof-assistant formalizations. Optimizer status is not used as mathematical evidence.

## Independent reproduction

Extract the ZIP and run from its root with Python 3.12, standard library only. Use fresh output names and do not enable Python's `-O` option (the checkers use assertions).

```text
python -B verify_b8_geometry.py --output-prefix MY_MODEL_CHECK
python -B check_b8_tree_v2.py proof_k53_private --output MY_FULL_TREE_CHECK.json
```

The first check independently generates the free-polyomino census through eight cells (1, 1, 2, 5, 12, 35, 108, 369), checks all 39,852 possible parent-target pairs and the 54-parent construction. Its reported lower bound 48 is an earlier weight certificate; it is not the final lower bound.

The second must report `PROVED UNSAT`, `k=53`, `strict_lower=54`, `nodes=20399`, `open=0`. Its dependency must report `k=52`, `strict_lower=53`, `nodes=14353`, `open=0`. Together the checks establish the exact value 54. The historical `proof_k53/` partial tree is retained for provenance; the final proof is `proof_k53_private/`.

The archive contains the full code, model, construction, geometric witnesses, proof trees, verification receipts, negative controls and search logs. `MANIFEST.json` lists 54 payload files with sizes and SHA-256 hashes. The ZIP checksum is:

```text
d9516d4678536b2ef9d813f35b12686989c2525fa04e4168d723b26e9a689c9c  A367441_n8_exact54_v1.0.0.zip
```

## Scope and credit

Sequence definition and original authorship: [OEIS A367441](https://oeis.org/A367441), Pontus von Brömssen. Evidence contributor: Xiong Luhang. This work matches the previously published upper bound 54 with a lower-bound certificate; it does not claim a smaller construction or priority over unpublished work.

AI tools assisted with coding and analysis. Separate program checks are computational verification, not external human peer review. No new license grant is made beyond the rights held by contributors. This GitHub publication does not submit or alter an OEIS entry.
