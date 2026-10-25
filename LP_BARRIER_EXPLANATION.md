# Certified LP barrier and kernel

VERIFIED: the supplied vector z has 369 rational entries in [0,1], denominator 1,000,000, covers every original target with closed-neighborhood numerator at least 1,000,007, and has objective 13,513,576/1,000,000 = 13.513576 < 14. All checks use integer arithmetic. It is a fractional cover, **not** an integer dominating set or an upper bound of 14 for the integer problem.

For any ordinary nonnegative vertex-weight dual y satisfying the original column inequalities, weak duality gives sum(y) <= sum(z) < 14. Thus no choice of such an unconditional dual can yield ceil(sum(y)) >= 15. Raising the integer lower bound beyond 14 requires additional integer structure, valid cuts, branching, conditional bounds or another method; it cannot come merely from retuning the same plain dual weights. This does not rule out the already verified weighted-union cuts, which exploit the integer cardinality assumption.

VERIFIED: all 20 column replacements map directly to one of the 349 retained candidates, the removed and retained IDs partition all 369 IDs, and each replacement satisfies N[u] subset N[v]. No cycles occur (every path has length one). Replacing a selected removed column preserves coverage and does not increase cardinality. This proves existence preservation, not that every old solution already avoided those 20 variables. Any new lower-bound proof using the kernel must explicitly compose this replacement argument with its augmented CNF proof.

See cert_lp_barrier.json and cert_kernel.json for file hashes and independent integer receipts. No optimization was run by this check.
