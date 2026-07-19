# Retrieve the installed version of srst2 without a runtime dependency on
# setuptools/pkg_resources. importlib.metadata is in the standard library
# (Python 3.8+) and reads the version recorded at install time, so it always
# tracks the release the package was built from. When the package metadata is
# not available (e.g. running straight from a source checkout that was never
# installed), report an explanatory message rather than a hardcoded release
# number, which would otherwise silently go stale as the project is versioned.
from importlib.metadata import PackageNotFoundError, version as _get_version

try:
    srst2_version = _get_version("srst2")
except PackageNotFoundError:
    srst2_version = (
        "unknown (srst2 package metadata not found; "
        "install srst2 with `pip install .` to record its version)"
    )
