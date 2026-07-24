"""Reading and cataloguing the Paderborn bearing dataset.

Domain-oriented helpers. A recording is a .mat file holding several named
signals. A bearing is identified by a code that encodes its fault location;
its damage nature (healthy, real, artificial) is documented externally.
"""

from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat

from . import config


@dataclass(frozen=True)
class BearingMetadata:
    """Static properties of a bearing, derived from its code."""

    code: str
    location: str          # "normal" | "outer" | "inner" | "combined"
    nature: str            # "healthy" | "real" | "artificial"
    class_id: int | None   # 0/1/2 for the study classes, None otherwise


def _prefix(code: str) -> str:
    return "".join(ch for ch in code if not ch.isdigit())


def bearing_metadata(code: str) -> BearingMetadata:
    """Build the metadata of a bearing from its code (e.g. 'KA04')."""
    location = config.LOCATION_BY_PREFIX[_prefix(code)]
    if location == "normal":
        nature = "healthy"
    elif code in config.REAL_BEARINGS:
        nature = "real"
    elif code in config.ARTIFICIAL_BEARINGS:
        nature = "artificial"
    else:
        raise ValueError(f"unknown damage nature for bearing {code}")
    return BearingMetadata(
        code=code,
        location=location,
        nature=nature,
        class_id=config.CLASS_ID_BY_LOCATION.get(location),
    )


def census(codes: list[str]) -> pd.DataFrame:
    """Count bearings per fault location and damage nature."""
    frame = pd.DataFrame(asdict(bearing_metadata(c)) for c in codes)
    return (
        frame.groupby(["location", "nature"])
        .size()
        .reset_index(name="bearings")
    )


def _recording_struct(mat_path: Path) -> dict:
    """Return the single MATLAB struct stored in a recording file."""
    mat = loadmat(mat_path, simplify_cells=True)
    names = [k for k in mat if not k.startswith("__")]
    if not names:
        raise ValueError(f"no data struct found in {mat_path}")
    return mat[names[0]]


def load_signal(mat_path: Path, signal_name: str) -> np.ndarray:
    """Return one named signal (e.g. 'phase_current_1') from a recording."""
    struct = _recording_struct(mat_path)
    for channel in struct["Y"]:
        if channel["Name"] == signal_name:
            return np.asarray(channel["Data"]).ravel()
    raise KeyError(f"signal {signal_name!r} not found in {mat_path}")


def signal_summary(
    mat_path: Path, recording_seconds: float = config.RECORDING_SECONDS
) -> pd.DataFrame:
    """List the signals in a recording with sample count and sampling rate."""
    struct = _recording_struct(mat_path)
    rows = [
        {
            "signal": channel["Name"],
            "samples": np.asarray(channel["Data"]).size,
            "sampling_hz": round(np.asarray(channel["Data"]).size / recording_seconds),
        }
        for channel in struct["Y"]
    ]
    return pd.DataFrame(rows)
