# OEIS A365621(8) = 17

This repository provides reproducible evidence for the eighth term of OEIS A365621, the domination number of the graph of free octominoes under the sequence's single-cell move rule.

The graph has 369 vertices and 6,544 edges. A 17-vertex dominating set proves the upper bound. An exhaustive, independently replayed exact search excludes dominating sets of size at most 16, proving the matching lower bound. Thus **a(8) = 17** for this graph definition.

## Evidence and reproduction

Download the complete evidence archive and its SHA-256 checksum from the [v2.0.0 release](https://github.com/Jason-XiongLuHang/oeis-a365621-n8-bounds/releases/tag/v2.0.0). The archive contains the complete proof tree, graph inputs, the Python standard-library checker, an independent geometric reconstruction, the 17-vertex construction, and run records. The large proof tree is kept in the release archive rather than Git history.

After extracting the archive, run from its root with Python 3.12 (standard library only):

```powershell
python -B verify_v3_sparse.py LATEST_PROOF --inputs inputs --output MY_ROOT_VERIFICATION.json
```

The output path must not already exist. The expected result is `PROVED`, `k=16`, `strict_lower=17`, `frontier=0`, and `nodes=759011`. The checker also validates the 5,481-node lower-bound dependency. Allow about 8 GiB of available RAM; the recorded independent check took about 183 seconds on the original machine.

The archive includes a separate geometry rebuild and upper-bound verification. Hashes of the principal artifacts are listed in `LATEST_RESULT.json` within the archive. Archive checksum:

```text
a52f1011b7c46aacd50940eb0379629c7815f83e13f00c6b39b4aa194c3bce03  A365621_n8_exact17_v2.0.0.zip
```

`DOMINATING_SET_17.csv` and `.json` give the upper-bound construction. `LATEST_RESULT.json` records the exact result and the proof/graph/checker hashes.

## Scope and provenance

The move graph uses translation, rotation, and reflection equivalence; removal of a cell is allowed to leave a disconnected seven-cell intermediate shape before one cell is reattached. See the OEIS entry for the canonical sequence definition: <https://oeis.org/A365621>.

The older v1.0.0 release and root-level historical files document the former interval `14 <= a(8) <= 17`; they are retained as historical evidence. This v2.0.0 release supplies the complete exact-value proof.

AI tools assisted with coding and analysis. The archive records human responsibility and the verification scope. No claim of external peer review or priority over unpublished work is made. This repository does not grant a license beyond the rights held by its contributors.


## Related result: A367441(8) = 54

The minimum number of free heptomino parents generating all 369 free octominoes by adding one cell is exactly **54**. A 54-parent construction and complete independently checked exclusion of covers of size at most 53 are available in the separate [a367441-n8-v1.0.0 release](https://github.com/Jason-XiongLuHang/oeis-a365621-n8-bounds/releases/tag/a367441-n8-v1.0.0). See [the result and reproduction instructions](a367441-n8/README.md). This does not change the A365621 result or its v1.0.0/v2.0.0 release assets.
