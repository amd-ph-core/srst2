# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This repository is a maintenance fork of [katholt/srst2](https://github.com/katholt/srst2)
at tag `v0.2.0` (the last upstream release, 2016), ported to Python 3 and maintained
for continued use.

## [Unreleased]

## [1.0.0-rc.1] - 2026-07-19

Release candidate for v1.0.0. Bundles the Round-2 correctness fixes and
maintenance work on top of the v0.3.x modernized baseline. Several entries are
**behavioral** (they change typing results) and are gated on re-validation
against the PHoeNIx reference dataset before a final v1.0.0 / production cut —
this RC exists precisely so that validation can run against a tagged build.

### Added

- `--label` option to set the sample name used in the output explicitly,
  instead of inferring it from the read file name(s). Only valid for a single
  read set (errors clearly otherwise). ([#62], [katholt#109])
- Brought the bundled `data/` databases up to upstream `73f885f` (the baseline
  the earlier production builds ran; see [#52]): added `ARGannot_r2.fasta` /
  `ARGannot_r3.fasta` (+ their clustered CSVs and the r2 change log) and
  `CARD_v3.0.8_SRST2.fasta` (+ clustered CSV), and updated `EcOH.fasta`,
  `ARGannot_clustered80.csv`, and `data/README.md`. These are reference
  databases only; the PHoeNIx pipeline supplies srst2 an external `--gene_db`
  (`ResGANNCBI_..._srst2.fasta`) / `--mlst_db`, so it never uses these bundled
  files — updating them does not change pipeline behavior. ([#52])

### Changed

- All alleles tied at the best score are now reported per gene/cluster, instead
  of a single arbitrary winner. Previously only `scores_sorted[0]` was reported,
  so when alleles tied at the top score the "winner" depended on the iteration
  order of the score dict (arbitrary, and historically non-deterministic across
  Python 2 dict orderings) — scientifically indefensible. Alleles are now sorted
  deterministically (score, then name); every allele tied at the top is
  reported. Gene detection joins the tied allele names in the summary cell
  (e.g. `aadA1/aadA2`) and writes one `fullgenes` row per allele; MLST joins the
  tied allele numbers (e.g. `11/14`) and flags the ST uncertain (`?`), since the
  locus — and therefore the ST — is ambiguous. The truncation heuristic still
  applies only to a single, clean, well-covered top allele. Behavioral change;
  the single-allele case (the overwhelming majority) is unchanged. Re-validate
  against the PHoeNIx reference dataset before production. ([#46])

### Fixed

- MLST allele names that do not contain the `--mlst_delimiter` no longer crash
  the whole run with a cryptic `IndexError`. `get_allele_name_from_db` now
  raises a clear `CommandError` naming the allele and delimiter, which is caught
  per sample (the sample is recorded as failed and the run continues) — a
  common cause of the upstream `list index out of range` reports
  ([katholt#113]). ([#60])

- Consensus headers now use the actual `sample_name` (threaded through
  `read_pileup_data`/`parse_scores`) instead of parsing it out of the pileup
  filename. The old positional parse (`pileup_file.split(".")[1].split("__")[1]`)
  crashed on paths/prefixes containing extra `.`s, reported by CDC and PHAC
  upstream ([katholt#143], [katholt#99]); the fix that shipped in the bioconda
  recipe (thread `sample_name`) never reached upstream GitHub. This adopts that
  root-cause fix, superseding the filename-parse-with-fallback introduced in
  #5. Behavioral (the consensus header's sample-name field is now the true
  sample name). ([#55])
- Adopted upstream fix #69 ("round penalty to integer", commit `9eaedff`) that
  our `v0.2.0`-based port was missing: the deletion/edge penalties in
  `read_pileup_data` are now `round(penalty)` rather than the raw float. This
  matches the later upstream commit (`73f885f`) that the earlier production
  builds actually ran, which our baseline was behind. Behavioral scoring change;
  re-validate against the PHoeNIx reference dataset before production. (Note:
  Python 3's `round()` uses banker's rounding for exact `.5` values, a minor
  difference from Python 2's round-half-up.) ([#52])
- `qsub_srst2.py` now uses a `#!/usr/bin/env python3` shebang instead of a
  hardcoded Python 2.7 interpreter path; `slurm_srst2.py` uses a generic
  `module load srst2` and only passes `--threads` when >1; and
  `database_clustering/VFDB_cdhit_to_csv.py` also recognises `gb|` accessions in
  VFDB headers. (Carried over from upstream `73f885f`.) ([#52])
- Hardened shell/command construction against spaces and metacharacters in
  filenames. `getmlst.py` reads the first line of the combined FASTA in pure
  Python instead of `os.popen("head -n 1 " + filename)`. `slurm_srst2.py`
  submits the job script through `subprocess` on `sbatch`'s stdin instead of
  `os.system('echo "..." | sbatch')`, and both `slurm_srst2.py` and
  `qsub_srst2.py` now `shlex.quote` the fastq paths, run directory, and output
  prefix embedded in the submitted command. ([#50])
- The pre-run consensus cleanup now removes the files that are actually written
  (`${output}.new_consensus_alleles.fasta` and, when `--report_all_consensus`
  is set, `${output}.all_consensus_alleles.fasta`) instead of a never-written
  `${output}.consensus_alleles.fasta`. Those files are opened in append mode, so
  re-running into the same `--output` prefix previously appended duplicate
  consensus records; re-runs now start clean. ([#48])
- Multi-digit indel lengths in the pileup are no longer mis-parsed. In
  `read_pileup_data`, `+`/`-` indels were skipped by reading only the first
  digit of the length (`int(aligned_bases[i + 1])`), so any indel of 10 bp or
  more advanced the parser incorrectly and the remaining indel bases were
  counted as matches/SNPs — mis-counting mismatches and corrupting the
  consensus. Now consume all consecutive digits after `+`/`-` and skip that
  many bases. This is a behavioral fix — results change for reads spanning an
  indel of 10 bp or more. ([#44])

## [0.3.1] - 2026-07-18

Maintenance release: brings the `database_clustering/` helper scripts up to a
modern Python 3 / Biopython stack and removes the `rpy2` + R dependency.

### Changed

- Rewrote `database_clustering/align_plot_tree_min3.py` as pure Python, dropping
  the `rpy2` + R (`ape`) dependency. It now builds neighbour-joining trees with
  Biopython (`AlignIO` + `Bio.Phylo.TreeConstruction`) and renders them to a
  multi-page PDF with matplotlib, and takes an argparse CLI (`--input_dir`,
  `--pattern`, `--output`, `--min_seqs`) in place of the previous hardcoded
  path. `matplotlib` is now declared in `setup.py`. (Generating the input
  alignments with an external aligner such as muscle/mafft remains a
  prerequisite.) ([#41])

### Fixed

- Modernized the `database_clustering/` helper scripts for Python 3 and current
  Biopython, with no behavior or CLI changes: dropped the removed `Bio.Alphabet`
  import from `VFDBgenus.py` and `csv_to_gene_db.py`; removed the alphabet
  argument from `Seq(...)` (removed in modern Biopython); replaced the removed
  `Bio.Align.Applications.MuscleCommandline` in `align_plot_tree_min3.py` with a
  direct command construction (execution stays disabled, as before); raw-stringed
  the invalid-escape regexes; removed dead imports; and defined the previously
  undefined `DoError` helper in `csv_to_gene_db.py` so its argument-validation
  paths exit cleanly instead of raising `NameError`. ([#39])

## [0.3.0] - 2026-07-18

The first working, modernized Python 3 release. SRST2 v0.2.0 (the last upstream
release, 2016) ported to Python 3.12 and coded against a current toolchain
(bowtie2 2.5.x, samtools 1.x), validated end-to-end. Backward compatibility with
the pre-1.9 samtools interface is intentionally dropped in favor of forward
compatibility. All bundled scripts are maintained, not just `srst2.py`.

### Changed

- Ported the SRST2 v0.2.0 source tree from Python 2.7 to Python 3.12: `2to3`
  translation, the removed `file()` builtin replaced with `open()`, and the `mock`
  backport swapped for the standard-library `unittest.mock` in tests. Behavioral
  fixes are tracked separately. ([#1])
- Normalized the whole tree to 4-space indentation and consistent style with
  `ruff format` (no behavioral change). ([#3])
- `setup.py` now declares `python_requires = ">=3.12"` and lists `numpy`,
  `scipy`, and `biopython` as runtime dependencies (previously left for the
  user to install). The Python deps are intentionally not lower-pinned — the
  code uses only long-stable APIs — so pip provisions a working environment
  without over-constraining versions. ([#34])
- Tool-version gates are now **minimum-version checks** rather than hardcoded
  exact-match lists. `check_bowtie_version`/`check_samtools_version` parse the
  reported version and require it to be at or above a floor
  (`BOWTIE2_MIN_VERSION = 2.4.0`, `SAMTOOLS_MIN_VERSION = 1.9`; tested against
  bowtie2 2.5.4 / samtools 1.22.1), accepting any newer release. This
  supersedes the earlier exact-list extension ([#24]) and also fixes a latent
  string-ordering bug (`"1.2"` substring-matched `"1.24"`). Applied in
  `srst2.py`, `slurm_srst2.py`, and `qsub_srst2.py`. ([#28])
- Version is now resolved with `importlib.metadata.version("srst2")` instead of
  `pkg_resources.require(...)`, removing the runtime dependency on
  `setuptools`/`pkg_resources`. When the package metadata is unavailable (an
  uninstalled source checkout), the version reports an explanatory message
  instead of a hardcoded release number that would go stale. `setup.py` now
  imports `setuptools` rather than the removed `distutils.core`. Reproduces the
  third inline "jvhagey" production patch (version hardcode) with a
  non-stale, self-updating implementation. ([#7])
- Annotation lookup for `--no_gene_details` now scans the FASTA in-process
  instead of shelling out to `grep`. The old unquoted `grep <allele> <fasta>`
  treated the allele name as a regex, so gene names containing parentheses
  (e.g. `aph(3')-Ia`) matched wrongly or not at all; the in-process scan
  matches the literal name and removes the `grep`/subprocess dependency.
  Reproduces the second inline "jvhagey" production patch. ([#6])

### Fixed

- `consensus_alignment.py` now imports under modern Biopython. It imported the
  `Bio.Alphabet` module (removed in Biopython 1.78) plus unused `Seq`/
  `SeqRecord`; only `SeqIO` is actually used. Dropped the three unused imports —
  no alphabet is needed. Verified end-to-end splitting real srst2 consensus
  output into per-locus FASTAs on Biopython 1.86. ([#32])
- `analyseSRST2.py` now imports under a modern SciPy. It carried a dead
  `from scipy.stats import binom_test, linregress` import (neither name is used
  in the file); `binom_test` was removed in SciPy 1.12, so the stale import
  broke the whole module. Removed the unused import. ([#30])
- Removed the `-L 1000` flag from the `samtools mpileup` call. `-L` was removed
  from `samtools mpileup` in samtools 1.9 (it belonged to the BCF/VCF calling
  path that moved to `bcftools`), so on any modern samtools the pileup step
  errored with `invalid option -- 'L'` and produced no output. srst2 consumes
  only the text pileup, so the flag was never needed. Verified end-to-end
  against samtools 1.22.1 (the container's version) and 1.24. ([#26])
- `getmlst.py` now runs under Python 3. It still imported the Python-2-only
  `urllib2` module (`ModuleNotFoundError`, so even `--help` failed) and wrote
  the `bytes` returned by `urlopen().read()` to text-mode files (`TypeError`).
  Import `urllib.request` and decode the downloaded profile/locus content
  before writing. Completes the Python 3 port for this script. ([#20])
- Escaped the backslashes in the bowtie2 `--other` and samtools mpileup
  argument `help=` strings (`"\\--no-mixed"`, `"\\-A"`). `\-` is an invalid
  escape sequence in a Python 3 string literal (a `SyntaxWarning`); doubling
  the backslash both silences the warning and makes the help text render the
  intended literal backslash. With this, all scripts compile clean under
  `python3 -W error::SyntaxWarning`. ([#11])
- Error logging in the per-database handler used `e.message`, which does not
  exist on Python 3 exceptions, so the handler itself raised `AttributeError`
  and masked the real error. It now logs `str(e)`. `CommandError` is also
  raised with a plain message string instead of a `{"message": ...}` dict, so
  the logged/propagated text is the message itself rather than a dict repr —
  applied consistently in `srst2.py`, `slurm_srst2.py`, and `qsub_srst2.py`
  (the wrappers raise `CommandError` uncaught, so this cleans up their
  tracebacks too). ([#10])
- Regex literals with backslash escapes are now raw strings: `r"NM:i:(\d+)\s"`
  in `srst2.py` and `r">(.*)([_-])(\d*)"` in `getmlst.py`. `\d`/`\s` are invalid
  escape sequences in ordinary Python 3 string literals (a `SyntaxWarning` that
  is slated to become a `SyntaxError`). ([#9])
- Tool-version checks now decode `subprocess.check_output` bytes to `str`
  before the `str in ...` membership tests, in `srst2.py`
  (`check_command_version`, `check_command_versions`) and in the
  `slurm_srst2.py` / `qsub_srst2.py` wrappers. Under Python 3 the checks
  compared a `str` against `bytes`, which never matched, so bowtie2/samtools
  were reported as the wrong version. ([#8])
- Consensus FASTA output: parse the sample name from the pileup filename by
  splitting on the `__` sample delimiter instead of positionally on `.`, so
  allele names containing a dot (e.g. `NG_047667.1`) no longer raise
  `IndexError`. Reproduces the first inline "jvhagey" production patch. ([#5])

[Unreleased]: https://github.com/amd-ph-core/srst2/compare/v1.0.0-rc.1...dev
[1.0.0-rc.1]: https://github.com/amd-ph-core/srst2/compare/v0.3.1...v1.0.0-rc.1
[0.3.1]: https://github.com/amd-ph-core/srst2/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/amd-ph-core/srst2/compare/v0.2.0...v0.3.0
[#1]: https://github.com/amd-ph-core/srst2/issues/1
[#3]: https://github.com/amd-ph-core/srst2/issues/3
[#5]: https://github.com/amd-ph-core/srst2/issues/5
[#6]: https://github.com/amd-ph-core/srst2/issues/6
[#7]: https://github.com/amd-ph-core/srst2/issues/7
[#8]: https://github.com/amd-ph-core/srst2/issues/8
[#9]: https://github.com/amd-ph-core/srst2/issues/9
[#10]: https://github.com/amd-ph-core/srst2/issues/10
[#11]: https://github.com/amd-ph-core/srst2/issues/11
[#20]: https://github.com/amd-ph-core/srst2/issues/20
[#24]: https://github.com/amd-ph-core/srst2/issues/24
[#26]: https://github.com/amd-ph-core/srst2/issues/26
[#28]: https://github.com/amd-ph-core/srst2/issues/28
[#30]: https://github.com/amd-ph-core/srst2/issues/30
[#32]: https://github.com/amd-ph-core/srst2/issues/32
[#34]: https://github.com/amd-ph-core/srst2/issues/34
[#39]: https://github.com/amd-ph-core/srst2/issues/39
[#41]: https://github.com/amd-ph-core/srst2/issues/41
[#44]: https://github.com/amd-ph-core/srst2/issues/44
[#46]: https://github.com/amd-ph-core/srst2/issues/46
[#48]: https://github.com/amd-ph-core/srst2/issues/48
[#50]: https://github.com/amd-ph-core/srst2/issues/50
[#52]: https://github.com/amd-ph-core/srst2/issues/52
[#55]: https://github.com/amd-ph-core/srst2/issues/55
[#60]: https://github.com/amd-ph-core/srst2/issues/60
[#62]: https://github.com/amd-ph-core/srst2/issues/62
[katholt#99]: https://github.com/katholt/srst2/issues/99
[katholt#109]: https://github.com/katholt/srst2/issues/109
[katholt#113]: https://github.com/katholt/srst2/issues/113
[katholt#143]: https://github.com/katholt/srst2/issues/143
