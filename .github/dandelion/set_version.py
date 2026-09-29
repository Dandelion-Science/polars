"""Set the distribution version of ``polars`` and ``polars-runtime-32``.

Only the package metadata changes: ``_plr.py`` and the crates keep the upstream
version, so polars' import-time runtime version check still passes.

Usage: ``python .github/dandelion/set_version.py [VERSION]``, where ``VERSION`` must be
``<upstream>.postN``. Without it, ``<upstream>.post0`` is used (dry-run builds).
"""

import re
import sys
from pathlib import Path

POLARS = Path("py-polars/pyproject.toml")
RUNTIME = Path("py-polars/runtime/polars-runtime-32/pyproject.toml")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if text.count(old) != 1:
        sys.exit(f"Expected exactly one {old!r} in {path}.")
    path.write_text(text.replace(old, new))


upstream = re.search(r'^version = "(.+)"$', POLARS.read_text(), re.M).group(1)
version = sys.argv[1] if len(sys.argv) > 1 else f"{upstream}.post0"
if re.fullmatch(rf"{re.escape(upstream)}\.post\d+", version) is None:
    sys.exit(f"Version {version!r} is not a post-release of upstream {upstream!r}.")
replace_once(POLARS, f'version = "{upstream}"', f'version = "{version}"')
replace_once(POLARS, f'"polars-runtime-32 == {upstream}"', f'"polars-runtime-32 == {version}"')
replace_once(RUNTIME, 'dynamic = ["version"]', f'version = "{version}"')
print(version)
