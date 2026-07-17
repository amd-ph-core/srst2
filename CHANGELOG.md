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

[Unreleased]: https://github.com/amd-ph-core/srst2/compare/v0.2.0...dev
[#1]: https://github.com/amd-ph-core/srst2/issues/1
