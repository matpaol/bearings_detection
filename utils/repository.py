"""Access to the remote Paderborn bearing data repository.

Interacts with the KAT Bearing Data Center: lists the available bearings,
downloads their archives and extracts them locally. Downloading and
extracting are separate steps.
"""

import re
import subprocess
from pathlib import Path
from urllib.request import urlopen, urlretrieve


def list_available_bearings(base_url: str) -> list[str]:
    """List the bearing codes offered by the remote repository.

    Parameters
    ----------
    base_url : str
        URL of the data center index page.

    Returns
    -------
    list[str]
        Sorted bearing codes (e.g. 'K001', 'KA04'), without the .rar suffix.
    """
    html = urlopen(base_url).read().decode("utf-8", "ignore")
    codes = set(re.findall(r"([A-Z]+\d+)\.rar", html))
    return sorted(codes)


def download_bearing(code: str, dest_dir: Path, base_url: str) -> Path:
    """Download one bearing archive, skipping it if already present.

    Returns
    -------
    Path
        Path to the local .rar archive.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    archive = dest_dir / f"{code}.rar"
    if not archive.exists():
        urlretrieve(f"{base_url}{code}.rar", archive)
    return archive


def extract_bearing(archive: Path, dest_dir: Path) -> Path:
    """Extract a bearing archive into its own folder under dest_dir.

    Returns
    -------
    Path
        Path to the folder containing the extracted files.
    """
    archive = Path(archive)
    target = Path(dest_dir) / archive.stem
    target.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["unrar", "x", "-o+", "-inul", str(archive), f"{target}/"],
        check=True,
    )
    return target
