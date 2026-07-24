"""Signal preprocessing for the Paderborn bearing current signals.

Pure array transformations: a raw current signal is turned into a set of
standardized frames, one per shaft revolution, all resampled to a common
length. No file I/O and no plotting here (see data.py for loading).
"""

import numpy as np
from scipy.signal import resample


def samples_per_revolution(rpm: float, sampling_frequency: int) -> int:
    """Number of signal samples spanned by one shaft revolution.

    Parameters
    ----------
    rpm : float
        Measured rotational speed of the shaft, in revolutions per minute.
    sampling_frequency : int
        Sampling frequency of the signal, in Hz.

    Returns
    -------
    int
        Samples per revolution, rounded to the nearest integer.
    """
    if rpm <= 0:
        raise ValueError(f"rpm must be positive, got {rpm}")
    revolutions_per_second = rpm / 60.0
    return round(sampling_frequency / revolutions_per_second)


def segment_by_revolution(signal: np.ndarray, samples_per_rev: int) -> np.ndarray:
    """Cut a 1-D signal into consecutive one-revolution frames.

    The trailing samples that do not fill a full revolution are discarded.

    Parameters
    ----------
    signal : np.ndarray
        One-dimensional signal (a single recording).
    samples_per_rev : int
        Length of one revolution in samples (see samples_per_revolution).

    Returns
    -------
    np.ndarray
        Array of shape (n_frames, samples_per_rev).
    """
    signal = np.asarray(signal).ravel()
    if samples_per_rev <= 0:
        raise ValueError(f"samples_per_rev must be positive, got {samples_per_rev}")
    n_frames = signal.size // samples_per_rev
    if n_frames == 0:
        raise ValueError(
            f"signal too short ({signal.size} samples) for one revolution "
            f"({samples_per_rev} samples)"
        )
    usable = signal[: n_frames * samples_per_rev]
    return usable.reshape(n_frames, samples_per_rev)


def resample_frames(frames: np.ndarray, target_length: int) -> np.ndarray:
    """Resample every frame to a common length.

    Uses the Fourier-based resampler, which band-limits the signal and so
    avoids aliasing. With target_length equal to the largest native frame
    length in the dataset, this only ever upsamples.

    Parameters
    ----------
    frames : np.ndarray
        Array of shape (n_frames, samples_per_rev).
    target_length : int
        Desired number of samples per frame after resampling.

    Returns
    -------
    np.ndarray
        Array of shape (n_frames, target_length).
    """
    if target_length <= 0:
        raise ValueError(f"target_length must be positive, got {target_length}")
    return resample(frames, target_length, axis=1)


def standardize(frames: np.ndarray) -> np.ndarray:
    """Standardize each frame to zero mean and unit standard deviation.

    The normalization is per frame (row-wise): amplitude differences between
    recordings are removed, so the model focuses on shape, not scale.

    Parameters
    ----------
    frames : np.ndarray
        Array of shape (n_frames, frame_length).

    Returns
    -------
    np.ndarray
        Standardized array, same shape as the input.
    """
    frames = np.asarray(frames, dtype=np.float64)
    mean = frames.mean(axis=1, keepdims=True)
    std = frames.std(axis=1, keepdims=True)
    std[std == 0] = 1.0
    return (frames - mean) / std
