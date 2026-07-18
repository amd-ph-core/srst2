# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This repository is a maintenance fork of [katholt/srst2](https://github.com/katholt/srst2)
at tag `v0.2.0` (the last upstream release, 2016), ported to Python 3 and maintained
for continued use.

## [Unreleased]

### Changed

- Ported the SRST2 v0.2.0 source tree from Python 2.7 to Python 3.12: `2to3`
  translation, the removed `file()` builtin replaced with `open()`, and the `mock`
  backport swapped for the standard-library `unittest.mock` in tests. Behavioral
  fixes are tracked separately. ([#1])
- Normalized the whole tree to 4-space indentation and consistent style with
  `ruff format` (no behavioral change). ([#3])

### Changed

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

[Unreleased]: https://github.com/amd-ph-core/srst2/compare/v0.2.0...dev
[#1]: https://github.com/amd-ph-core/srst2/issues/1
[#3]: https://github.com/amd-ph-core/srst2/issues/3
[#5]: https://github.com/amd-ph-core/srst2/issues/5
[#6]: https://github.com/amd-ph-core/srst2/issues/6
[#7]: https://github.com/amd-ph-core/srst2/issues/7
[#8]: https://github.com/amd-ph-core/srst2/issues/8
[#9]: https://github.com/amd-ph-core/srst2/issues/9
[#10]: https://github.com/amd-ph-core/srst2/issues/10
[#11]: https://github.com/amd-ph-core/srst2/issues/11
