# Checks and evidence

## Isolated execution

Use a disposable clone or a worktree if the harness permits writing its parent
repository metadata. A clone avoids changing the user's checkout or shared Git
metadata. Keep reports and the review ledger in a dedicated scratch directory
outside the PR source tree. Reuse that directory only for the same PR/revision.

1. Record the PR's base SHA and head SHA. Fetch enough history to calculate their
   merge base; shallow history must not silently change the comparison.
2. Check out the recorded head detached. Obtain the complete diff from merge base
   to head, including new, renamed, deleted, and binary files. A binary/generated
   artifact may require checking its source or consumer rather than text review.
3. Find the affected modules, documented check commands, pinned runtime/tool
   versions, formatter settings, test suites, and coverage configuration.
4. Inspect build scripts before running them. Use repository wrappers/lockfiles
   and the host's permitted isolation; a temporary clone alone does not prevent
   network access, credentials access, or deployment side effects. Run local
   verification tasks only. Do not use `publish`, `deploy`, release, infrastructure
   apply, or live production tests as part of a review.
5. Use existing tools first. If a required tool is absent, use a disposable tool
   environment when supported and permitted; otherwise mark the check unverified.
   Do not add dependencies to the PR or install tools globally to finish a review.
6. Record commands, runtime versions, exit status, revision, and relevant report
   paths. Unexpected build/test failures need base comparison before attributing
   them to the PR. Use a separate base checkout when a comparison is necessary.

## Formatting and naming

Find configuration such as `.editorconfig`, formatter/linter files, pre-commit
settings, Checkstyle, or Spotless. Run the existing formatter's check-only mode;
task names vary by repository. Filter findings to introduced/worsened violations.
If there is no configured formatter, inspect formatting against nearby code and
the language's documented style; label the check manual, not tool-verified.

Check names within the relevant scope: object keys, variables, methods, and files.
Existing camelCase JSON keys imply camelCase additions. New unconstrained JSON
uses the user's camelCase preference; Python variables use snake_case and Java
variables camelCase. External schemas, serialized public contracts, overrides,
and generated code can require other spellings. Avoid suggesting a rename that
would break a contract. Flag vague or misleading names with the specific ambiguity
and a contextual alternative, rather than a subjective dislike.

## Cyclomatic complexity

Use the repository's analyzer first, configured for **cyclomatic complexity** at
method/function level. A Sonar project total or cognitive-complexity warning is
not the requested metric. Consult the analyzer's language-specific definition
and version before interpreting a score; do not estimate it with a regex that
counts `if` tokens in comments, strings, or unrelated scopes.

- A new method scoring 13 passes; 14 fails.
- A changed method scoring 12 before and 14 after is a PR finding.
- An existing method scoring 20 before and 20 after is an existing problem, even
  if nearby formatting changed; do not flag it in this PR.
- A changed method scoring 20 before and 21 after worsens the problem: report the
  increase and suggest addressing the introduced complexity.
- A score of 20 reduced to 18 remains above the target but is not introduced or
  worsened; do not require this PR to finish the existing cleanup.

Use an available language-aware analyzer in isolation if the repository has none.
If precise measurement is unavailable, say so; do not invent a numeric score or
claim the threshold passed. Anchor an evidenced violation to the changed decision
logic or method declaration within a reviewable diff range.

## Coverage of added lines

Compute coverage from **unit-test** execution for the recorded head, restricted
to added executable production lines in the merge-base-to-head diff. Replacement
lines count as additions; deleted and unchanged lines do not. Do not silently use
a combined integration/unit report as proof of unit-test coverage.

Let A be the added executable production lines, and H the members of A hit by at
least one unit test. Coverage is `100 * |H| / |A|`; pass when the unrounded ratio
is **>= 80%**. Do not round 79.9% into a pass. If A is empty, report not applicable
with a reason, rather than an invented 100%.

Use the repository's diff-coverage tooling where available. `diff-cover` supports
common reports such as Cobertura and JaCoCo. An example for an already-produced
report and recorded diff, after checking the installed tool's help:

```sh
git diff --no-ext-diff --find-renames --unified=0 <merge-base-sha> <head-sha> -- > <scratch>/pr.diff
diff-cover <coverage-report.xml> --diff-file=<scratch>/pr.diff --fail-under=80
```

The placeholders are inputs to substitute and quote, not literal shell commands.
Use the tool's supported report format and path/source-root options as needed.
Map report paths carefully for monorepos and renamed files; union hit information
for the same source line without double-counting it across reports.

**Validate the denominator before trusting any percentage.** A diff tool may
intersect only lines that appear in the coverage report, silently omitting a new
unimported/uninstrumented file. Inventory every added production source file and
confirm it is represented with executable-line data, including zero-hit lines.
Review changed multi-line statements that line-level instrumentation cannot map.
If production files or lines are missing, regenerate complete instrumentation
when possible; otherwise report coverage as incomplete/unverified, not passing.
Do not classify absent coverage data as proof that a file is non-executable.

Exclude comments, blank lines, and non-executable data. Inspect documented
generated/vendor/test exclusions for correctness; do not create exclusions to
reach 80%, and do not count test code as production code. Pure build/declarative
configuration may not have a meaningful unit-line denominator: explain this and
validate behavior through suitable tests instead.

Report covered/total counts, percentage, evidence source, and uncovered locations.
Below 80%, propose a comment on representative uncovered added logic, explaining
which behavior needs a unit test. At or above 80%, do not demand coverage for all
remaining lines just to reach 100%. A separate demonstrated correctness problem
may still justify a targeted test recommendation.

Sources:

- [diff-cover usage and report formats](https://github.com/Bachmann1234/diff_cover)
- [Sonar metric definitions](https://docs.sonarsource.com/sonarqube-server/user-guide/code-metrics/metrics-definition)

The 80% coverage and 13 complexity thresholds are this user's review policy;
do not describe them as universal language or Sonar defaults.
