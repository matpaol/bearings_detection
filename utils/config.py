"""Central configuration for the bearing fault-diagnosis project.

All parameters live here so they are defined in one place, with no magic
numbers scattered across modules. This module performs no I/O.
"""

from pathlib import Path

# remote dataset
BASE_URL = "https://groups.uni-paderborn.de/kat/BearingDataCenter/"

# local paths
DATA_DIR = Path("data")     # where archives are downloaded and extracted
CLEAN_DIR = Path("clean")   # where the built dataset is saved

# acquisition
SAMPLING_FREQUENCY = 64_000   # Hz, motor current channel
RECORDING_SECONDS = 4.0       # nominal duration of each recording
SIGNAL = "phase_current_1"    # stator current used for diagnosis

# reproducibility
SEED = 42

# fault taxonomy: the code prefix encodes the fault location
LOCATION_BY_PREFIX = {"K": "normal", "KA": "outer", "KI": "inner", "KB": "combined"}
CLASS_ID_BY_LOCATION = {"normal": 0, "outer": 1, "inner": 2}

# damage nature, documented by Lessmeier et al. (2016): not derivable from the code
REAL_BEARINGS = {
    "KA04", "KA15", "KA16", "KA22", "KA30",
    "KI04", "KI14", "KI16", "KI17", "KI18", "KI21",
    "KB23", "KB24", "KB27",
}
ARTIFICIAL_BEARINGS = {
    "KA01", "KA03", "KA05", "KA06", "KA07", "KA08", "KA09",
    "KI01", "KI03", "KI05", "KI07", "KI08",
}
