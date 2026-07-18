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
